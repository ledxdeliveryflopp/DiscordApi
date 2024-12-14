from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class BaseRepository:
    """Репозиторий бд"""
    session: AsyncSession

    async def _repository_save_object(self, new_object: object) -> None:
        """Сохранить объект в бд"""
        try:
            self.session.add(new_object)
            await self.session.commit()
            await self.session.refresh(new_object)
        except Exception as exc:
            await self.session.rollback()

    async def _repository_delete_object(self, deleted_object: object) -> None:
        """Удалить объект из бд"""
        try:
            await self.session.delete(deleted_object)
            await self.session.commit()
        except Exception as exc:
            await self.session.rollback()
