from typing import Union

from fastapi import HTTPException

from ..config.database.db_helper import Session
from .token_utils import verify_jwt_token, create_access_jwt_token, create_refresh_jwt_token


class TokenRepository:
    """
    Репозиторий для работы с токенами (генерация, верификация).

    ### Основные методы:
    - Генерация refresh и access токенов.
    - Извлечение данных о пользователе из токенов.

    ### Инициализация репозитория токенов.

    ### Входные параметры:
    - `db_session` (Session): Экземпляр сессии для работы с базой данных. Если не передан, используется дефолтный репозиторий.
    """
    def __init__(self, db: Session = None):
        self.db = db

    @staticmethod
    def create_access_token_rep(refresh_token: str) -> str | None:
        """
        Создание access токена на основе переданного refresh токена.

        ### Входные параметры:
        - `refresh_token` (str): Refresh токен.

        ### Логика:
        1. Проверяется валидность refresh токена.
        2. Генерируется новый access токен, на основе данных из refresh токена.

        ### Возвращаемые данные:
        - `str`: Сгенерированный access токен.
        """
        payload = verify_jwt_token(refresh_token)
        if payload.get("type", "") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token")
        return create_access_jwt_token(payload)

    @staticmethod
    def create_refresh_token_rep(user_id: Union[int, str]) -> str | None:
        """
        Создание refresh токена для пользователя.

        ### Входные параметры:
        - `user_id` (int | str): Идентификатор пользователя.

        ### Логика:
        1. Проверяется валидность `user_id`.
        2. Генерируется новый refresh токен.

        ### Возвращаемые данные:
        - `str`: Сгенерированный refresh токен.
        """
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        if isinstance(user_id, str):
            user_id = int(user_id)
        refresh_token = create_refresh_jwt_token(user_id=user_id)
        return refresh_token

    @staticmethod
    def get_user_id_by_token_rep(token: str) -> int | None:
        """
        Извлекает идентификатор пользователя из токена.

        ### Входные параметры:
        - `token` (str): Токен.

        ### Логика:
        1. Декодирует токен и извлекает ID пользователя.

        ### Возвращаемые данные:
        - `int`: Идентификатор пользователя, если токен валидный.
        - `None`: Если токен не содержит ID пользователя.
        """
        payload = verify_jwt_token(token)
        user_id = payload.get("sub", None)
        if user_id:
            return int(user_id)
        return None

    @staticmethod
    def get_user_status_by_token_rep(token: str) -> str | None:
        """
        Извлекает статус пользователя из токена.

        ### Входные параметры:
        - `token` (str): Токен.

        ### Логика:
        1. Декодирует токен и извлекает статус пользователя.

        ### Возвращаемые данные:
        - `str`: Статус пользователя, если токен валидный.
        - `None`: Если токен не содержит статуса.
        """
        payload = verify_jwt_token(token)
        user_status = payload.get("status", None)
        if user_status:
            return user_status
        return None
