from dataclasses import dataclass

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket

from src.auth.models import UserModel
from src.auth.sockets import socket_manager
from src.auth.utils import check_token_payload


@dataclass
class AuthEventsRepository:
    session: AsyncSession

    async def _repository_find_user(self, user_id: int) -> UserModel:
        user = await self.session.execute(Select(UserModel).where(UserModel.id == user_id))
        return user.scalar()

    @staticmethod
    async def _repository_handle_auth_websocket(websocket: WebSocket, client_id: str) -> None:
        await socket_manager.create_auth_hub(client_id=client_id)
        await socket_manager.connect_to_auth_hub(websocket, client_id)
        try:
            status = True
            while status is True:
                receive_json = await websocket.receive_json()
                receive_data = receive_json.get("op")
                if receive_data == "heartbeat":
                    await socket_manager.heartbeat_ack(websocket, client_id)
                if receive_data == "pending_ticket":
                    user_data = receive_json.get("encrypted_user_payload")
                    check_user_payload = await check_token_payload(user_data)
                    if check_user_payload is True:
                        await socket_manager.broadcast({"op": "access granted", "auth_token": f"{user_data}"},
                                                       client_id)
                        await socket_manager.success_close_all_connections(client_id)
                        status = False
                    else:
                        await socket_manager.send_message_to_client(websocket, client_id, {"op": "bad user payload"})
        except Exception as exc:
            pass
