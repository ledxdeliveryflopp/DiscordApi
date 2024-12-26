from loguru import logger
from starlette import status
from starlette.websockets import WebSocket

from src.broker.router import BrokerService


class AuthConnectionManager(BrokerService):
    """Класс менеджера управления группами авторизации"""
    def __init__(self) -> None:
        self.auth_hub_list: dict = {}

    async def create_auth_hub(self, client_id: str, client_ip: str) -> None:
        """Создание группы авторизации"""
        hub_id = self.auth_hub_list.get(f"{client_id}")
        if not hub_id:
            new_hub = {f"{client_id}": {"client_ip": f"{client_ip}", "client_pc": None, "client_mb": None}}
            self.auth_hub_list.update(new_hub)
            logger.info(f"hun: {self.auth_hub_list}")
        else:
            pass

    async def connect_to_auth_hub(self, websocket: WebSocket, client_id: str, client_ip: str, client_type: str) -> None:
        """Подключение к группе авторизации"""
        hub: dict = self.auth_hub_list.get(f"{client_id}")
        if hub:
            hub_ip = hub.get("client_ip")
            logger.info(f"ip {hub_ip}")
            logger.info(f"hub2 {hub}")
            if hub_ip == client_ip:
                await websocket.accept()
                hub[f"client_{client_type}"] = websocket
                await websocket.send_json({"op": f"connected type: {client_type}"})
            else:
                await websocket.accept()
                await websocket.send_json({"op": "bad hub ip"})
                await websocket.close(status.WS_1000_NORMAL_CLOSURE, "bad hab ip")
        else:
            await websocket.accept()
            await websocket.send_json({"op": "bad hub id"})
            await websocket.close(status.WS_1000_NORMAL_CLOSURE, "bad hab id")

    async def broadcast(self, message: dict, client_id: str) -> None:
        """Отправка сообщения всем клиентам группы"""
        hub: dict = self.auth_hub_list.get(f"{client_id}")
        if hub:
            client_pc: WebSocket = hub.get("client_pc")
            client_mb: WebSocket = hub.get("client_mb")
            if client_pc and client_mb:
                await client_pc.send_json(message)
                await client_mb.send_json(message)

    async def web_socket_disconnect_handler(self, websocket: WebSocket, client_id: str) -> bool | None:
        """Обработка неожиданных отключений клиентов от хаба авторизации"""
        hub: dict = self.auth_hub_list.get(f"{client_id}")
        logger.debug(f"hub list: {self.auth_hub_list}")
        logger.debug(f"exception hub: {hub}")
        if hub:
            client_pc: WebSocket = hub.get("client_pc")
            client_mb: WebSocket = hub.get("client_mb")
            if not client_pc and not client_mb:
                hub.pop(f"{client_id}")
                return False
            elif client_pc == websocket:
                hub["client_pc"] = None
                await client_mb.send_json({"op": "pc client dropped connection"})
            elif client_mb == websocket:
                hub["client_mb"] = None
                await client_pc.send_json({"op": "mobile client dropped connection"})
        else:
            return False

    async def success_close_all_connections(self, client_id: str) -> None:
        """Успешно закрыть соединение с всеми клиентами в группе"""
        hub: dict = self.auth_hub_list.get(f"{client_id}")
        if hub:
            client_pc: WebSocket = hub.get("client_pc")
            client_mb: WebSocket = hub.get("client_mb")
            if client_pc:
                await client_pc.close(status.WS_1000_NORMAL_CLOSURE, "success auth")
            if client_mb:
                await client_mb.close(status.WS_1000_NORMAL_CLOSURE, "success auth")
            self.auth_hub_list.pop(f"{client_id}")
            logger.debug(f"closed: {client_id} hub")
            logger.debug(f"hub list success: {self.auth_hub_list}")

    async def check_hub_exist(self, client_id: str) -> bool:
        hub: dict = self.auth_hub_list.get(f"{client_id}")
        if hub:
            return True
        else:
            return False


socket_manager = AuthConnectionManager()
