from fastapi import Depends
from sqlalchemy.orm import Session

from src.config.database.db_helper import get_db
from src.repositories.user_repositories import UserRepository
from src.services.user_service import UserService


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    """
    Фабричная функция для создания UserService с передачей нужных зависимостей.
    """
    user_repo = UserRepository(db)
    return UserService(user_repo)
