from fastapi import Depends

from src.config.database.db_helper import Session, get_db
from src.token.token_service import TokenService


def get_token_db_service(db: Session = Depends(get_db)) -> TokenService:
    return TokenService(db)


def get_token_service() -> TokenService:
    return TokenService()
