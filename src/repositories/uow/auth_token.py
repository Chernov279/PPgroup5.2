from fastapi import HTTPException

from ...authentication.utils.security import verify_password
from ...config.database.db_helper import Session
from ...config.token_config import settings_token
from ...models.models import User
from ...token.token_repository import TokenRepository


class AuthTokenUOW:
    """
    Unit of Work (UoW) для работы с авторизацией и токенами (refresh и access).

    ### Основные задачи:
    - Создание refresh и access токенов.
    - Управление cookies для refresh токенов.

    ###Инициализация UoW для токенов.

    - `db` (Session): Экземпляр SQLAlchemy-сессии для работы с базой данных.

    Если передана сессия `db`, инициализируются репозитории с этой сессией.
    Если `db` не передана, используются репозитории с дефолтными параметрами.
        """

    def __init__(
            self,
            db: Session = None,
    ):
        self.db = db
        if db:
            self.token_repository = TokenRepository(db)
        else:
            self.token_repository = TokenRepository()

    def create_refresh_token_uow(self, user_id):
        """
        Создание refresh токена.

        ### Входные параметры:
        - `user_id` (int): Идентификатор пользователя.

        ### Логика:
        1. Вызывает `create_refresh_token_rep` в `TokenRepository`.
        2. Возвращает сгенерированный токен.

        ### Возвращаемые данные:
        - `str`: Сгенерированный refresh токен.
        """
        return self.token_repository.create_refresh_token_rep(user_id)

    def create_access_token_uow(self, refresh_token):
        """
        Создание access токена.

        ### Входные параметры:
        - `refresh_token` (str): Действующий refresh токен.

        ### Логика:
        1. Вызывает `create_access_token_rep` в `TokenRepository`.
        2. Возвращает сгенерированный токен.

        ### Возвращаемые данные:
        - `str`: Сгенерированный access токен.
        """
        return self.token_repository.create_access_token_rep(refresh_token)

    # TODO пофиксить это чудо
    def get_login_user_uow(self, email: str, password: str) -> User | None:
        user = self.db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return user

    @staticmethod
    def set_refresh_token_cookie_uow(response, refresh_token: str) -> None:
        """
        Устанавливает refresh токен в cookies.

        ### Входные параметры:
        - `response` (JSONResponse): Ответ, в который нужно добавить cookie.
        - `refresh_token` (str): Значение refresh токена.

        ### Логика:
        Устанавливает cookie с ключом `refresh_token`.
        """
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=settings_token.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
            path="/get_token",
        )

    @staticmethod
    def delete_refresh_token_cookie_uow(response) -> None:
        """
        Удаляет refresh токен из cookies.

        ### Входные параметры:
        - `response` (JSONResponse): Ответ, из которого нужно удалить cookie.

        ### Логика:
        1. Удаляет cookie с ключом `refresh_token` и путем `/get_token`.
        """
        response.delete_cookie(
            key="refresh_token",
            path="/get_token"
        )
