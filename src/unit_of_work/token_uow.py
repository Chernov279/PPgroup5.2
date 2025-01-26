from src.models.models import User
from src.repositories.base_repositories import BaseRepository
from src.token.token_utils import verify_jwt_token
from src.unit_of_work.base_uow import BaseUOW


class TokenUOW(BaseUOW):
    def __init__(self, db_session):
        super().__init__(db_session)

    def is_user_exists_by_token_uow(self, token: str) -> bool | None:
        payload = verify_jwt_token(token)
        user_id = payload.get("sub", None)
        if user_id is None:
            # TODO
            return
        base_repo = BaseRepository(self.db_session)
        # TODO user_repo
        user = base_repo.get_single(User, id=user_id)
        if user:
            return True
        return False

    def user_exists_by_token_uow(self, token: str) -> int | None:
        payload = verify_jwt_token(token)
        user_id = payload.get("sub", None)
        if user_id is None:
            return# TODO
        base_repo = BaseRepository(self.db_session)
        user = base_repo.get_single(User, id=user_id)
        if user:
            return int(user_id)
        return

    def get_user_by_token_uow(self, token: str) -> User | None:
        payload = verify_jwt_token(token)
        user_id = payload.get("sub", None)
        if user_id is None:
            return# TODO
        base_repo = BaseRepository(self.db_session)
        user = base_repo.get_single(User, id=user_id)
        if user:
            return user

    @staticmethod
    def get_user_id_by_token_uow(token: str) -> int | None:
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
    def get_user_status_by_token_uow(token: str) -> str | None:
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
