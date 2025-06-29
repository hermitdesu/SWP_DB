"""
Полные тесты для User моделей
Тестируем валидацию, создание и преобразование данных
"""

import pytest
from datetime import datetime
from app.models.user import UserIn, UserDB, UserOut


class TestUserIn:
    """Тесты для модели UserIn"""

    def test_user_in_valid_with_id(self):
        """Тест создания пользователя с ID"""
        user = UserIn(_id=123, name="John Doe")
        assert user.id == 123
        assert user.name == "John Doe"

    def test_user_in_valid_without_id(self):
        """Тест создания пользователя без ID"""
        user = UserIn(name="John Doe")
        assert user.id is None
        assert user.name == "John Doe"

    def test_user_in_invalid_name_empty(self):
        """Тест создания пользователя с пустым именем"""
        with pytest.raises(ValueError):
            UserIn(name="")

    def test_user_in_invalid_name_too_long(self):
        """Тест создания пользователя с именем слишком длинным"""
        with pytest.raises(ValueError):
            UserIn(name="a" * 51)  # Имя длиннее 50 символов

    def test_user_in_name_exactly_max_length(self):
        """Тест создания пользователя с именем максимальной длины"""
        user = UserIn(name="a" * 50)
        assert user.name == "a" * 50

    def test_user_in_name_min_length(self):
        """Тест создания пользователя с именем минимальной длины"""
        user = UserIn(name="a")
        assert user.name == "a"

    def test_user_in_model_dump(self):
        """Тест сериализации модели"""
        user = UserIn(_id=123, name="John Doe")
        data = user.model_dump()
        assert data["id"] == 123
        assert data["name"] == "John Doe"

    def test_user_in_model_dump_by_alias(self):
        """Тест сериализации модели с алиасами"""
        user = UserIn(_id=123, name="John Doe")
        data = user.model_dump(by_alias=True)
        assert data["_id"] == 123
        assert data["name"] == "John Doe"


class TestUserDB:
    """Тесты для модели UserDB"""

    def test_user_db_valid_full(self):
        """Тест создания полного пользователя"""
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
        """Тест создания минимального пользователя"""
        user = UserDB(name="John Doe")
        assert user.name == "John Doe"
        assert user.gender is None
        assert user.language is None
        assert user.recommendation_method is None
        assert user.launch_count == 0
        assert user.current_bundle_version is None
        assert user.bundle_version_at_install is None

    def test_user_db_valid_gender_male(self):
        """Тест создания пользователя с полом male"""
        user = UserDB(name="John Doe", gender="male")
        assert user.gender == "male"

    def test_user_db_valid_gender_female(self):
        """Тест создания пользователя с полом female"""
        user = UserDB(name="John Doe", gender="female")
        assert user.gender == "female"

    def test_user_db_valid_language_ru(self):
        """Тест создания пользователя с языком ru"""
        user = UserDB(name="John Doe", language="ru")
        assert user.language == "ru"

    def test_user_db_valid_language_en(self):
        """Тест создания пользователя с языком en"""
        user = UserDB(name="John Doe", language="en")
        assert user.language == "en"

    def test_user_db_valid_recommendation_methods(self):
        """Тест создания пользователя с разными методами рекомендаций"""
        methods = ["fixed", "kb", "cf"]
        for method in methods:
            user = UserDB(name="John Doe", recommendation_method=method)
            assert user.recommendation_method == method

    def test_user_db_launch_count_default(self):
        """Тест значения по умолчанию для launch_count"""
        user = UserDB(name="John Doe")
        assert user.launch_count == 0

    def test_user_db_launch_count_custom(self):
        """Тест установки пользовательского значения launch_count"""
        user = UserDB(name="John Doe", launch_count=10)
        assert user.launch_count == 10

    def test_user_db_negative_launch_count(self):
        """Тест отрицательного значения launch_count"""
        user = UserDB(name="John Doe", launch_count=-5)
        assert user.launch_count == -5

    def test_user_db_model_dump_exclude_unset(self):
        """Тест сериализации с исключением неустановленных полей"""
        user = UserDB(name="John Doe")
        data = user.model_dump(exclude_unset=True)
        assert "name" in data
        assert "gender" not in data
        assert "language" not in data

    def test_user_db_model_dump_by_alias(self):
        """Тест сериализации с алиасами"""
        user = UserDB(_id=123, name="John Doe")
        data = user.model_dump(by_alias=True)
        assert data["_id"] == 123
        assert data["name"] == "John Doe"

    def test_user_db_from_user_in(self):
        """Тест создания UserDB из UserIn"""
        user_in = UserIn(name="John Doe")
        user_db = UserDB(**user_in.model_dump())
        assert user_db.name == "John Doe"
        assert user_db.launch_count == 0


class TestUserOut:
    """Тесты для модели UserOut"""

    def test_user_out_inheritance(self):
        """Тест наследования от UserDB"""
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
        """Тест сериализации UserOut"""
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
    """Интеграционные тесты для User моделей"""

    def test_user_workflow(self):
        """Тест полного workflow создания пользователя"""
        # 1. Создаем UserIn
        user_in = UserIn(name="John Doe")
        assert user_in.name == "John Doe"
        assert user_in.id is None

        # 2. Создаем UserDB
        user_db = UserDB(**user_in.model_dump())
        user_db.id = 123
        user_db.gender = "male"
        user_db.language = "ru"
        assert user_db.id == 123
        assert user_db.name == "John Doe"
        assert user_db.gender == "male"

        # 3. Создаем UserOut
        user_out = UserOut(**user_db.model_dump())
        assert user_out.id == 123
        assert user_out.name == "John Doe"
        assert user_out.gender == "male"

    def test_user_validation_chain(self):
        """Тест цепочки валидации"""
        # Проверяем, что валидация работает на всех уровнях
        with pytest.raises(ValueError):
            UserIn(name="")  # Пустое имя

    def test_user_edge_cases(self):
        """Тест граничных случаев"""
        # Максимальная длина имени
        user = UserIn(name="a" * 50)
        assert len(user.name) == 50

        # Минимальная длина имени
        user = UserIn(name="a")
        assert len(user.name) == 1

        # Нулевой launch_count
        user = UserDB(name="John Doe", launch_count=0)
        assert user.launch_count == 0

        # Отрицательный launch_count
        user = UserDB(name="John Doe", launch_count=-1)
        assert user.launch_count == -1 