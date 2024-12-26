from dataclasses import dataclass

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket

from src.auth.repository import AuthEventsRepository
from src.settings.database import get_session, get_email_session


@dataclass
class AuthEventsService(AuthEventsRepository):

    async def handle_auth_websocket(self, websocket: WebSocket, client_id: str,  client_ip: str,
                                    client_type: str) -> None:
        return await self._repository_handle_auth_websocket(websocket, client_id, client_ip, client_type)


async def init_auth_events_service(session: AsyncSession = Depends(get_session),
                                   email_session: AsyncSession = Depends(get_email_session)):
    return AuthEventsService(session, email_session)
