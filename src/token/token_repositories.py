from typing import Annotated

from fastapi import Depends

from src.config.database.db_helper import Session
from src.config.token_config import oauth2_scheme
from src.models.models import User
from src.utils.token_utils import verify_jwt_token


class TokenRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)]) -> User | None:
        """
        Получить пользователя по токену.
        """
        user_id = verify_jwt_token(token).get("sub", None)
        if user_id:
            return self.db.query(User).filter(User.id == int(user_id)).first()

