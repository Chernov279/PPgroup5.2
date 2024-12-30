from fastapi import Depends, HTTPException, status

from src.token.token_services import verify_token
from src.models.models import User


def get_token_from_header(authorization: str) -> str:
    """
    Извлекаем токен из заголовка Authorization.
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization token is missing",
        )
    return authorization.split("Bearer ")[-1]  # извлекаем токен из формата 'Bearer <token>'


def get_user_from_token(token: str = Depends(get_token_from_header)) -> User:
    """
    Получаем пользователя по токену.
    """
    user = verify_token(token)  # Предполагаем, что есть функция для верификации токена
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or expired",
        )
    return user