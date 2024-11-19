import httpx
import pytest


@pytest.mark.directly
class TestDirectlyUserRouter:
    """Тестирование отправки запросов напрямую"""
    url: str = "http://localhost:7000/users/"

    async def test_success_register(self) -> None:
        """Успешная регистрация"""
        async with httpx.AsyncClient() as client:
            data = {"username": "TestUser", "email": "testuser@gmail.com",
                    "description": "test description",
                    "status": "test status",
                    "password": "testpassword"}
            headers = {'Accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'}
            request = await client.post(f'{self.url}register/', json=data, headers=headers)
            assert request.status_code == 200
            assert request.json() == {"detail": "success"}

    async def test_register_duplicate(self) -> None:
        """Регистрации дубликата"""
        async with httpx.AsyncClient() as client:
            data = {"username": "TestUser", "email": "testuser@gmail.com",
                    "description": "test description",
                    "status": "test status",
                    "password": "testpassword"}
            headers = {'Accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'}
            request = await client.post(f'{self.url}register/', json=data, headers=headers)
            assert request.status_code == 400
            assert request.json() == {"detail": "User already exist."}

    async def test_register_big_username(self) -> None:
        """Регистрация с слишком большим username"""
        async with httpx.AsyncClient() as client:
            data = {"username": "TestUser123134авафывафсафыасыфасафапвап", "email": "testuser@gmail.com",
                    "description": "test description",
                    "status": "test status",
                    "password": "testpassword"}
            headers = {'Accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'}
            request = await client.post(f'{self.url}register/', json=data, headers=headers)
            assert request.status_code == 422
            username = data.get("username")
            assert request.json() == {"detail":[{"type":"string_too_long","loc":["body","username"],
                                                 "msg":"String should have at most 20 characters",
                                                 "input":f"{username}",
                                                 "ctx":{"max_length":20}}]}

    async def test_success_find_user_by_username(self) -> None:
        """Успешный поиск пользователя по username"""
        async with httpx.AsyncClient() as client:
            request = await client.get('http://localhost:7000/users/user/?username=TestUser')
            data = request.json()
            for i in data:
                user_id = i.get("id")
            assert request.status_code == 200
            assert request.json() == [{"id": user_id, "username": "TestUser", "avatar_url": None}]

    async def test_dont_find_user_by_username(self) -> None:
        """Поиск не существующего пользователя"""
        async with httpx.AsyncClient() as client:
            request = await client.get('http://localhost:7000/users/user/?username=TestUserFailed')
            assert request.status_code == 404
            assert request.json() == {"detail": "User dont exist."}
