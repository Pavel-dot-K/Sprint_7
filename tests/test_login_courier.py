import pytest
import json
import requests
import allure
from data import HTTP_STATUS_CODES
from utils.urls import Urls
from helpers import random_password, random_username


class TestLoginCourier:

    @allure.title("Авторизация несуществующего курьера")
    @allure.description("Проверяем, что авторизация несуществующего пользователя возвращает NOT_FOUND")
    def test_login_nonexistent_user(self):
        with allure.step("Генерация фиктивных учётных данных"):
            test_credentials = {
                "login": random_username(),
                "password": random_password()
            }

        with allure.step("Отправка запроса авторизации"):
            response = requests.post(
                f"{Urls.SCOOTER_PRAKTIKUM_URL}{Urls.COURIER_AUTHORIZATION}", 
                json=test_credentials
            )

        with allure.step("Проверка статуса ответа и тела"):
            assert response.status_code == HTTP_STATUS_CODES['NOT_FOUND']
            assert "message" in response.json()


    @allure.title("Авторизация под существующим курьером")
    @allure.description("Проверка успешной авторизации существующего курьера")
    def test_courier_can_login(self, courier_credentials):
        # courier_credentials возвращает (login, password, first_name)
        login, password, _ = courier_credentials

        auth_payload = {
            "login": login,
            "password": password
        }

        with allure.step("Формирование payload авторизации"):
            payload = auth_payload

        with allure.step("Отправка запроса авторизации"):
            response = requests.post(
                f"{Urls.SCOOTER_PRAKTIKUM_URL}{Urls.COURIER_AUTHORIZATION}",
                json=payload
            )

        with allure.step("Проверка кода ответа"):
            assert response.status_code == HTTP_STATUS_CODES['SUCCESS']

        with allure.step("Проверка структуры ответа и типа id"):
            data = response.json()
            assert "id" in data and isinstance(data["id"], int)


    @pytest.mark.parametrize(
        "base_payload, extra_payload",
        [
            ({"password": "qwer_pass"}, {"login": ""}),
            ({"login": "qwer_name"}, {"password": ""}),
     ]
    )
    @allure.title("Валидация обязательных полей авторизации курьера")
    @allure.description("Проверяем невозможность регистрации курьера, если одно из полей незаполненно.")
    def test_validate_auth_required_fields(self, base_payload, extra_payload):
        # Формируем итоговый payload из двух частей
        payload = {**base_payload, **extra_payload}

        with allure.step("Подготовка payload для авторизации"):
                allure.attach(
                json.dumps(payload, ensure_ascii=False),
                name="payload",
                attachment_type=allure.attachment_type.JSON
            )

        url = f"{Urls.SCOOTER_PRAKTIKUM_URL}{Urls.COURIER_AUTHORIZATION}"

        with allure.step("Отправка запроса на авторизацию курьера"):
            response = requests.post(url, json=payload, timeout=20)

        with allure.step("Проверка, что статус ответа не равен SUCCESS"):
            assert response.status_code != HTTP_STATUS_CODES['SUCCESS']  # или 200 если константа не доступна

        with allure.step("Проверка наличия поля 'message' в теле ответа"):
            data = response.json()
            assert "message" in data


    @pytest.mark.parametrize('invalid_field, field_value_generator', [
        ("login", random_username),
        ("password", random_password),
    ])

    @allure.title("Неверный ввод даных при авторизации курьера.")
    @allure.description("Проверем невозможность авторизации при вводе некоректных данных.")
    def test_invalid_credentials_login(self, courier_credentials, invalid_field, field_value_generator):
        # courier_credentials возвращает (login, password, first_name)
        login, password, _ = courier_credentials

        auth_payload = {
            "login": login,
            "password": password
        }

        modified_payload = auth_payload.copy()
        modified_payload[invalid_field] = field_value_generator()

        with allure.step(f"Проверка авторизации с неверными данными"):
            response = requests.post(
                f"{Urls.SCOOTER_PRAKTIKUM_URL}{Urls.COURIER_AUTHORIZATION}",
                json=modified_payload
            )

        with allure.step("Проверка, что статус не равен SUCCESS"):
            assert response.status_code != HTTP_STATUS_CODES['SUCCESS']

        with allure.step("Проверка наличия поля 'message' в теле ответа"):
            data = response.json()
            assert "message" in data