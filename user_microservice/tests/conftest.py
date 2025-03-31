from unittest.mock import Mock

import allure
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.testclient import TestClient

from src.settings.database import get_session


@allure.step("Импорт приложения FASTAPI")
@pytest.fixture(scope="session")
def app_session():
    from main import user_app

    return user_app


@pytest.fixture
async def session_mock():
    return Mock(name="db_session_mock", spec_set=AsyncSession)


@pytest.fixture
def app(app_session, session_mock):

    app_session.dependency_overrides[get_session] = lambda: session_mock

    return app_session


@pytest.fixture
def client(app):
    with TestClient(app) as client:
        yield client
