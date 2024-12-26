from fastapi import Depends
from sqlalchemy.orm import Session

from src.authentication.auth_service import UserAuthService
from src.config.database.db_helper import get_db
from src.repositories.user_repositories import UserRepository


def get_user_auth_service(db: Session = Depends(get_db)) -> UserAuthService:
    """
    Фабричная функция для создания UserService с передачей нужных зависимостей.
    """
    user_repo = UserRepository(db)
    return UserAuthService(user_repo)
