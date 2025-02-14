from passlib.context import CryptContext
from argon2 import PasswordHasher

from src.exceptions.base_exceptions import AppException

ph = PasswordHasher()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


hashers = {
    "argon2": ph,
}


def hash_password(password: str, scrypt: str = "argon2") -> str:
    """
    Хэширование пароля с использованием выбранного алгоритма.
    Возвращает хэшированный пароль.
    """
    hasher = hashers.get(scrypt)
    if not hasher:
        raise AppException(detail="Wrong type of hash scrypt")
    return hasher.hash(password)


def verify_password(plain_password: str, hashed_password: str, scrypt: str = "argon2") -> bool:
    """
    Проверка пароля с хэшированным значением.
    """
    hasher = hashers.get(scrypt)
    if not hasher:
        raise AppException(detail="Wrong type of hash scrypt")
    return ph.verify(hashed_password, plain_password)
