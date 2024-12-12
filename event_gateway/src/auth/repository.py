from dataclasses import dataclass

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket

from src.auth.models import UserModel
from src.auth.utils import get_user_id_from_token


@dataclass
class AuthEventsRepository:
    session: AsyncSession

    async def _repository_find_user(self, user_id: int) -> UserModel:
        user = await self.session.execute(Select(UserModel).where(UserModel.id == user_id))
        return user.scalar()

    async def _repository_get_user_auth_token(self, user_id: int) -> str | bool:
        user = await self._repository_find_user(user_id)
        auth_token = user.qr_auth_token
        return auth_token

    async def _repository_handle_auth_websocket(self, websocket: WebSocket, access_token: str) -> None:
        """..."""
        await websocket.accept()
        try:
            await websocket.send_json({"op": "waiting client answer"})
            user_id = await get_user_id_from_token(access_token)
            success = False
            while not success:
                receive_data = await websocket.receive_json()
                receive_user_id = receive_data.get("op")
                if receive_user_id == user_id:
                    user = await self._repository_find_user(receive_user_id)
                    if not user:
                        await websocket.send_json({"op": "user not found"})
                    else:
                        user_auth_token = await self._repository_get_user_auth_token(receive_user_id)
                        await websocket.send_json({"op": "access granted"})
                        await websocket.send_json({"op": f"user auth token: {user_auth_token}"})
                        await websocket.close(code=1000, reason=None)
                        success = True
                else:
                    await websocket.send_json({"op": "bad user id"})
        except Exception as exception:
            pass




