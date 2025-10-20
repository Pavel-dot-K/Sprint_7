import pytest
import requests
import random
import string
import allure
from utils.urls import Urls

def generate_random_string(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))


@pytest.fixture

def courier_credentials():
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    url_create = f"{Urls.SCOOTER_PRAKTIKUM_URL}{Urls.COURIER_CREATE}"
    with allure.step("Создание курьера"):
        requests.post(url_create, json=payload, timeout=20)

        url_auth = f"{Urls.SCOOTER_PRAKTIKUM_URL}{Urls.COURIER_AUTHORIZATION}"
        auth_payload = {
            "login": login,
            "password": password
        }
    with allure.step("Авторизация курьера для получения ID"):
        auth_response = requests.post(url_auth, json=auth_payload, timeout=20)
        courier_id = auth_response.json().get("id")

        yield login, password, first_name

    with allure.step("Удаление тестового курьера после выполнения теста"):
        delete_url = f"{Urls.SCOOTER_PRAKTIKUM_URL}{Urls.COURIER_DELETE}{courier_id}"
        requests.delete(delete_url, timeout=20)


