from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from .auth_schemas import UserAuthIn, UserLoginIn
from .utils.auth_utils import is_valid_email
from .utils.security import hash_password, verify_password
from ..repositories.uow.auth_token import AuthTokenUOW
# TODO убрать импорт UserRepository из сервиса
from ..user.user_repository import UserRepository


class UserAuthService:
    """
    Сервис для работы с аутентификацией и регистрацией пользователей.

    ### Основные задачи:
    - Регистрация новых пользователей.
    - Авторизация (вход) пользователей.
    - Выход (logout) пользователей, включая управление токенами.

    ###Инициализация сервиса аутентификации.

    - `db` (Session): Экземпляр SQLAlchemy-сессии для взаимодействия с базой данных.

    Если передана сессия `db`, инициализируются репозитории с этой сессией.
    Если `db` не передана, используются репозитории с дефолтными параметрами.
    Такая логика использована для того, чтобы не инициализировать репозиторий с сессией даже в том случае, когда логика
     выполняется и без обращения к БД
    """
    def __init__(
            self,
            db: Session = None
    ):
        if db:
            self.user_repo = UserRepository(db)
            self.auth_uow = AuthTokenUOW(db)
        else:
            self.user_repo = UserRepository()
            self.auth_uow = AuthTokenUOW()

    def register_user(
            self,
            user_auth: UserAuthIn,
    ) -> JSONResponse:
        """
        Регистрация нового пользователя.

        ### Входные параметры:
        - `user_auth` (UserAuthIn): Данные для регистрации пользователя.
          - Поля:
            - `name` (str): Имя пользователя.
            - `email` (str): Email пользователя.
            - `password` (str): Пароль пользователя.

        ### Логика:
        1. Проверяет валидность email через `is_valid_email`.
        2. Проверяет, что email не зарегистрирован.
        3. Хэширует пароль.
        4. Создаёт нового пользователя в базе данных через `UserRepository`.
        5. Генерирует refresh и access токены через `AuthTokenUOW`.
        6. Устанавливает refresh токен в cookies.
        7. Возвращает JSON-ответ с access токеном.

        ### Возвращаемые данные:
        - `JSONResponse`:
          - Поля:
            - `access_token` (str): Токен доступа.
            - `token_type` (str): Тип токена (обычно "bearer").
        """
        # TODO проверка на никнейм и сложность пароля, похожесть пароля на email и ник
        if not is_valid_email(user_auth.email):
            raise HTTPException(status_code=400, detail="Invalid email format")

        if self.user_repo.get_user_by_email(user_auth.email):
            raise HTTPException(status_code=400, detail="Email is already registered")

        hashed_password = hash_password(user_auth.password)
        user = self.user_repo.create_user(user_auth.name, user_auth.email, hashed_password)
        refresh_token = self.auth_uow.create_refresh_token_uow(user.id)
        access_token = self.auth_uow.create_access_token_uow(refresh_token)
        response = JSONResponse(content={
            "access_token": access_token,
            "token_type": "bearer",
        })
        self.auth_uow.set_refresh_token_cookie_uow(response, refresh_token)
        return response

    def login_user(
            self,
            user_login: UserLoginIn
    ) -> JSONResponse | None:
        """
        Авторизация пользователя.

        ### Входные параметры:
        - `user_login` (UserLoginIn): Учетные данные пользователя.
          - Поля:
            - `email` (str): Email пользователя.
            - `password` (str): Пароль пользователя.

        ### Логика:
        1. Проверяет существование пользователя по email через `UserRepository`.
        2. Проверяет соответствие пароля через `verify_password`.
        3. Генерирует refresh и access токены через `AuthTokenUOW`.
        4. Устанавливает refresh токен в cookies.
        5. Возвращает JSON-ответ с access токеном.

        ### Возвращаемые данные:
        - `JSONResponse`:
          - Поля:
            - `access_token` (str): Токен доступа.
            - `token_type` (str): Тип токена (обычно "bearer").
        """
        user = self.user_repo.get_user_by_email(user_login.email)
        if not user or not verify_password(user_login.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        refresh_token = self.auth_uow.create_refresh_token_uow(user_id=user.id)
        access_token = self.auth_uow.create_access_token_uow(refresh_token)
        response = JSONResponse(content={
            "access_token": access_token,
            "token_type": "bearer",
        })
        self.auth_uow.set_refresh_token_cookie_uow(response, refresh_token)
        return response

    def logout_user(self) -> JSONResponse:
        """
        Выход пользователя из системы.

        ### Логика:
        1. Удаляет refresh токен из cookies через `AuthTokenUOW`.
        2. Возвращает JSON-ответ с сообщением об успешном выходе.

        ### Возвращаемые данные:
        - `JSONResponse`:
          - Поля:
            - `message` (str): Сообщение об успешном выходе.
        """
        response = JSONResponse(content={})
        self.auth_uow.delete_refresh_token_cookie_uow(response)

        response.content = {"message": "Successfully logged out"}
        return response
