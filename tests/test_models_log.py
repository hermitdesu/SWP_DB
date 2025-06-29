
import pytest
from datetime import datetime
from bson import ObjectId
from app.models.log import LogIn, LogDB, LogOut, PyObjectId


class TestLogIn:
    """Tests for LogIn"""

    def test_log_in_valid(self):
        start_time = datetime.now()
        completion_time = datetime.now()
        log = LogIn(
            user_id=123, 
            activity_id="test_activity",
            type="test_type",
            start_time=start_time,
            completion_time=completion_time
        )
        assert log.user_id == 123
        assert log.activity_id == "test_activity"
        assert log.type == "test_type"
        assert log.value is None
        assert log.start_time == start_time
        assert log.completion_time == completion_time
        assert log.build_version is None

    def test_log_in_with_optional_fields(self):
        start_time = datetime.now()
        completion_time = datetime.now()
        log = LogIn(
            user_id=123,
            activity_id="test_activity",
            type="test_type",
            value="test_value",
            start_time=start_time,
            completion_time=completion_time,
            build_version="1.0.0"
        )
        assert log.user_id == 123
        assert log.activity_id == "test_activity"
        assert log.type == "test_type"
        assert log.value == "test_value"
        assert log.start_time == start_time
        assert log.completion_time == completion_time
        assert log.build_version == "1.0.0"

    def test_log_in_negative_user_id(self):
        start_time = datetime.now()
        completion_time = datetime.now()
        log = LogIn(
            user_id=-123,
            activity_id="test_activity",
            type="test_type",
            start_time=start_time,
            completion_time=completion_time
        )
        assert log.user_id == -123

    def test_log_in_zero_user_id(self):
        start_time = datetime.now()
        completion_time = datetime.now()
        log = LogIn(
            user_id=0,
            activity_id="test_activity",
            type="test_type",
            start_time=start_time,
            completion_time=completion_time
        )
        assert log.user_id == 0

    def test_log_in_empty_type(self):
        start_time = datetime.now()
        completion_time = datetime.now()
        with pytest.raises(ValueError):
            LogIn(
                user_id=123,
                activity_id="test_activity",
                type="",
                start_time=start_time,
                completion_time=completion_time
            )

    def test_log_in_long_type(self):
        start_time = datetime.now()
        completion_time = datetime.now()
        long_type = "a" * 50
        log = LogIn(
            user_id=123,
            activity_id="test_activity",
            type=long_type,
            start_time=start_time,
            completion_time=completion_time
        )
        assert log.type == long_type

    def test_log_in_type_min_length(self):
        start_time = datetime.now()
        completion_time = datetime.now()
        log = LogIn(
            user_id=123,
            activity_id="test_activity",
            type="a",
            start_time=start_time,
            completion_time=completion_time
        )
        assert log.type == "a"

    def test_log_in_model_dump(self):
        start_time = datetime.now()
        completion_time = datetime.now()
        log = LogIn(
            user_id=123,
            activity_id="test_activity",
            type="test_type",
            value="test_value",
            start_time=start_time,
            completion_time=completion_time,
            build_version="1.0.0"
        )
        data = log.model_dump()
        assert data["user_id"] == 123
        assert data["activity_id"] == "test_activity"
        assert data["type"] == "test_type"
        assert data["value"] == "test_value"
        assert data["start_time"] == start_time
        assert data["completion_time"] == completion_time
        assert data["build_version"] == "1.0.0"

    def test_log_in_model_dump_by_alias(self):
        start_time = datetime.now()
        completion_time = datetime.now()
        log = LogIn(
            user_id=123,
            activity_id="test_activity",
            type="test_type",
            start_time=start_time,
            completion_time=completion_time
        )
        data = log.model_dump(by_alias=True)
        assert data["user_id"] == 123
        assert data["activity_id"] == "test_activity"
        assert data["type"] == "test_type"


class TestLogDB:
    """Tests for LogDB"""

    def test_log_db_valid(self):
        start_time = datetime.now()
        completion_time = datetime.now()
        log = LogDB(
            user_id=123,
            activity_id="test_activity",
            type="test_type",
            start_time=start_time,
            completion_time=completion_time
        )
        assert log.user_id == 123
        assert log.activity_id == "test_activity"
        assert log.type == "test_type"
        assert log.value is None
        assert log.start_time == start_time
        assert log.completion_time == completion_time
        assert log.build_version is None
        assert isinstance(log.id, ObjectId)

    def test_log_db_with_optional_fields(self):
        start_time = datetime.now()
        completion_time = datetime.now()
        log = LogDB(
            user_id=123,
            activity_id="test_activity",
            type="test_type",
            value="test_value",
            start_time=start_time,
            completion_time=completion_time,
            build_version="1.0.0"
        )
        assert log.user_id == 123
        assert log.activity_id == "test_activity"
        assert log.type == "test_type"
        assert log.value == "test_value"
        assert log.start_time == start_time
        assert log.completion_time == completion_time
        assert log.build_version == "1.0.0"
        assert isinstance(log.id, ObjectId)

    def test_log_db_model_dump(self):
        start_time = datetime.now()
        completion_time = datetime.now()
        log = LogDB(
            user_id=123,
            activity_id="test_activity",
            type="test_type",
            value="test_value",
            start_time=start_time,
            completion_time=completion_time,
            build_version="1.0.0"
        )
        data = log.model_dump()
        assert data["user_id"] == 123
        assert data["activity_id"] == "test_activity"
        assert data["type"] == "test_type"
        assert data["value"] == "test_value"
        assert data["start_time"] == start_time
        assert data["completion_time"] == completion_time
        assert data["build_version"] == "1.0.0"
        assert "id" in data

    def test_log_db_model_dump_by_alias(self):
        start_time = datetime.now()
        completion_time = datetime.now()
        log = LogDB(
            user_id=123,
            activity_id="test_activity",
            type="test_type",
            start_time=start_time,
            completion_time=completion_time
        )
        data = log.model_dump(by_alias=True)
        assert data["user_id"] == 123
        assert data["activity_id"] == "test_activity"
        assert data["type"] == "test_type"
        assert "_id" in data

    def test_log_db_from_log_in(self):
        start_time = datetime.now()
        completion_time = datetime.now()
        log_in = LogIn(
            user_id=123,
            activity_id="test_activity",
            type="test_type",
            value="test_value",
            start_time=start_time,
            completion_time=completion_time,
            build_version="1.0.0"
        )
        log_db = LogDB(**log_in.model_dump())
        assert log_db.user_id == 123
        assert log_db.activity_id == "test_activity"
        assert log_db.type == "test_type"
        assert log_db.value == "test_value"
        assert log_db.start_time == start_time
        assert log_db.completion_time == completion_time
        assert log_db.build_version == "1.0.0"
        assert isinstance(log_db.id, ObjectId)

    def test_log_db_exclude_unset(self):
        start_time = datetime.now()
        completion_time = datetime.now()
        log = LogDB(
            user_id=123,
            activity_id="test_activity",
            type="test_type",
            start_time=start_time,
            completion_time=completion_time
        )
        data = log.model_dump(exclude_unset=True)
        assert "user_id" in data
        assert "activity_id" in data
        assert "type" in data
        assert "start_time" in data
        assert "completion_time" in data
        assert "value" not in data
        assert "build_version" not in data


class TestLogOut:
    """Tests fof LogOut"""

    def test_log_out_valid(self):
        start_time = datetime.now()
        completion_time = datetime.now()
        log = LogOut(
            user_id=123,
            activity_id="test_activity",
            type="test_type",
            start_time=start_time,
            completion_time=completion_time
        )
        assert log.user_id == 123
        assert log.activity_id == "test_activity"
        assert log.type == "test_type"
        assert log.value is None
        assert log.start_time == start_time
        assert log.completion_time == completion_time
        assert log.build_version is None

    def test_log_out_with_optional_fields(self):
        start_time = datetime.now()
        completion_time = datetime.now()
        log = LogOut(
            user_id=123,
            activity_id="test_activity",
            type="test_type",
            value="test_value",
            start_time=start_time,
            completion_time=completion_time,
            build_version="1.0.0"
        )
        assert log.user_id == 123
        assert log.activity_id == "test_activity"
        assert log.type == "test_type"
        assert log.value == "test_value"
        assert log.start_time == start_time
        assert log.completion_time == completion_time
        assert log.build_version == "1.0.0"

    def test_log_out_model_dump(self):
        start_time = datetime.now()
        completion_time = datetime.now()
        log = LogOut(
            user_id=123,
            activity_id="test_activity",
            type="test_type",
            value="test_value",
            start_time=start_time,
            completion_time=completion_time,
            build_version="1.0.0"
        )
        data = log.model_dump()
        assert data["user_id"] == 123
        assert data["activity_id"] == "test_activity"
        assert data["type"] == "test_type"
        assert data["value"] == "test_value"
        assert data["start_time"] == start_time
        assert data["completion_time"] == completion_time
        assert data["build_version"] == "1.0.0"

    def test_log_out_from_log_db(self):
        start_time = datetime.now()
        completion_time = datetime.now()
        log_db = LogDB(
            user_id=123,
            activity_id="test_activity",
            type="test_type",
            value="test_value",
            start_time=start_time,
            completion_time=completion_time,
            build_version="1.0.0"
        )
        log_data = log_db.model_dump()
        log_data["id"] = str(log_data["id"])
        log_out = LogOut(**log_data)
        assert log_out.user_id == 123
        assert log_out.activity_id == "test_activity"
        assert log_out.type == "test_type"
        assert log_out.value == "test_value"
        assert log_out.start_time == start_time
        assert log_out.completion_time == completion_time
        assert log_out.build_version == "1.0.0"


class TestLogModelIntegration:
    """Integration tests for log models"""

    def test_log_workflow(self):
        start_time = datetime.now()
        completion_time = datetime.now()
        
        log_in = LogIn(
            user_id=123,
            activity_id="test_activity",
            type="test_type",
            value="test_value",
            start_time=start_time,
            completion_time=completion_time,
            build_version="1.0.0"
        )
        assert log_in.user_id == 123
        assert log_in.activity_id == "test_activity"
        assert log_in.type == "test_type"
        assert log_in.value == "test_value"
        
        log_db = LogDB(**log_in.model_dump())
        assert log_db.user_id == 123
        assert log_db.activity_id == "test_activity"
        assert log_db.type == "test_type"
        assert log_db.value == "test_value"
        assert isinstance(log_db.id, ObjectId)
        

        log_data = log_db.model_dump()
        log_data["id"] = str(log_data["id"])
        log_out = LogOut(**log_data)
        assert log_out.user_id == 123
        assert log_out.activity_id == "test_activity"
        assert log_out.type == "test_type"
        assert log_out.value == "test_value"

    def test_log_validation_chain(self):
        start_time = datetime.now()
        completion_time = datetime.now()
        

        with pytest.raises(ValueError):
            LogIn(
                user_id=123,
                activity_id="test_activity",
                type="",
                start_time=start_time,
                completion_time=completion_time
            )

    def test_log_edge_cases(self):
        start_time = datetime.now()
        completion_time = datetime.now()
     
        long_type = "a" * 50
        log = LogIn(
            user_id=123,
            activity_id="test_activity",
            type=long_type,
            start_time=start_time,
            completion_time=completion_time
        )
        assert len(log.type) == 50
        

        log = LogIn(
            user_id=0,
            activity_id="test_activity",
            type="test_type",
            start_time=start_time,
            completion_time=completion_time
        )
        assert log.user_id == 0
        
        log = LogIn(
            user_id=-1,
            activity_id="test_activity",
            type="test_type",
            start_time=start_time,
            completion_time=completion_time
        )
        assert log.user_id == -1

    def test_log_serialization_chain(self):
        start_time = datetime.now()
        completion_time = datetime.now()
        
        log_in = LogIn(
            user_id=123,
            activity_id="test_activity",
            type="test_type",
            value="test_value",
            start_time=start_time,
            completion_time=completion_time,
            build_version="1.0.0"
        )
        
        data = log_in.model_dump()
        assert data["user_id"] == 123
        assert data["activity_id"] == "test_activity"
        assert data["type"] == "test_type"
        assert data["value"] == "test_value"
        
        log_db = LogDB(**data)
        assert log_db.user_id == 123
        assert log_db.activity_id == "test_activity"
        assert log_db.type == "test_type"
        assert log_db.value == "test_value"
        
        data_with_alias = log_db.model_dump(by_alias=True)
        assert "_id" in data_with_alias

    def test_log_different_types(self):
        start_time = datetime.now()
        completion_time = datetime.now()
        
        types = [
            "user_login",
            "user_logout", 
            "conversation_start",
            "conversation_end",
            "message_sent",
            "message_received",
            "error_occurred",
            "system_event"
        ]
        
        for log_type in types:
            log = LogIn(
                user_id=123,
                activity_id="test_activity",
                type=log_type,
                start_time=start_time,
                completion_time=completion_time
            )
            assert log.type == log_type

    def test_log_value_types(self):
        start_time = datetime.now()
        completion_time = datetime.now()
        
        log = LogIn(
            user_id=123,
            activity_id="test_activity",
            type="test",
            value="simple string",
            start_time=start_time,
            completion_time=completion_time
        )
        assert log.value == "simple string"

        log = LogIn(
            user_id=123,
            activity_id="test_activity",
            type="test",
            start_time=start_time,
            completion_time=completion_time
        )
        assert log.value is None

    def test_log_time_validation(self):
        start_time = datetime.now()
        completion_time = datetime.now()
        
        log = LogIn(
            user_id=123,
            activity_id="test_activity",
            type="test_type",
            start_time=start_time,
            completion_time=completion_time
        )
        assert log.start_time == start_time
        assert log.completion_time == completion_time 