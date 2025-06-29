"""
Интеграционные тесты для API endpoints
Тестируем HTTP endpoints с моками базы данных
"""

import unittest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from datetime import datetime
from bson import ObjectId

from app.main import app


class TestUserAPI(unittest.TestCase):
    """Интеграционные тесты для User API endpoints"""

    def setUp(self):
        """Настройка тестового клиента"""
        self.client = TestClient(app)
        self.user_data = {
            "name": "Test User"
        }

    @patch('app.routes.user_routes.users_collection')
    def test_create_user_success(self, mock_collection):
        """Тест успешного создания пользователя через API"""
        mock_result = AsyncMock()
        mock_result.inserted_id = 123
        mock_collection.insert_one = AsyncMock(return_value=mock_result)
        
        # Мокаем read_user_by_id для возврата созданного пользователя
        user_doc = {
            "_id": 123,
            "name": "Test User",
            "gender": None,
            "language": None,
            "recommendation_method": None,
            "launch_count": 0,
            "current_bundle_version": None,
            "bundle_version_at_install": None
        }
        mock_collection.find_one = AsyncMock(return_value=user_doc)

        response = self.client.post("/users/", json=self.user_data)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "Test User")

    @patch('app.routes.user_routes.users_collection')
    def test_create_user_invalid_data(self, mock_collection):
        """Тест создания пользователя с невалидными данными через API"""
        response = self.client.post("/users/", json={"name": ""})
        
        self.assertEqual(response.status_code, 422)

    @patch('app.routes.user_routes.users_collection')
    def test_read_user_found(self, mock_collection):
        """Тест чтения существующего пользователя через API"""
        user_doc = {
            "_id": 123,
            "name": "Test User",
            "gender": "male",
            "language": "en",
            "recommendation_method": "cf",
            "launch_count": 5,
            "current_bundle_version": 1,
            "bundle_version_at_install": 1
        }
        mock_collection.find_one = AsyncMock(return_value=user_doc)

        response = self.client.get("/users/123")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "Test User")

    @patch('app.routes.user_routes.users_collection')
    def test_read_user_not_found(self, mock_collection):
        """Тест чтения несуществующего пользователя через API"""
        mock_collection.find_one = AsyncMock(return_value=None)

        response = self.client.get("/users/999")
        
        self.assertEqual(response.status_code, 404)
        self.assertIn("User not found", response.json()["detail"])

    @patch('app.routes.user_routes.users_collection')
    def test_update_user_success(self, mock_collection):
        """Тест успешного обновления пользователя через API"""
        mock_result = AsyncMock()
        mock_result.modified_count = 1
        mock_collection.replace_one = AsyncMock(return_value=mock_result)

        response = self.client.put("/users/123", json=self.user_data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json())

    @patch('app.routes.user_routes.users_collection')
    def test_update_user_not_found(self, mock_collection):
        """Тест обновления несуществующего пользователя через API"""
        mock_result = AsyncMock()
        mock_result.modified_count = 0
        mock_collection.replace_one = AsyncMock(return_value=mock_result)

        response = self.client.put("/users/999", json=self.user_data)
        
        self.assertEqual(response.status_code, 404)
        self.assertIn("User not updated", response.json()["detail"])

    @patch('app.routes.user_routes.users_collection')
    def test_delete_user_success(self, mock_collection):
        """Тест успешного удаления пользователя через API"""
        mock_result = AsyncMock()
        mock_result.deleted_count = 1
        mock_collection.delete_one = AsyncMock(return_value=mock_result)

        response = self.client.delete("/users/123")
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json())

    @patch('app.routes.user_routes.users_collection')
    def test_delete_user_not_found(self, mock_collection):
        """Тест удаления несуществующего пользователя через API"""
        mock_result = AsyncMock()
        mock_result.deleted_count = 0
        mock_collection.delete_one = AsyncMock(return_value=mock_result)

        response = self.client.delete("/users/999")
        
        self.assertEqual(response.status_code, 404)
        self.assertIn("User not found", response.json()["detail"])


class TestConversationAPI(unittest.TestCase):
    """Интеграционные тесты для Conversation API endpoints"""

    def setUp(self):
        """Настройка тестового клиента"""
        self.client = TestClient(app)
        self.conv_data = {
            "user_id": 123,
            "messages": []
        }

    @patch('app.routes.conv_routes.conversations_collection')
    def test_create_conversation_success(self, mock_collection):
        """Тест успешного создания беседы через API"""
        mock_result = AsyncMock()
        mock_result.inserted_id = ObjectId()
        mock_collection.insert_one = AsyncMock(return_value=mock_result)
        
        # Мокаем read_conv для возврата созданной беседы
        conv_doc = {
            "_id": ObjectId(),
            "user_id": 123,
            "messages": []
        }
        mock_collection.find_one = AsyncMock(return_value=conv_doc)

        response = self.client.post("/conversations/", json=self.conv_data)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("_id", data)

    @patch('app.routes.conv_routes.conversations_collection')
    def test_read_conversation_found(self, mock_collection):
        """Тест чтения существующей беседы через API"""
        conv_doc = {
            "_id": ObjectId(),
            "user_id": 123,
            "messages": []
        }
        mock_collection.find_one = AsyncMock(return_value=conv_doc)

        response = self.client.get(f"/conversations/{str(ObjectId())}")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["user_id"], 123)

    @patch('app.routes.conv_routes.conversations_collection')
    def test_read_conversation_not_found(self, mock_collection):
        """Тест чтения несуществующей беседы через API"""
        mock_collection.find_one = AsyncMock(return_value=None)

        response = self.client.get(f"/conversations/{str(ObjectId())}")
        
        self.assertEqual(response.status_code, 404)
        self.assertIn("Conversation not found", response.json()["detail"])

    @patch('app.routes.conv_routes.conversations_collection')
    def test_add_message_success(self, mock_collection):
        """Тест успешного добавления сообщения через API"""
        mock_result = AsyncMock()
        mock_result.modified_count = 1
        mock_collection.update_one = AsyncMock(return_value=mock_result)

        message_data = {
            "sender": "user",
            "text": "Hello",
            "time": datetime.now().isoformat()
        }

        response = self.client.post(f"/conversations/{str(ObjectId())}/messages", json=message_data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json())

    @patch('app.routes.conv_routes.conversations_collection')
    def test_get_user_conversations(self, mock_collection):
        """Тест получения бесед пользователя через API"""
        convs = [
            {"_id": ObjectId(), "user_id": 123, "messages": []},
            {"_id": ObjectId(), "user_id": 123, "messages": []}
        ]
        mock_cursor = AsyncMock()
        mock_cursor.to_list.return_value = convs
        mock_collection.find.return_value = mock_cursor

        response = self.client.get("/conversations/user/123")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)


class TestLogAPI(unittest.TestCase):
    """Интеграционные тесты для Log API endpoints"""

    def setUp(self):
        """Настройка тестового клиента"""
        self.client = TestClient(app)
        self.log_data = {
            "user_id": 123,
            "activity_id": "test_activity",
            "type": "test_type",
            "start_time": datetime.now().isoformat(),
            "completion_time": datetime.now().isoformat()
        }

    @patch('app.routes.log_routes.logs_collection')
    def test_create_log_success(self, mock_collection):
        """Тест успешного создания лога через API"""
        mock_result = AsyncMock()
        mock_result.inserted_id = ObjectId()
        mock_collection.insert_one = AsyncMock(return_value=mock_result)
        
        # Мокаем read_log для возврата созданного лога
        log_doc = {
            "_id": ObjectId(),
            "user_id": 123,
            "activity_id": "test_activity",
            "type": "test_type",
            "start_time": datetime.now(),
            "completion_time": datetime.now()
        }
        mock_collection.find_one = AsyncMock(return_value=log_doc)

        response = self.client.post("/logs/", json=self.log_data)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("_id", data)

    @patch('app.routes.log_routes.logs_collection')
    def test_read_log_found(self, mock_collection):
        """Тест чтения существующего лога через API"""
        log_doc = {
            "_id": ObjectId(),
            "user_id": 123,
            "activity_id": "test_activity",
            "type": "test_type",
            "start_time": datetime.now(),
            "completion_time": datetime.now()
        }
        mock_collection.find_one = AsyncMock(return_value=log_doc)

        response = self.client.get(f"/logs/{str(ObjectId())}")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["user_id"], 123)

    @patch('app.routes.log_routes.logs_collection')
    def test_update_log_success(self, mock_collection):
        """Тест успешного обновления лога через API"""
        mock_result = AsyncMock()
        mock_result.modified_count = 1
        mock_collection.replace_one = AsyncMock(return_value=mock_result)

        response = self.client.put(f"/logs/{str(ObjectId())}", json=self.log_data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json())

    @patch('app.routes.log_routes.logs_collection')
    def test_delete_log_success(self, mock_collection):
        """Тест успешного удаления лога через API"""
        mock_result = AsyncMock()
        mock_result.deleted_count = 1
        mock_collection.delete_one = AsyncMock(return_value=mock_result)

        response = self.client.delete(f"/logs/{str(ObjectId())}")
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json())


class TestRootEndpoint(unittest.TestCase):
    """Интеграционные тесты для корневого endpoint"""

    def setUp(self):
        """Настройка тестового клиента"""
        self.client = TestClient(app)

    def test_root_endpoint(self):
        """Тест корневого endpoint"""
        response = self.client.get("/")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["message"], "API is running")


if __name__ == '__main__':
    unittest.main() 