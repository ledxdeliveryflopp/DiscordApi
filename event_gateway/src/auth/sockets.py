from loguru import logger
from starlette.websockets import WebSocket


class AuthConnectionManager:
    """Класс менеджера управления группами авторизации"""
    def __init__(self) -> None:
        self.auth_hub_list: list[dict] = []
        self.auth_hub_id_list: list[str] = []

    async def create_auth_hub(self, client_id: str) -> None:
        """Создание группы авторизации"""
        if client_id in self.auth_hub_id_list:
            pass
        else:
            hub = {"id": client_id, "clients": []}
            self.auth_hub_list.append(hub)
            self.auth_hub_id_list.append(client_id)

    async def connect_to_auth_hub(self, websocket: WebSocket, client_id: str) -> None:
        """Подключение к группе авторизации"""
        for hub in self.auth_hub_list:
            if hub.get("id") == client_id:
                clients_list = hub.get("clients")
                clients_list_len = len(clients_list)
                if clients_list_len == 0:
                    await websocket.accept()
                    await websocket.send_json({"op": "wait mobile connect"})
                    clients_list.append(websocket)
                elif clients_list_len == 1:
                    await websocket.accept()
                    pc_client: WebSocket = clients_list[0]
                    await pc_client.send_json({"op": "mobile connected"})
                    clients_list.append(websocket)
                else:
                    await websocket.accept()
                    await websocket.send_json({"op": "hub is full"})
                    await websocket.close(1000, "full auth hub")
            else:
                await websocket.accept()
                await websocket.send_json({"op": "bad hub id"})
                await websocket.close(1000, "bad hab id")

    async def heartbeat_ack(self, websocket: WebSocket, client_id: str) -> None:
        """Ответ на heartbeat"""
        for hub in self.auth_hub_list:
            if hub.get("id") == client_id:
                await websocket.send_json({"op": "heartbeat_ack"})

    async def send_message_to_client(self, websocket: WebSocket, client_id: str, message: dict) -> None:
        """Отправка сообщения клиенту"""
        for hub in self.auth_hub_list:
            if hub.get("id") == client_id:
                await websocket.send_json(message)

    async def broadcast(self, message: dict, client_id: str) -> None:
        """Отправка сообщения всем клиентам группы"""
        for hub in self.auth_hub_list:
            if hub.get("id") == client_id:
                clients_list = hub.get("clients")
                for connection in clients_list:
                    await connection.send_json(message)

    async def success_close_all_connections(self, client_id: str) -> None:
        """Успешно закрыть соединение с всеми клиентами в группе"""
        for hub in self.auth_hub_list:
            if hub.get("id") == client_id:
                clients_list = hub.get("clients")
                for connection in clients_list:
                    await connection.close(1000, "success auth")
                    self.auth_hub_list.remove(hub)
                    self.auth_hub_id_list.remove(client_id)
                    logger.debug(f"auth hub closed: {client_id}")


socket_manager = AuthConnectionManager()
