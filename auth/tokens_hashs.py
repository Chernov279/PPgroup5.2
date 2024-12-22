import secrets
import string
import hashlib
import os
from PPgroup5.pythonBackEnd.database.database import User, session


def generate_token(length=10):
    """
    Генерирует уникальный токен мобильного приложения.

    Parameters:
    - length (int): Длина токена (по умолчанию 10 символов).

    Returns:
    - str: Сгенерированный уникальный токен.
    """
    alphabet = string.digits
    token_mobile = ''.join(secrets.choice(alphabet) for _ in range(length))
    user = session.query(User).filter_by(token_mobile=token_mobile).first()
    if user is None:
        return token_mobile
    return generate_token()


def generate_salt():
    """
    Генерирует случайную соль для хэширования пароля.

    Returns:
    - str: Сгенерированная соль в виде hex строки.
    """
    return os.urandom(16).hex()


def hash_password(password, salt):
    """
    Хэширует пароль с использованием соли.

    Parameters:
    - password (str): Пароль для хэширования.
    - salt (str): Соль для хэширования.

    Returns:
    - str: Хэшированный пароль.
    """
    hash_input = f"{password}{salt}".encode('utf-8')
    hashed_password = hashlib.sha256(hash_input).hexdigest()
    return hashed_password


def creating_hash_salt(password):
    """
    Создает хэш пароля и соль для сохранения в базе данных.

    Parameters:
    - password (str): Пароль для хэширования.

    Returns:
    - tuple: Кортеж из соли и хэшированного пароля.
    """
    salt = generate_salt()
    hashed_password = hash_password(password, salt)
    return salt, hashed_password


def authenticated_user(entry_password, hashed_password, salt):
    """
    Проверяет аутентификацию пользователя на основе введенного пароля.

    Parameters:
    - entry_password (str): Введенный пользователем пароль.
    - hashed_password (str): Хэшированный пароль в базе данных.
    - salt (str): Соль для хэширования пароля.

    Returns:
    - bool: True, если пароль верный, иначе False.
    """
    return hash_password(entry_password, salt) == hashed_password
