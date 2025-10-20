import time
import pytest
import requests
import allure
from data import HTTP_STATUS_CODES
from utils.urls import Urls
from helpers import random_username, random_password, random_firstname

class TestCreatingCourier:

    @allure.title("Курьера можно создать")
    @allure.description("Проверяем создание нового курьера с уникальным логином, полученным через фикстуру courier_credentials")
    def test_courier_can_be_created(self, courier_credentials):
        # courier_credentials возвращает (login, password, first_name)
        login, password, first_name = courier_credentials
        unique_login = f"{login}_{int(time.time() * 1000)}"

        payload = {
            "login": unique_login,
            "password": password,
            "firstName": first_name
        }

        response = requests.post(
            f"{Urls.SCOOTER_PRAKTIKUM_URL}{Urls.COURIER_CREATE}",
            json=payload
        )

        with allure.step("Проверяем код ответа и тело"):
            assert response.status_code == HTTP_STATUS_CODES['CREATED']
            assert response.json() == {"ok": True}


    @allure.title('Проверяем невозможность создать двух идентичных курьеров')
    @allure.description('Используем фикстуру для создания нового курьера')
    def test_impossible_create_two_identical_couriers(self, courier_credentials: tuple[str, str, str]):

        with allure.step("Добавляем курьера"):
            login, password, first_name = courier_credentials
            payload = {
                "login": login,
                "password": password,
                "firstName": first_name
            }

        with allure.step("Добавляем дубликат курьера"):
            courier_duplicate = requests.post(
                f"{Urls.SCOOTER_PRAKTIKUM_URL}{Urls.COURIER_CREATE}",
                data=payload
            )

        with allure.step("Проверяем код ответа"):
            assert courier_duplicate.status_code == HTTP_STATUS_CODES['CONFLICT']
            
        with allure.step("Проверка наличия поля 'message' в теле ответа"):
            data = courier_duplicate.json()
            assert "message" in data


    @pytest.mark.parametrize("test_data", [
        {"password": random_password(), "firstName": random_firstname()},
        {"login": random_username(), "firstName": random_firstname()},
    ])
    @allure.title("Проверка валидации обязательных полей регистрации")
    @allure.description("Проверка отсутствия обязательных полей в данных регистрации")
    def test_validate_required_fields(self, test_data):

        with allure.step("Отправка запроса на создание курьера с неполными данными"):
            result = requests.post(
                f"{Urls.SCOOTER_PRAKTIKUM_URL}{Urls.COURIER_CREATE}",
                json=test_data
            )
            
        with allure.step("Проверка статуса ответа"):
            assert result.status_code == HTTP_STATUS_CODES['BAD_REQUEST']
           
        with allure.step("Проверка наличия поля 'message' в теле ответа"):
            data = result.json()
            assert "message" in data