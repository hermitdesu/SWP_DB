"""
Простой пример unit теста для демонстрации
Этот файл показывает, как можно тестировать ваши модели
"""

# Импортируем необходимые библиотеки
import pytest
from pydantic import ValidationError

# Теперь можно импортировать все модели одним импортом!
# from app.models import UserIn, UserDB, UserOut, Message, ConversationIn

# Простой пример теста без реальных импортов
def test_example():
    """Простой тест для демонстрации"""
    assert 2 + 2 == 4

# Пример того, как теперь можно писать тесты с новыми импортами:
"""
# Старый способ (много импортов):
# from app.models.user import UserIn, UserDB, UserOut
# from app.models.conv import Message, ConversationIn
# from app.models.log import LogIn

# Новый способ (один импорт):
from app.models import UserIn, UserDB, UserOut, Message, ConversationIn, LogIn

def test_user_in_valid():
    # Тест: создание пользователя с правильными данными
    user = UserIn(name="John Doe")
    assert user.name == "John Doe"
    assert user.id is None

def test_user_in_invalid_name():
    # Тест: создание пользователя с пустым именем должно вызвать ошибку
    with pytest.raises(ValidationError):
        UserIn(name="")  # Пустое имя недопустимо

def test_user_in_name_too_long():
    # Тест: имя слишком длинное
    with pytest.raises(ValidationError):
        UserIn(name="a" * 51)  # Имя длиннее 50 символов
"""

if __name__ == "__main__":
    # Запускаем тест
    test_example()
    print("Тест прошел успешно!")
    print("Теперь вы можете использовать удобные импорты:")
    print("from app.models import UserIn, UserDB, UserOut")
    print("from app.cruds import create_user, read_user_by_id") 