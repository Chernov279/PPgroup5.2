from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Хэширование пароля с использованием bcrypt.
    Возвращает хэшированный пароль.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверка пароля с хэшированным значением.
    """
    return pwd_context.verify(plain_password, hashed_password)
