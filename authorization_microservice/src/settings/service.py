from dataclasses import dataclass

from src.settings.repository import BaseRepository


@dataclass
class BaseService(BaseRepository):
    """Сервис бд"""

    async def save_object(self, saved_object: object) -> None:
        """Сохранить объект в бд"""
        return await self._repository_save_object(saved_object)

    async def save_user_object(self, saved_object: object) -> None:
        """Сохранить объект в бд"""
        return await self._repository_save_user_object(saved_object)

    async def save_email_object(self, saved_object: object) -> None:
        """Сохранить объект в бд"""
        return await self._repository_save_email_object(saved_object)

    async def delete_object(self, deleted_object: object) -> None:
        """Удалить объект из бд"""
        return await self._repository_delete_object(deleted_object)

    async def delete_email_object(self, deleted_object: object) -> None:
        """Удалить объект из бд"""
        return await self._repository_delete_email_object(deleted_object)
