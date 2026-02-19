"""
Тесты для PostmanEcho API
"""

import pytest
import requests
import json
from datetime import datetime

BASE_URL = "https://postman-echo.com"


class TestPostmanEchoAPI:

    def test_1_get_basic_request(self):
        """
        Тест 1: Базовый GET запрос
        """

        # Отправляем GET запрос как в Postman
        response = requests.get(f"{BASE_URL}/get")

        # Проверяем статус код (в Postman видим 200 OK)
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

        # JSON ответ
        data = response.json()
        print(f"Ответ сервера: {json.dumps(data, indent=2)}")

        # Проверяем структуру ответа как наблюдали в Postman
        assert "args" in data, "В ответе отсутствует поле 'args'"
        assert "headers" in data, "В ответе отсутствует поле 'headers'"
        assert "url" in data, "В ответе отсутствует поле 'url'"

        # Проверяем, что URL соответствует ожидаемому
        assert data["url"] == f"{BASE_URL}/get", f"URL не совпадает: {data['url']}"

        # Проверяем наличие стандартных заголовков как в Postman
        assert "host" in data["headers"], "В заголовках отсутствует 'host'"
        assert data["headers"]["host"] == "postman-echo.com", "Неверный host"


    def test_2_get_with_query_parameters(self):
        """
        Тест 2: GET запрос с query-параметрами
        Как тестировали в Postman с параметрами name, age, city
        """

        # Параметры как в Postman тестировании
        params = {
            "name": "John",
            "age": "30",
            "city": "New York",
            "is_active": "true"
        }

        # Отправляем запрос с параметрами
        response = requests.get(f"{BASE_URL}/get", params=params)

        assert response.status_code == 200
        data = response.json()

        # Проверяем, что параметры вернулись в args
        assert data["args"]["name"] == "John"
        assert data["args"]["age"] == "30"
        assert data["args"]["city"] == "New York"
        assert data["args"]["is_active"] == "true"

        # Проверяем, что URL содержит параметры
        expected_url = f"{BASE_URL}/get?name=John&age=30&city=New+York&is_active=true"
        assert data["url"] == expected_url, f"URL не совпадает:\nОжидалось: {expected_url}\nПолучено: {data['url']}"


    def test_3_post_with_json_body(self):
        """
        Тест 3: POST запрос с JSON телом
        Как тестировали в Postman с raw JSON
        """

        # JSON данные как в Postman
        json_data = {
            "user": "test_user",
            "password": "secure_password_123",
            "active": True,
            "roles": ["admin", "editor", "viewer"],
            "metadata": {
                "created_at": "2024-01-15",
                "last_login": None
            },
            "balance": 1500.75
        }

        # Отправляем POST с JSON телом
        headers = {"Content-Type": "application/json"}
        response = requests.post(f"{BASE_URL}/post", json=json_data, headers=headers)

        assert response.status_code == 200
        data = response.json()
        print(f"Отправленный JSON: {json.dumps(json_data, indent=2)}")
        print(f"Полученный JSON в ответе: {json.dumps(data['json'], indent=2)}")

        # Проверяем структуру ответа как в Postman
        assert "json" in data, "В ответе отсутствует поле 'json'"
        assert "data" in data, "В ответе отсутствует поле 'data'"
        assert "headers" in data, "В ответе отсутствует поле 'headers'"

        # Проверяем, что JSON данные вернулись корректно
        assert data["json"]["user"] == "test_user"
        assert data["json"]["password"] == "secure_password_123"
        assert data["json"]["active"] is True
        assert len(data["json"]["roles"]) == 3
        assert data["json"]["metadata"]["created_at"] == "2024-01-15"
        assert data["json"]["balance"] == 1500.75

        # Проверяем заголовок Content-Type как в Postman
        assert "application/json" in data["headers"]["content-type"]


    def test_4_post_with_form_data(self):
        """
        Тест 4: POST запрос с form-data
        Как тестировали в Postman с form-data
        """

        # Form-data как в Postman
        form_data = {
            "username": "jane_doe",
            "email": "jane@example.com",
            "subscribe": "true",
            "newsletter_frequency": "weekly",
            "interests": "technology,sports,music"  # В form-data это будет строкой
        }

        # Отправляем POST с form-data
        response = requests.post(f"{BASE_URL}/post", data=form_data)

        assert response.status_code == 200
        data = response.json()
        print(f"Отправленные form-data: {form_data}")
        print(f"Полученные form данные: {json.dumps(data['form'], indent=2)}")

        # Проверяем структуру ответа как в Postman
        assert "form" in data, "В ответе отсутствует поле 'form'"
        assert "files" in data, "В ответе отсутствует поле 'files'"

        # Проверяем, что form-data вернулись корректно
        assert data["form"]["username"] == "jane_doe"
        assert data["form"]["email"] == "jane@example.com"
        assert data["form"]["subscribe"] == "true"
        assert data["form"]["newsletter_frequency"] == "weekly"
        assert data["form"]["interests"] == "technology,sports,music"

        # Проверяем Content-Type заголовок
        assert "application/x-www-form-urlencoded" in data["headers"]["content-type"]


    def test_5_put_request_with_json(self):
        """
        Тест 6: PUT запрос с JSON телом
        """

        json_data = {
            "id": 456,
            "action": "update",
            "fields": {
                "name": "Updated Name",
                "status": "active"
            },
            "timestamp": datetime.now().isoformat()
        }

        response = requests.put(f"{BASE_URL}/put", json=json_data)

        assert response.status_code == 200
        data = response.json()

        assert data["json"]["id"] == 456
        assert data["json"]["action"] == "update"
        assert data["json"]["fields"]["name"] == "Updated Name"
        assert data["url"] == f"{BASE_URL}/put"



    def test_6_delete_request(self):
        """
        Тест 7: DELETE запрос
        """

        response = requests.delete(f"{BASE_URL}/delete")

        assert response.status_code == 200
        data = response.json()

        # Проверяем структуру ответа для DELETE
        assert "args" in data
        assert "headers" in data
        assert data["url"] == f"{BASE_URL}/delete"



    def test_7_get_with_special_characters(self):
        """
        Тест 8: GET запрос со специальными символами в параметрах
        """

        params = {
            "search": "test & data",
            "price": "100$",
            "email": "test@example.com",
            "message": "Hello, World!",
            "unicode": "тест русский текст"
        }

        response = requests.get(f"{BASE_URL}/get", params=params)

        assert response.status_code == 200
        data = response.json()

        # Проверяем, что специальные символы корректно переданы
        assert data["args"]["search"] == "test & data"
        assert data["args"]["price"] == "100$"
        assert data["args"]["email"] == "test@example.com"
        assert data["args"]["message"] == "Hello, World!"
        assert data["args"]["unicode"] == "тест русский текст"

