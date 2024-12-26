from dataclasses import dataclass

from src.settings.repository import BaseRepository


@dataclass
class BaseService(BaseRepository):

    async def save_object(self, new_object) -> None:
        return await self._repository_save_object(new_object)


base_service = BaseService()
