from src.models.models import User
from src.token.token_repository import TokenRepository
from src.user.user_repository import UserRepository


class UserUOW:
    def __init__(
            self,
            db_session = None,
    ):
        self.db_session = db_session

    def get_user_by_token_uow(self, token) -> User | None:
        token_repository = TokenRepository(self.db_session)
        user_repository = UserRepository(self.db_session)

        user_id = token_repository.get_user_id_by_token_rep(token)
        if user_id is None:
            return
        user = user_repository.get_user_by_id(user_id)
        return user

    def is_user_exists_by_token(self, token) -> bool | None:
        token_repository = TokenRepository(self.db_session)
        user_repository = UserRepository(self.db_session)

        user_id = token_repository.get_user_id_by_token_rep(token)
        if user_id is None:
            return
        user = user_repository.get_user_by_id(user_id)
        if user:
            return True
        return False

    def is_user_exists_by_id(self, user_id: int) -> bool:
        user_repository = UserRepository(self.db_session)

        user = user_repository.get_user_by_id(user_id)
        if user:
            return True
        return False
