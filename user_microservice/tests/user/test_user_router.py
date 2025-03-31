import datetime
import allure
from allure_commons.types import LabelType
from pytest_mock import MockerFixture

from src.user.models import UserModel
from user.const import MockerPathConst


@allure.feature('Тестирование эндпоинтов микросервиса пользователей')
class TestUserRouter:
    png_file = {"avatar_file": ("test.png", b"image data", "image/png")}
    mocked_user = UserModel(username="ledx", email="korstim18@gmail.com", avatar_url="test.url", description="test",
                            status="test", country="ru", password="resrwr", clients_fingerprints=[], id=1,
                            created_at=datetime.datetime.now())

    @allure.title("Получение информации о юзере по username(Пользователь найден)")
    @allure.label(LabelType.LANGUAGE, "python")
    @allure.label(LabelType.FRAMEWORK, "pytest")
    @allure.tag("users")
    async def test_get_user_info_router_success(self, client, mocker: MockerFixture):
        mocker.patch(f"{MockerPathConst.UserRepositoryPath}._repository_find_user_by_username").return_value = [self.mocked_user]
        with allure.step('Отправка запроса на uri - users/user/?username=ledx'):
            response = client.get("users/user/?username=ledx")
        with allure.step(f"Ожидаемый код - 200, Полученный код - {response.status_code}"):
            assert response.status_code == 200
        with allure.step("Проверка тела ответа"):
            assert response.json() == [{'id': 1, 'username': 'ledx', 'avatar_url': 'test.url'}]

    @allure.title("Получение информации о юзере по username(Пользователь не найден)")
    @allure.label(LabelType.LANGUAGE, "python")
    @allure.label(LabelType.FRAMEWORK, "pytest")
    @allure.tag("users")
    async def test_get_user_info_router_error(self, client, mocker: MockerFixture):
        mocker.patch(f"{MockerPathConst.UserRepositoryPath}._repository_find_user_by_username").return_value = None
        with allure.step('Отправка запроса на uri - users/user/?username=ledx'):
            response = client.get("users/user/?username=ledx")
        with allure.step(f"Ожидаемый код - 404, Полученный код - {response.status_code}"):
            assert response.status_code == 404
        with allure.step("Проверка тела ответа"):
            assert response.json() == {"detail": "User dont exist."}

    @allure.title("Загрузка аватарки пользователю(Успешно)")
    @allure.label(LabelType.LANGUAGE, "python")
    @allure.label(LabelType.FRAMEWORK, "pytest")
    @allure.tag("users")
    async def test_upload_avatar_success(self, client, mocker: MockerFixture):
        mocker.patch(f"{MockerPathConst.UserRepositoryPath}._repository_get_user_by_token").return_value = self.mocked_user
        mocker.patch(f"{MockerPathConst.S3ServicePath}._S3Service__get_url_to_file_in_s3").return_value = "test_avatar.s3.com"
        mocker.patch(f"{MockerPathConst.S3ServicePath}.upload_file_in_s3").return_value = "test_avatar.s3.com"
        with allure.step('Отправка запроса на uri - users/upload-avatar/'):
            response = client.patch("users/upload-avatar/", files=self.png_file,
                                    headers={"Authorization": "test_token"})
        with allure.step(f"Ожидаемый код - 200, Полученный код - {response.status_code}"):
            assert response.status_code == 200
        with allure.step("Проверка тела ответа"):
            assert response.json() == {"Detail": "success"}
