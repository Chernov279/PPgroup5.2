from fastapi import Depends

from src.config.database.db_helper import Session, get_db
from src.repositories.uow.auth_token import AuthTokenUOW


def get_auth_token_uow_db(db: Session = Depends(get_db)) -> AuthTokenUOW:
    return AuthTokenUOW(db)


def get_auth_token_uow() -> AuthTokenUOW:
    return AuthTokenUOW()