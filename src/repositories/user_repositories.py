from typing import List

from sqlalchemy.orm import Session

from src.models.models import User
from src.utils.logging_utils import log_errors


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int) -> User | None:
        """
        Получить пользователя по ID.
        """
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> User | None:
        """
        Получить пользователя по email.
        """
        return self.db.query(User).filter(User.email == email).first()

    def get_users(self) -> List[User]:
        """
        Получить пользователя по ID.
        """
        return self.db.query(User).all()

    def create_user(self, name: str, email: str, hashed_password: str) -> User:
        """
        Создать нового пользователя.
        """
        user = User(name=name, email=email, hashed_password=hashed_password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user(self, user_id: int, name: str) -> User | None:
        """
        Обновить информацию о пользователе.
        """
        user = self.get_user_by_id(user_id)
        if user:
            user.name = name
            self.db.commit()
            self.db.refresh(user)
            return user
        return None

    def delete_user(self, user_id: int) -> bool:
        """
        Удалить пользователя.
        """
        user = self.get_user_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False