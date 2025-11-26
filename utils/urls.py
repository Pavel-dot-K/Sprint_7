class Urls:

    # url ЯндексСамокат
    SCOOTER_PRAKTIKUM_URL = "http://qa-scooter.praktikum-services.ru/api/v1"

    # Эндпоинты для курьера
    COURIER_DELETE = "/courier/{id}"
    COURIER_CREATE = "/courier"
    COURIER_AUTHORIZATION = "/courier/login"

    # Эндпоинты для заказа
    CREATE_ORDER = "/orders"
    GET_ORDER_BY_TRACK = "/orders/track"
    GET_LIST_ORDERS = "/orders"