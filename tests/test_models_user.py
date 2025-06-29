import pytest
from datetime import datetime
from app.models.user import UserIn, UserDB, UserOut


class TestUserIn:
    """Tests for UserIn"""

    def test_user_in_valid_with_id(self):
        user = UserIn(_id=123, name="John Doe")
        assert user.id == 123
        assert user.name == "John Doe"

    def test_user_in_valid_without_id(self):
        user = UserIn(name="John Doe")
        assert user.id is None
        assert user.name == "John Doe"

    def test_user_in_invalid_name_empty(self):
        with pytest.raises(ValueError):
            UserIn(name="")

    def test_user_in_invalid_name_too_long(self):
        with pytest.raises(ValueError):
            UserIn(name="a" * 51)

    def test_user_in_name_exactly_max_length(self):
        user = UserIn(name="a" * 50)
        assert user.name == "a" * 50

    def test_user_in_name_min_length(self):
        user = UserIn(name="a")
        assert user.name == "a"

    def test_user_in_model_dump(self):
        user = UserIn(_id=123, name="John Doe")
        data = user.model_dump()
        assert data["id"] == 123
        assert data["name"] == "John Doe"

    def test_user_in_model_dump_by_alias(self):
        user = UserIn(_id=123, name="John Doe")
        data = user.model_dump(by_alias=True)
        assert data["_id"] == 123
        assert data["name"] == "John Doe"


class TestUserDB:
    """Tests for Userdb"""

    def test_user_db_valid_full(self):
        user = UserDB(
            name="John Doe",
            gender="male",
            language="ru",
            recommendation_method="fixed",
            launch_count=5,
            current_bundle_version=1,
            bundle_version_at_install=1
        )
        assert user.name == "John Doe"
        assert user.gender == "male"
        assert user.language == "ru"
        assert user.recommendation_method == "fixed"
        assert user.launch_count == 5
        assert user.current_bundle_version == 1
        assert user.bundle_version_at_install == 1

    def test_user_db_valid_minimal(self):
        user = UserDB(name="John Doe")
        assert user.name == "John Doe"
        assert user.gender is None
        assert user.language is None
        assert user.recommendation_method is None
        assert user.launch_count == 0
        assert user.current_bundle_version is None
        assert user.bundle_version_at_install is None

    def test_user_db_valid_gender_male(self):
        user = UserDB(name="John Doe", gender="male")
        assert user.gender == "male"

    def test_user_db_valid_gender_female(self):
        user = UserDB(name="John Doe", gender="female")
        assert user.gender == "female"

    def test_user_db_valid_language_ru(self):
        user = UserDB(name="John Doe", language="ru")
        assert user.language == "ru"

    def test_user_db_valid_language_en(self):
        user = UserDB(name="John Doe", language="en")
        assert user.language == "en"

    def test_user_db_valid_recommendation_methods(self):
        methods = ["fixed", "kb", "cf"]
        for method in methods:
            user = UserDB(name="John Doe", recommendation_method=method)
            assert user.recommendation_method == method

    def test_user_db_launch_count_default(self):
        user = UserDB(name="John Doe")
        assert user.launch_count == 0

    def test_user_db_launch_count_custom(self):
        user = UserDB(name="John Doe", launch_count=10)
        assert user.launch_count == 10

    def test_user_db_negative_launch_count(self):
        user = UserDB(name="John Doe", launch_count=-5)
        assert user.launch_count == -5

    def test_user_db_model_dump_exclude_unset(self):
        user = UserDB(name="John Doe")
        data = user.model_dump(exclude_unset=True)
        assert "name" in data
        assert "gender" not in data
        assert "language" not in data

    def test_user_db_model_dump_by_alias(self):
        user = UserDB(_id=123, name="John Doe")
        data = user.model_dump(by_alias=True)
        assert data["_id"] == 123
        assert data["name"] == "John Doe"

    def test_user_db_from_user_in(self):
        user_in = UserIn(name="John Doe")
        user_db = UserDB(**user_in.model_dump())
        assert user_db.name == "John Doe"
        assert user_db.launch_count == 0


class TestUserOut:
    """Tests for UserOut"""

    def test_user_out_inheritance(self):
        user_db = UserDB(
            name="John Doe",
            gender="male",
            language="ru",
            recommendation_method="fixed",
            launch_count=5
        )
        user_out = UserOut(**user_db.model_dump())
        assert user_out.name == "John Doe"
        assert user_out.gender == "male"
        assert user_out.language == "ru"
        assert user_out.recommendation_method == "fixed"
        assert user_out.launch_count == 5

    def test_user_out_serialization(self):
        user_out = UserOut(
            name="John Doe",
            gender="male",
            language="ru",
            recommendation_method="fixed",
            launch_count=5
        )
        data = user_out.model_dump()
        assert data["name"] == "John Doe"
        assert data["gender"] == "male"


class TestUserModelIntegration:
    """Integration tests for user model"""

    def test_user_workflow(self):
        user_in = UserIn(name="John Doe")
        assert user_in.name == "John Doe"
        assert user_in.id is None

        user_db = UserDB(**user_in.model_dump())
        user_db.id = 123
        user_db.gender = "male"
        user_db.language = "ru"
        assert user_db.id == 123
        assert user_db.name == "John Doe"
        assert user_db.gender == "male"

        user_out = UserOut(**user_db.model_dump())
        assert user_out.id == 123
        assert user_out.name == "John Doe"
        assert user_out.gender == "male"

    def test_user_validation_chain(self):
        with pytest.raises(ValueError):
            UserIn(name="")

    def test_user_edge_cases(self):
        user = UserIn(name="a" * 50)
        assert len(user.name) == 50

        user = UserIn(name="a")
        assert len(user.name) == 1

        user = UserDB(name="John Doe", launch_count=0)
        assert user.launch_count == 0

        user = UserDB(name="John Doe", launch_count=-1)
        assert user.launch_count == -1 