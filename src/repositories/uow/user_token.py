from ...config.database.db_helper import Session
from ...token.token_repository import TokenRepository
from ...user.user_repositories import UserRepository


class UserTokenUOW:
    def __init__(
            self,
            db: Session = None,
    ):
        self.db = db
        if db:
            self.user_repository = UserRepository(db)
            self.token_repository = TokenRepository(db)
        else:
            self.user_repository = UserRepository()
            self.token_repository = TokenRepository()

    def get_user_by_token_uow(self, token):
        user_id = self.token_repository.get_user_id_by_token_rep(token)
        user = self.user_repository.get_user_by_id(user_id)
        return user
