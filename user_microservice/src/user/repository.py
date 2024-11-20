from dataclasses import dataclass
from typing import Any, Sequence

from sqlalchemy import Select, Result, CursorResult, Row, RowMapping

from src.settings.service import BaseService
from src.user.models import UserModel


@dataclass
class UserRepository(BaseService):
    """Репозиторий пользователей"""

    async def _repository_find_user_by_email(self, email: str) -> Result | CursorResult:
        """Поиск пользователя по email"""
        user = await self.session.execute(Select(UserModel).where(UserModel.email == email))
        return user.scalar()

    async def _repository_find_user_by_username(self, username: str) -> Sequence[Row[Any] | RowMapping | Any]:
        """Поиск пользователя по username"""
        user = await self.session.execute(Select(UserModel).where(UserModel.username == username))
        return user.scalars().all()
