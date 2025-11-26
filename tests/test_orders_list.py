import requests
import allure
from data import HTTP_STATUS_CODES
from utils.urls import Urls


class TestOrdersList:

    @allure.title("Список заказов.")
    @allure.description("Проверем невозможность получения списка заказов.")
    def test_available_orders_list(self):
        with allure.step("Отправляем запрос для получения списка заказов"):
            response = requests.get(f"{Urls.SCOOTER_PRAKTIKUM_URL}{Urls.GET_LIST_ORDERS}")

        with allure.step("Проверка что запрос выполнен успешно"):
            assert response.status_code == HTTP_STATUS_CODES["SUCCESS"]

        with allure.step("Проверка структуры ответа"):
            response_data = response.json()
            assert "orders" in response_data
            assert isinstance(response_data["orders"], list)

   