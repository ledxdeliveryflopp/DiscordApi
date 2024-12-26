from dataclasses import dataclass

from loguru import logger

from src.settings.database import async_session


@dataclass
class BaseRepository:

    @staticmethod
    async def _repository_save_object(new_object) -> None:
        try:
            async with async_session() as session:
                session.add(new_object)
                await session.commit()
                await session.refresh(new_object)
        except Exception as exc:
            await session.rollback()
            logger.info(f"Save error: {exc}")
