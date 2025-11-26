import pytest
import requests
import allure
from utils.urls import Urls
from data import HTTP_STATUS_CODES, DataOrder

class TestOrderCreation:

    @pytest.mark.parametrize("color_option", [["BLACK"], ["GREY"]])

    @allure.title("Успешное создание заказа")
    @allure.description("Можно выбрать один из цветов")
    def test_creating_order_one_any_colors(self, color_option):
        with allure.step("Подготовка данных заказа с одним цветом"):
            order_details = DataOrder.order_catalog.copy()
            order_details["color"] = color_option

        with allure.step(f"Отправка POST запроса на создание заказа с цветом {color_option}"):
            response = requests.post(
                f"{Urls.SCOOTER_PRAKTIKUM_URL}{Urls.CREATE_ORDER}", 
                json=order_details
            )

        with allure.step("Проверка успешного создания заказа"):
            assert response.status_code == HTTP_STATUS_CODES["CREATED"]
        
        with allure.step("Проверка что в ответе содержится track номер"):
            response_data = response.json()
            assert "track" in response_data
            assert isinstance(response_data["track"], int)


    @allure.title("Успешное создание заказа")
    @allure.description("Можно указать оба цвета")
    def test_create_order_with_both_colors(self):
        with allure.step("Подготовка данных заказа с двумя цветами"):
            order_details = DataOrder.order_catalog.copy()
            order_details["color"] = ["BLACK", "GREY"]

        with allure.step("Отправка POST запроса на создание заказа с двумя цветами"):
            response = requests.post(
                f"{Urls.SCOOTER_PRAKTIKUM_URL}{Urls.CREATE_ORDER}", 
                json=order_details
            )

        with allure.step("Проверка успешного создания заказа"):
            assert response.status_code == HTTP_STATUS_CODES["CREATED"]
        
        with allure.step("Проверка что в ответе содержится track номер"):
            response_data = response.json()
            assert "track" in response_data
            assert isinstance(response_data["track"], int)


    @allure.title("Успешное создание заказа")
    @allure.description("Цвет можно не выбирать")
    def test_create_order_without_color(self):
        with allure.step("Подготовка данных заказа без указания цвета"):
            order_details = DataOrder.order_catalog.copy()
            order_details["color"] = []

        with allure.step("Отправка POST запроса на создание заказа без цвета"):
            response = requests.post(
                f"{Urls.SCOOTER_PRAKTIKUM_URL}{Urls.CREATE_ORDER}", 
                json=order_details
            )

        with allure.step("Проверка успешного создания заказа"):
            assert response.status_code == HTTP_STATUS_CODES["CREATED"]
        
        with allure.step("Проверка, что в ответе содержится track номер"):
            response_data = response.json()
            assert "track" in response_data
            assert isinstance(response_data["track"], int)
