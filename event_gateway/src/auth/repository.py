from dataclasses import dataclass
from datetime import datetime, timedelta

from fastapi import WebSocketException
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.websockets import WebSocket

from src.auth.models import UserModel, EmailAuthConfirmationCodeModel
from src.auth.sockets import socket_manager
from src.auth.utils import check_token_payload, get_user_id_from_token, get_request_user_ip, create_confirmation_code
from src.email.service import email_service
from src.settings.service import BaseService


@dataclass
class AuthEventsRepository(BaseService):
    session: AsyncSession

    async def _repository_find_user(self, user_id: int) -> UserModel:
        """Поиск пользователя по id"""
        user = await self.session.execute(Select(UserModel).where(UserModel.id == user_id))
        return user.scalar()

    async def _repository_find_confirmation_code(self, code: str) -> EmailAuthConfirmationCodeModel:
        """Поиск кода подтверждения"""
        code = await self.session.execute(Select(EmailAuthConfirmationCodeModel)
                                          .where(EmailAuthConfirmationCodeModel.code == code))
        return code.scalar()

    async def _repository_create_confirmation_code(self, code: str) -> None:
        """Создание кода подтверждения"""
        expire_date = datetime.utcnow() + timedelta(minutes=10)
        new_code = EmailAuthConfirmationCodeModel(code=code, expire=expire_date)
        await self.save_object(new_code)

    async def _repository_handle_auth_websocket(self, websocket: WebSocket, client_id: str) -> None:
        """Обработчик сокета авторизации"""
        await socket_manager.create_auth_hub(client_id=client_id)
        await socket_manager.connect_to_auth_hub(websocket, client_id)
        try:
            success = True
            while success is True:
                receive_json = await websocket.receive_json()
                receive_data = receive_json.get("op")
                if receive_data == "heartbeat":
                    await socket_manager.heartbeat_ack(websocket, client_id)
                if receive_data == "pending_ticket":
                    user_data = receive_json.get("encrypted_user_payload")
                    check_user_payload = await check_token_payload(user_data)
                    if check_user_payload is False:
                        await socket_manager.send_message_to_client(websocket, client_id, {"op": "bad user payload"})
                    user_id = await get_user_id_from_token(user_data)
                    user_info = await self._repository_find_user(user_id)
                    if not user_info:
                        await socket_manager.send_message_to_client(websocket, client_id, {"op": "user not found"})
                    user_clients = user_info.clients_fingerprints
                    if client_id not in user_clients:
                        request_user_ip = await get_request_user_ip()
                        confirmation_code = await create_confirmation_code(user_info.id)
                        await self._repository_create_confirmation_code(confirmation_code)
                        await email_service.send_email_message(user_info.email, request_user_ip, confirmation_code)
                        await socket_manager.send_message_to_client(websocket, client_id,
                                                                    {"op": "Enter confirmation code from email message"})
                    else:
                        await socket_manager.broadcast({"op": "access granted", "auth_token": f"{user_data}"},
                                                       client_id)
                        user_info = await self._repository_find_user(user_id)
                        new_list = []
                        for i in user_info.clients_fingerprints:
                            if i == client_id:
                                pass
                            else:
                                new_list.append(i)
                        new_list.append(client_id)
                        user_info.clients_fingerprints = new_list
                        await self.save_object(user_info)
                        await socket_manager.success_close_all_connections(client_id)
                        success = False
                if receive_data == "pending_ticket_confirmation":
                    code = receive_json.get("code")
                    confirmation_code = await self._repository_find_confirmation_code(code)
                    if not confirmation_code:
                        await socket_manager.send_message_to_client(websocket, client_id,
                                                                    {"op": "Bad confirmation code"})
                    if confirmation_code.expire < datetime.utcnow():
                        await socket_manager.send_message_to_client(websocket, client_id,
                                                                    {"op": "Confirmation code expire"})
                        await self.delete_object(confirmation_code)
                    await socket_manager.broadcast({"op": "success confirmation"}, client_id)
                    await self.delete_object(confirmation_code)
        except Exception as unknown_exception:
            await socket_manager.broadcast({"op": "error, disconnect all clients in hub"}, client_id)
            await socket_manager.error_close_all_connections(client_id)
            raise WebSocketException(code=status.WS_1011_INTERNAL_ERROR, reason="server error")
