"""
Полные тесты для Conversation моделей
Тестируем валидацию, создание и преобразование данных
"""

import pytest
from datetime import datetime
from bson import ObjectId
from app.models.conv import Message, ConversationIn, ConversationDB, ConversationOut, PyObjectId


class TestMessage:
    """Тесты для модели Message"""

    def test_message_valid_user(self):
        """Тест создания сообщения от пользователя"""
        time = datetime.now()
        message = Message(sender="user", text="Hello", time=time)
        assert message.sender == "user"
        assert message.text == "Hello"
        assert message.time == time

    def test_message_valid_bot(self):
        """Тест создания сообщения от бота"""
        time = datetime.now()
        message = Message(sender="bot", text="Hi there!", time=time)
        assert message.sender == "bot"
        assert message.text == "Hi there!"
        assert message.time == time

    def test_message_empty_text(self):
        """Тест создания сообщения с пустым текстом"""
        with pytest.raises(ValueError):
            Message(sender="user", text="", time=datetime.now())

    def test_message_text_min_length(self):
        """Тест создания сообщения с текстом минимальной длины"""
        message = Message(sender="user", text="a", time=datetime.now())
        assert message.text == "a"

    def test_message_text_long(self):
        """Тест создания сообщения с длинным текстом"""
        long_text = "a" * 1000
        message = Message(sender="user", text=long_text, time=datetime.now())
        assert message.text == long_text

    def test_message_model_dump(self):
        """Тест сериализации сообщения"""
        time = datetime.now()
        message = Message(sender="user", text="Hello", time=time)
        data = message.model_dump()
        assert data["sender"] == "user"
        assert data["text"] == "Hello"
        assert data["time"] == time

    def test_message_model_dump_by_alias(self):
        """Тест сериализации сообщения с алиасами"""
        time = datetime.now()
        message = Message(sender="user", text="Hello", time=time)
        data = message.model_dump(by_alias=True)
        assert data["sender"] == "user"
        assert data["text"] == "Hello"
        assert data["time"] == time


class TestConversationIn:
    """Тесты для модели ConversationIn"""

    def test_conversation_in_valid_empty_messages(self):
        """Тест создания беседы с пустым списком сообщений"""
        conv = ConversationIn(user_id=123, messages=[])
        assert conv.user_id == 123
        assert conv.messages == []

    def test_conversation_in_valid_with_messages(self):
        """Тест создания беседы с сообщениями"""
        messages = [
            Message(sender="user", text="Hello", time=datetime.now()),
            Message(sender="bot", text="Hi!", time=datetime.now())
        ]
        conv = ConversationIn(user_id=123, messages=messages)
        assert conv.user_id == 123
        assert len(conv.messages) == 2
        assert conv.messages[0].sender == "user"
        assert conv.messages[1].sender == "bot"

    def test_conversation_in_default_messages(self):
        """Тест создания беседы без указания сообщений"""
        conv = ConversationIn(user_id=123)
        assert conv.user_id == 123
        assert conv.messages == []

    def test_conversation_in_negative_user_id(self):
        """Тест создания беседы с отрицательным user_id"""
        conv = ConversationIn(user_id=-123, messages=[])
        assert conv.user_id == -123

    def test_conversation_in_zero_user_id(self):
        """Тест создания беседы с нулевым user_id"""
        conv = ConversationIn(user_id=0, messages=[])
        assert conv.user_id == 0

    def test_conversation_in_model_dump(self):
        """Тест сериализации беседы"""
        conv = ConversationIn(user_id=123, messages=[])
        data = conv.model_dump()
        assert data["user_id"] == 123
        assert data["messages"] == []

    def test_conversation_in_model_dump_with_messages(self):
        """Тест сериализации беседы с сообщениями"""
        messages = [
            Message(sender="user", text="Hello", time=datetime.now())
        ]
        conv = ConversationIn(user_id=123, messages=messages)
        data = conv.model_dump()
        assert data["user_id"] == 123
        assert len(data["messages"]) == 1
        assert data["messages"][0]["sender"] == "user"


class TestPyObjectId:
    """Тесты для PyObjectId"""

    def test_py_object_id_create(self):
        """Тест создания PyObjectId"""
        oid = PyObjectId()
        assert isinstance(oid, ObjectId)

    def test_py_object_id_validate_valid_string(self):
        """Тест валидации корректной строки ObjectId"""
        original_oid = ObjectId()
        oid_str = str(original_oid)
        validated_oid = PyObjectId.validate(oid_str)
        assert isinstance(validated_oid, ObjectId)
        assert validated_oid == original_oid

    def test_py_object_id_validate_object_id(self):
        """Тест валидации ObjectId объекта"""
        original_oid = ObjectId()
        validated_oid = PyObjectId.validate(original_oid)
        assert isinstance(validated_oid, ObjectId)
        assert validated_oid == original_oid

    def test_py_object_id_validate_invalid_string(self):
        """Тест валидации неверной строки"""
        with pytest.raises(ValueError):
            PyObjectId.validate("invalid_id")

    def test_py_object_id_validate_empty_string(self):
        """Тест валидации пустой строки"""
        with pytest.raises(ValueError):
            PyObjectId.validate("")

    def test_py_object_id_validate_short_string(self):
        """Тест валидации короткой строки"""
        with pytest.raises(ValueError):
            PyObjectId.validate("123")

    def test_py_object_id_validate_long_string(self):
        """Тест валидации длинной строки"""
        with pytest.raises(ValueError):
            PyObjectId.validate("a" * 100)


class TestConversationDB:
    """Тесты для модели ConversationDB"""

    def test_conversation_db_valid(self):
        """Тест создания ConversationDB"""
        conv = ConversationDB(user_id=123, messages=[])
        assert conv.user_id == 123
        assert conv.messages == []
        assert isinstance(conv.id, ObjectId)

    def test_conversation_db_with_messages(self):
        """Тест создания ConversationDB с сообщениями"""
        messages = [
            Message(sender="user", text="Hello", time=datetime.now())
        ]
        conv = ConversationDB(user_id=123, messages=messages)
        assert conv.user_id == 123
        assert len(conv.messages) == 1
        assert isinstance(conv.id, ObjectId)

    def test_conversation_db_model_dump(self):
        """Тест сериализации ConversationDB"""
        conv = ConversationDB(user_id=123, messages=[])
        data = conv.model_dump()
        assert data["user_id"] == 123
        assert data["messages"] == []
        assert "id" in data

    def test_conversation_db_model_dump_by_alias(self):
        """Тест сериализации ConversationDB с алиасами"""
        conv = ConversationDB(user_id=123, messages=[])
        data = conv.model_dump(by_alias=True)
        assert data["user_id"] == 123
        assert data["messages"] == []
        assert "_id" in data

    def test_conversation_db_from_conversation_in(self):
        """Тест создания ConversationDB из ConversationIn"""
        conv_in = ConversationIn(user_id=123, messages=[])
        conv_db = ConversationDB(**conv_in.model_dump())
        assert conv_db.user_id == 123
        assert conv_db.messages == []
        assert isinstance(conv_db.id, ObjectId)


class TestConversationOut:
    """Тесты для модели ConversationOut"""

    def test_conversation_out_valid(self):
        """Тест создания ConversationOut"""
        conv = ConversationOut(user_id=123, messages=[])
        assert conv.user_id == 123
        assert conv.messages == []

    def test_conversation_out_with_messages(self):
        """Тест создания ConversationOut с сообщениями"""
        messages = [
            Message(sender="user", text="Hello", time=datetime.now())
        ]
        conv = ConversationOut(user_id=123, messages=messages)
        assert conv.user_id == 123
        assert len(conv.messages) == 1

    def test_conversation_out_model_dump(self):
        """Тест сериализации ConversationOut"""
        conv = ConversationOut(user_id=123, messages=[])
        data = conv.model_dump()
        assert data["user_id"] == 123
        assert data["messages"] == []

    def test_conversation_out_from_conversation_db(self):
        """Тест создания ConversationOut из ConversationDB"""
        conv_db = ConversationDB(user_id=123, messages=[])
        conv_data = conv_db.model_dump()
        conv_data["id"] = str(conv_data["id"])
        conv_out = ConversationOut(**conv_data)
        assert conv_out.user_id == 123
        assert conv_out.messages == []


class TestConversationModelIntegration:
    """Интеграционные тесты для Conversation моделей"""

    def test_conversation_workflow(self):
        """Тест полного workflow создания беседы"""
        # 1. Создаем сообщения
        message1 = Message(sender="user", text="Hello", time=datetime.now())
        message2 = Message(sender="bot", text="Hi!", time=datetime.now())
        
        # 2. Создаем ConversationIn
        conv_in = ConversationIn(user_id=123, messages=[message1, message2])
        assert conv_in.user_id == 123
        assert len(conv_in.messages) == 2
        
        # 3. Создаем ConversationDB
        conv_db = ConversationDB(**conv_in.model_dump())
        assert conv_db.user_id == 123
        assert len(conv_db.messages) == 2
        assert isinstance(conv_db.id, ObjectId)
        
        # 4. Создаем ConversationOut
        conv_data = conv_db.model_dump()
        conv_data["id"] = str(conv_data["id"])
        conv_out = ConversationOut(**conv_data)
        assert conv_out.user_id == 123
        assert len(conv_out.messages) == 2

    def test_conversation_validation_chain(self):
        """Тест цепочки валидации"""
        # Проверяем валидацию сообщений
        with pytest.raises(ValueError):
            Message(sender="user", text="", time=datetime.now())

    def test_conversation_edge_cases(self):
        """Тест граничных случаев"""
        # Беседа с большим количеством сообщений
        messages = [
            Message(sender="user", text=f"Message {i}", time=datetime.now())
            for i in range(100)
        ]
        conv = ConversationIn(user_id=123, messages=messages)
        assert len(conv.messages) == 100
        
        # Беседа с очень длинным текстом
        long_text = "a" * 10000
        message = Message(sender="user", text=long_text, time=datetime.now())
        assert len(message.text) == 10000

    def test_conversation_serialization_chain(self):
        """Тест цепочки сериализации"""
        # Создаем беседу
        messages = [
            Message(sender="user", text="Hello", time=datetime.now())
        ]
        conv_in = ConversationIn(user_id=123, messages=messages)
        
        # Сериализуем
        data = conv_in.model_dump()
        assert data["user_id"] == 123
        assert len(data["messages"]) == 1
        
        # Десериализуем
        conv_db = ConversationDB(**data)
        assert conv_db.user_id == 123
        assert len(conv_db.messages) == 1
        
        # Сериализуем с алиасами
        data_with_alias = conv_db.model_dump(by_alias=True)
        assert "_id" in data_with_alias 