from typing import Annotated

from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from ..config.database.db_helper import Session
from src.unit_of_work.auth_token import AuthTokenUOW
from .token_repository import TokenRepository


class TokenService:
    """
    Сервис для работы с токенами (генерация access и refresh токенов).

    ### Основные функции:
    - Авторизация пользователя и выдача токенов.
    - Получение нового access токена по refresh токену.


    ### Инициализация сервиса токенов.

    ### Входные параметры:
    - `db_session` (Session): Экземпляр сессии для работы с базой данных. Если не передан, используется дефолтный репозиторий.
    """
    def __init__(
            self,
            db: Session = None,
    ):
        if db:
            self.auth_token_uow = AuthTokenUOW(db)
            self.token_repo = TokenRepository(db)
        else:
            self.auth_token_uow = AuthTokenUOW()
            self.token_repo = TokenRepository()

    def login_user_service(
            self,
            form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    ) -> JSONResponse:
        """
        Авторизация пользователя с использованием email и пароля. Возвращает access и refresh токены.

        ### Входные параметры:
        - `form_data` (OAuth2PasswordRequestForm):
          - `username` (str): Email пользователя.
          - `password` (str): Пароль пользователя.

        ### Логика:
        Входные данные передаются в `AuthTokenUOW` для проверки пользователя.
        Генерация refresh и access токенов через `TokenRepository`.
        В ответ возвращается JSON с access токеном и его типом.
        refresh токен сохраняется в cookie (HttpOnly).

        ### Возвращаемые данные:
        - `JSONResponse`:
          - `access_token` (str): Сгенерированный access токен.
          - `token_type` (str): Тип токена, обычно "bearer".
        """
        user = self.auth_token_uow.get_login_user_uow(form_data.username, form_data.password)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        refresh_token = self.token_repo.create_refresh_token_rep(user_id=user.id)
        access_token = self.token_repo.create_access_token_rep(refresh_token)
        response = JSONResponse(content={
            "access_token": access_token,
            "token_type": "bearer",
        })
        self.auth_token_uow.set_refresh_token_cookie_uow(response=response, refresh_token=refresh_token)
        return response

    def get_access_token_service(self, request: Request) -> dict[str, str | None]:
        """
        Получение нового access токена по refresh токену, который передаётся через cookie.

        ### Входные параметры:
        - `request` (Request): HTTP запрос, содержащий refresh токен в cookie.

        ### Логика:
        Извлекается refresh токен из cookie.
        Генерируется новый access токен через `TokenRepository`.
        Если токена нет или он недействителен, выбрасывается ошибка.

        ### Возвращаемые данные:
        - `dict`:
          - `access_token` (str): Новый access токен.
          - `token_type` (str): Тип токена, обычно "bearer".
        """
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise HTTPException(status_code=400, detail="Refresh token is missing")

        access_token = self.token_repo.create_access_token_rep(refresh_token)
        return {"access_token": access_token, "token_type": "bearer"}
