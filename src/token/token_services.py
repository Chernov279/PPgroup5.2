from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import Optional

from src.config.token_config import settings_token
from src.models.models import User
from src.repositories.user_repositories import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_token(token: str = Depends(oauth2_scheme)) -> Optional[User]:
    """
    Проверка токена и извлечение пользователя.
    """
    try:
        payload = jwt.decode(token, settings_token.SECRET_KEY, algorithms=[settings_token.ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            return None
        user = UserRepository.get_user_by_id(user_id)
        if user:
            return user
        raise HTTPException(
            status_code=404,
            detail="User by ID not found",
        )
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )


def is_admin(token: str = Depends(oauth2_scheme)) -> bool:
    """
    Проверка токена и извлечение пользователя.
    """
    try:
        payload = jwt.decode(token, settings_token.SECRET_KEY, algorithms=[settings_token.ALGORITHM])
        status = payload.get("status")
        permission_status = {"member": 1, "honored": 2, "moderator": 3, "superuser": 4}
        if status is None or status not in permission_status:
            return False
        return permission_status[status] >= 3

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )
