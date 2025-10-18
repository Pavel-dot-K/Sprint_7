import pytest
import requests
import random
import string
import allure
from utils.urls import Urls


@pytest.fixture
def courier_credentials():
    def generate_random_string(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    with allure.step("Создание курьера"):
        response = requests.post(
            f"{Urls.SCOOTER_PRAKTIKUM_URL}{Urls.COURIER_CREATE}",
            json=payload
        )
        assert response.status_code == 201, "Не удалось создать курьера"

    with allure.step("Авторизация курьера для получения ID"):
        auth_payload = {
            "login": login,
            "password": password
        }
        auth_response = requests.post(
            f"{Urls.SCOOTER_PRAKTIKUM_URL}{Urls.COURIER_AUTHORIZATION}",
            json=auth_payload
        )
        assert auth_response.status_code == 200, "Не удалось авторизовать курьера"

    courier_id = auth_response.json().get("id")

    yield login, password, first_name

    with allure.step("Удаление тестового курьера после выполнения теста"):
        if courier_id:
            delete_url = f"{Urls.SCOOTER_PRAKTIKUM_URL}{Urls.COURIER_DELETE}{courier_id}"
            requests.delete(delete_url)


