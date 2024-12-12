from dataclasses import dataclass

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket

from src.auth.repository import AuthEventsRepository
from src.settings.database import get_session


@dataclass
class AuthEventsService(AuthEventsRepository):

    async def handle_auth_websocket(self, websocket: WebSocket, access_token: str) -> None:
        return await self._repository_handle_auth_websocket(websocket, access_token)


async def init_auth_events_service(session: AsyncSession = Depends(get_session)):
    return AuthEventsService(session)
