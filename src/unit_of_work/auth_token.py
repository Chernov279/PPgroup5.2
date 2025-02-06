from fastapi import HTTPException

from src.authentication.utils.security import verify_password
from src.config.token_config import settings_token
from src.models.models import User
from src.token.token_repository import TokenRepository


class AuthTokenUOW:
    """
    Unit of Work (UoW) для работы с авторизацией и токенами (refresh и access).

    ### Основные задачи:
    - Создание refresh и access токенов.
    - Управление cookies для refresh токенов.

    ###Инициализация UoW для токенов.

    - `db_session` (Session): Экземпляр SQLAlchemy-сессии для работы с базой данных.

    Если передана сессия `db_session`, инициализируются репозитории с этой сессией.
    Если `db_session` не передана, используются репозитории с дефолтными параметрами.
        """

    def __init__(
            self,
            db = None,
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

