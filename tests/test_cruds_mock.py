import pytest
from unittest.mock import AsyncMock, Mock
from bson import ObjectId
from datetime import datetime

from app.cruds.user_crud import create_user, read_user_by_id, update_user_by_id, delete_user_by_id
from app.cruds.conv_crud import create_conv, create_message, read_conv, read_user_conv, update_conv, delete_conv
from app.cruds.log_crud import create_log, read_log, update_log, delete_log
from app.models.user import UserDB
from app.models.conv import ConversationIn, Message
from app.models.log import LogIn


class TestUserCRUDMock:
    """Mock tests for user crud"""

    @pytest.mark.asyncio
    async def test_create_user_success(self):
        mock_collection = AsyncMock()
        user = UserDB(name="John Doe")
        user.id = 123
        
        result = await create_user(mock_collection, user)
        
        assert result == 123
        mock_collection.insert_one.assert_called_once()
        
        call_args = mock_collection.insert_one.call_args[0][0]
        assert call_args["name"] == "John Doe"
        assert call_args["_id"] == 123

    @pytest.mark.asyncio
    async def test_read_user_by_id_found(self):
        mock_collection = AsyncMock()
        user_doc = {
            "_id": 123,
            "name": "John Doe",
            "gender": "male",
            "language": "ru"
        }
        mock_collection.find_one.return_value = user_doc
        
        result = await read_user_by_id(mock_collection, 123)
        
        assert result == user_doc
        mock_collection.find_one.assert_called_once_with({"_id": 123})

    @pytest.mark.asyncio
    async def test_read_user_by_id_not_found(self):
        mock_collection = AsyncMock()
        mock_collection.find_one.return_value = None
        
        result = await read_user_by_id(mock_collection, 999)
        
        assert result is None
        mock_collection.find_one.assert_called_once_with({"_id": 999})

    @pytest.mark.asyncio
    async def test_update_user_by_id_success(self):
        mock_collection = AsyncMock()
        mock_result = AsyncMock()
        mock_result.modified_count = 1
        mock_collection.replace_one.return_value = mock_result
        
        user = UserDB(name="Updated Name")
        user.id = 123
        
        result = await update_user_by_id(mock_collection, 123, user)
        
        assert result is True
        mock_collection.replace_one.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_user_by_id_not_found(self):
        mock_collection = AsyncMock()
        mock_result = AsyncMock()
        mock_result.modified_count = 0
        mock_collection.replace_one.return_value = mock_result
        
        user = UserDB(name="Updated Name")
        user.id = 123
        
        result = await update_user_by_id(mock_collection, 999, user)
        
        assert result is False
        mock_collection.replace_one.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_user_by_id_success(self):
        mock_collection = AsyncMock()
        mock_result = AsyncMock()
        mock_result.deleted_count = 1
        mock_collection.delete_one.return_value = mock_result
        
        result = await delete_user_by_id(mock_collection, 123)
        
        assert result is True
        mock_collection.delete_one.assert_called_once_with({"_id": 123})

    @pytest.mark.asyncio
    async def test_delete_user_by_id_not_found(self):
        mock_collection = AsyncMock()
        mock_result = AsyncMock()
        mock_result.deleted_count = 0
        mock_collection.delete_one.return_value = mock_result
        
        result = await delete_user_by_id(mock_collection, 999)
        
        assert result is False
        mock_collection.delete_one.assert_called_once_with({"_id": 999})


class TestConversationCRUDMock:
    """Mock tests for conv crud"""

    @pytest.mark.asyncio
    async def test_create_conv_success(self):
        mock_collection = AsyncMock()
        mock_result = AsyncMock()
        mock_result.inserted_id = ObjectId()
        mock_collection.insert_one.return_value = mock_result
        
        conv = ConversationIn(user_id=123, messages=[])
        
        result = await create_conv(mock_collection, conv)
        
        assert isinstance(result, str)
        assert result == str(mock_result.inserted_id)
        mock_collection.insert_one.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_message_success(self):
        mock_collection = AsyncMock()
        mock_result = AsyncMock()
        mock_result.modified_count = 1
        mock_collection.update_one.return_value = mock_result
        
        message = Message(sender="user", text="Hello", time=datetime.now())
        conv_id = str(ObjectId())
        
        result = await create_message(mock_collection, conv_id, message)
        
        assert result is True
        mock_collection.update_one.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_message_invalid_id(self):
        mock_collection = AsyncMock()
        message = Message(sender="user", text="Hello", time=datetime.now())
        
        result = await create_message(mock_collection, "invalid_id", message)
        
        assert result is False
        mock_collection.update_one.assert_not_called()

    @pytest.mark.asyncio
    async def test_read_conv_found(self):
        mock_collection = AsyncMock()
        conv_doc = {
            "_id": ObjectId(),
            "user_id": 123,
            "messages": []
        }
        mock_collection.find_one.return_value = conv_doc
        
        conv_id = str(ObjectId())
        result = await read_conv(mock_collection, conv_id)
        
        assert result == conv_doc
        mock_collection.find_one.assert_called_once()

    @pytest.mark.asyncio
    async def test_read_conv_not_found(self):
        mock_collection = AsyncMock()
        mock_collection.find_one.return_value = None
        
        conv_id = str(ObjectId())
        result = await read_conv(mock_collection, conv_id)
        
        assert result is None
        mock_collection.find_one.assert_called_once()

    @pytest.mark.asyncio
    async def test_read_conv_invalid_id(self):
        mock_collection = AsyncMock()
        
        result = await read_conv(mock_collection, "invalid_id")
        
        assert result is None
        mock_collection.find_one.assert_not_called()

    @pytest.mark.asyncio
    async def test_read_user_conv(self):
        from unittest.mock import Mock
        mock_collection = Mock()
        convs = [
            {"_id": ObjectId(), "user_id": 123, "messages": []},
            {"_id": ObjectId(), "user_id": 123, "messages": []}
        ]
        mock_cursor = AsyncMock()
        mock_cursor.to_list.return_value = convs
        mock_collection.find.return_value = mock_cursor
        
        result = await read_user_conv(mock_collection, 123)
        
        assert result == convs
        mock_collection.find.assert_called_once_with({"user_id": 123})
        mock_cursor.to_list.assert_called_once_with(length=100)

    @pytest.mark.asyncio
    async def test_update_conv_success(self):
        mock_collection = AsyncMock()
        mock_result = AsyncMock()
        mock_result.modified_count = 1
        mock_collection.replace_one.return_value = mock_result
        
        conv = ConversationIn(user_id=123, messages=[])
        conv_id = str(ObjectId())
        
        result = await update_conv(mock_collection, conv_id, conv)
        
        assert result is True
        mock_collection.replace_one.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_conv_invalid_id(self):
        mock_collection = AsyncMock()
        conv = ConversationIn(user_id=123, messages=[])
        
        result = await update_conv(mock_collection, "invalid_id", conv)
        
        assert result is False
        mock_collection.replace_one.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_conv_success(self):
        mock_collection = AsyncMock()
        mock_result = AsyncMock()
        mock_result.deleted_count = 1
        mock_collection.delete_one.return_value = mock_result
        
        conv_id = str(ObjectId())
        result = await delete_conv(mock_collection, conv_id)
        
        assert result is True
        mock_collection.delete_one.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_conv_invalid_id(self):
        mock_collection = AsyncMock()
        
        result = await delete_conv(mock_collection, "invalid_id")
        
        assert result is False
        mock_collection.delete_one.assert_not_called()


class TestLogCRUDMock:
    """Mock tests for log crud"""

    @pytest.mark.asyncio
    async def test_create_log_success(self):
        mock_collection = AsyncMock()
        mock_result = AsyncMock()
        mock_result.inserted_id = ObjectId()
        mock_collection.insert_one.return_value = mock_result
        
        log = LogIn(
            user_id=123,
            activity_id="test_activity",
            type="test_type",
            start_time=datetime.now(),
            completion_time=datetime.now()
        )
        
        result = await create_log(mock_collection, log)
        
        assert isinstance(result, str)
        assert result == str(mock_result.inserted_id)
        mock_collection.insert_one.assert_called_once()

    @pytest.mark.asyncio
    async def test_read_log_found(self):
        mock_collection = AsyncMock()
        log_doc = {
            "_id": ObjectId(),
            "user_id": 123,
            "activity_id": "test_activity",
            "type": "test_type"
        }
        mock_collection.find_one.return_value = log_doc
        
        log_id = str(ObjectId())
        result = await read_log(mock_collection, log_id)
        
        assert result == log_doc
        mock_collection.find_one.assert_called_once()

    @pytest.mark.asyncio
    async def test_read_log_not_found(self):
        mock_collection = AsyncMock()
        mock_collection.find_one.return_value = None
        
        log_id = str(ObjectId())
        result = await read_log(mock_collection, log_id)
        
        assert result is None
        mock_collection.find_one.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_log_success(self):
        mock_collection = AsyncMock()
        mock_result = AsyncMock()
        mock_result.modified_count = 1
        mock_collection.replace_one.return_value = mock_result
        
        log = LogIn(
            user_id=123,
            activity_id="test_activity",
            type="test_type",
            start_time=datetime.now(),
            completion_time=datetime.now()
        )
        log_id = str(ObjectId())
        
        result = await update_log(mock_collection, log_id, log)
        
        assert result == 1
        mock_collection.replace_one.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_log_success(self):
        mock_collection = AsyncMock()
        mock_result = AsyncMock()
        mock_result.deleted_count = 1
        mock_collection.delete_one.return_value = mock_result
        
        log_id = str(ObjectId())
        result = await delete_log(mock_collection, log_id)
        
        assert result == 1
        mock_collection.delete_one.assert_called_once() 