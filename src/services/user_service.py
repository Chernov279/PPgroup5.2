from fastapi import Depends

from src.config.database.db_helper import Session, get_db
from src.models.models import User
from src.repositories.user_repositories import UserRepository


def get_user_service(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db=db)

class UserService:



    def create_new_user(self, email: str, hashed_password: str, name: str) -> User:
        """
        Создать нового пользователя.
        """
        return self.user_repo.create_user(email, hashed_password, name)

    def update_user(self, user_id: int, name: str, is_active: bool) -> User:
        """
        Обновить данные пользователя.
        """
        return self.user_repo.update_user(user_id, name, is_active)

    def delete_user(self, user_id: int) -> bool:
        """
        Удалить пользователя.
        """
        return self.user_repo.delete_user(user_id)
