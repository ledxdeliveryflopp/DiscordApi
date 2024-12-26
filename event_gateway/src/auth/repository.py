from dataclasses import dataclass
from datetime import datetime

from loguru import logger
from sqlalchemy import Select
from starlette.websockets import WebSocket, WebSocketDisconnect

from src.auth.models import UserModel, ConfirmationCodeModel
from src.auth.sockets import socket_manager
from src.auth.utils import check_token_payload, get_user_id_from_token, create_confirmation_code
from src.broker.router import broker_service
from src.settings.service import BaseService


@dataclass
class AuthEventsRepository(BaseService):

    async def _repository_find_user(self, user_id: int) -> UserModel:
        """Поиск пользователя по id"""
        user = await self.session.execute(Select(UserModel).where(UserModel.id == user_id))
        return user.scalar()

    async def _repository_find_confirmation_code(self, code: str) -> ConfirmationCodeModel:
        """Поиск кода подтверждения"""
        confirmation_code = await self.email_session.execute(
            Select(ConfirmationCodeModel).where(ConfirmationCodeModel.code == code))
        return confirmation_code.scalar()

    @staticmethod
    async def handle_heartbeat_op(websocket: WebSocket):
        await websocket.send_json({"op": "heartbeat_ack"})

    async def handle_pending_ticket_op(self, websocket: WebSocket, client_id: str, receive_data: dict, client_ip: str):
        encrypted_user_payload = receive_data.get("encrypted_user_payload")
        if not encrypted_user_payload:
            await websocket.send_json({"op": "Empty encrypted_user_payload variable"})
        else:
            check_user_payload = await check_token_payload(encrypted_user_payload)
            if check_user_payload is False:
                await websocket.send_json({"op": "Error while check user payload"})
            else:
                user_id = await get_user_id_from_token(encrypted_user_payload)
                check_user = await self._repository_find_user(user_id)
                if not check_user:
                    await websocket.send_json({"op": "User saved in encrypted payload dont found"})
                else:
                    user_clients = check_user.clients_fingerprints
                    if client_id not in user_clients:
                        await websocket.send_json({"op": f"New auth device detected,"
                                                         f" send confirmation code to: {check_user.email}"})
                        confirmation_code = await create_confirmation_code(user_id, client_id)
                        await broker_service.send_email_data_in_queue(check_user.email, confirmation_code,
                                                                      client_ip)
                    else:
                        await socket_manager.broadcast({"op": "Success auth",
                                                        "user_payload": encrypted_user_payload}, client_id)
                        await socket_manager.success_close_all_connections(client_id)
                        return False

    async def handle_pending_ticket_confirmation_op(self, websocket: WebSocket, client_id: str, receive_data: dict):
        confirmation_code = receive_data.get("confirmation_code")
        if not confirmation_code:
            await websocket.send_json({"op": "Empty confirmation_code variable"})
        else:
            check_code = await self._repository_find_confirmation_code(confirmation_code)
            if not check_code:
                await websocket.send_json({"op": "Confirmation code dont exist"})
            elif check_code.expire < datetime.utcnow():
                await self.delete_confirmation_code(check_code)
                await websocket.send_json({"op": "Confirmation code expired"})
            else:
                encrypted_user_payload = receive_data.get("encrypted_user_payload")
                if not encrypted_user_payload:
                    await websocket.send_json({"op": "Empty encrypted_user_payload variable"})
                else:
                    check_user_payload = await check_token_payload(encrypted_user_payload)
                    if check_user_payload is False:
                        await websocket.send_json({"op": "Error while check user payload"})
                    else:
                        user_id = await get_user_id_from_token(encrypted_user_payload)
                        check_user = await self._repository_find_user(user_id)
                        if not check_user:
                            await websocket.send_json({"op": "User saved in encrypted payload dont found"})
                        else:
                            await self.delete_confirmation_code(check_code)
                            await socket_manager.broadcast({"op": "Success auth",
                                                            "user_payload": encrypted_user_payload}, client_id)
                            await socket_manager.success_close_all_connections(client_id)
                            return False

    async def handle_opcode(self, websocket: WebSocket, receive_data: dict, opcode: str, client_id: str,
                            client_ip: str) -> bool | None:
        """Обработка опкодов вебсокета авторизации"""
        check_hub = await socket_manager.check_hub_exist(client_id)
        if check_hub is True:
            if opcode == "heartbeat":
                await self.handle_heartbeat_op(websocket)
            elif opcode == "pending_ticket":
                handle_status = await self.handle_pending_ticket_op(websocket, client_id, receive_data, client_ip)
                if handle_status is False:
                    return False
            elif opcode == "pending_ticket_confirmation":
                handle_status = await self.handle_pending_ticket_confirmation_op(websocket, client_id, receive_data)
                if handle_status is False:
                    return False

    async def _repository_handle_auth_websocket(self, websocket: WebSocket, client_id: str, client_ip: str,
                                                client_type: str) -> None:
        """Обработчик сокета авторизации"""
        await socket_manager.create_auth_hub(client_id, client_ip)
        await socket_manager.connect_to_auth_hub(websocket, client_id, client_ip, client_type)
        try:
            run = True
            while run is True:
                command_list: list = ["heartbeat", "pending_ticket", "pending_ticket_confirmation"]
                receive_data = await websocket.receive_json()
                receive_opcode = receive_data.get("op")
                if receive_opcode in command_list:
                    handler_status = await self.handle_opcode(websocket, receive_data, receive_opcode, client_id,
                                                              client_ip)
                    logger.debug(f"handle status: {handler_status}")
                    if handler_status is False:
                        run = False
                else:
                    await websocket.send_json({"op": "Opcode dont exits"})
        except WebSocketDisconnect:
            hub_status = await socket_manager.web_socket_disconnect_handler(websocket, client_id)
            if hub_status is False:
                return
