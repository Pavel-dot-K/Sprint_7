from datetime import datetime, timedelta

HTTP_STATUS_CODES = {
    "SUCCESS": 200,
    "CREATED": 201,
    "BAD_REQUEST": 400,
    "NOT_FOUND": 404,
    "CONFLICT": 409
}

order_colors = [['BLACK'], ['GREY'], ['BLACK', 'GREY'], []]

class DataOrder:
    
    order_catalog = {
        "firstName": "Ivan",
        "lastName": "Ivanov",
        "address": "Lenina, 1",
        "metroStation": 4,
        "phone": "+7 999 999 99 99",
        "rentTime": 1,
        "deliveryDate": (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
        "comment": "Hello World"
    }
    
