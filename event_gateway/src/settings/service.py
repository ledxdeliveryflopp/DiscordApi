from dataclasses import dataclass

from src.settings.repository import BaseRepository


@dataclass
class BaseService(BaseRepository):
    """Сервис бд"""

    async def save_object(self, new_object: object) -> None:
        """Сохранить объект в бд"""
        return await self._repository_save_object(new_object)

    async def delete_object(self, deleted_object: object) -> None:
        """Удалить объект из бд"""
        return await self._repository_delete_object(deleted_object)

    async def delete_confirmation_code(self, deleted_object: object) -> None:
        """Удалить объект из бд"""
        return await self._repository_delete_confirmation_code(deleted_object)
