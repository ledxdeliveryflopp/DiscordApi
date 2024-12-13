from fastapi import APIRouter, Depends
from starlette.websockets import WebSocket

from src.auth.service import AuthEventsService, init_auth_events_service

auth_events_router = APIRouter(prefix="/auth_events")


@auth_events_router.websocket("/qr_auth/")
async def router_handle_auth_websocket(client_id: str, websocket: WebSocket,
                                       service: AuthEventsService = Depends(init_auth_events_service)):
    return await service.handle_auth_websocket(websocket, client_id)
