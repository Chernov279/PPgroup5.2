from typing import List

from sqlalchemy.orm import Session

from ..models.models import User


class UserRepository:
    def __init__(self, db: Session = None):
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

    def update_user(
            self,
            user: User,
            user_data
    ) -> User | None:
        """
        Обновить информацию о пользователе.
        """
        updated = False

        if user:
            if user_data.name and user.name != user_data.name:
                user.name = user_data.name
                updated = True

            if user_data.surname and user.surname != user_data.surname:
                user.surname = user_data.surname
                updated = True

            if user_data.patronymic and user.patronymic != user_data.patronymic:
                user.patronymic = user_data.patronymic
                updated = True

            if user_data.location and user.location != user_data.location:
                user.location = user_data.location
                updated = True

            if user_data.sex and user.sex != user_data.sex:
                user.sex = user_data.sex
                updated = True

            if user_data.birth and user.birth != user_data.birth:
                user.birth = user_data.birth
                updated = True

            if updated:
                self.db.commit()
                self.db.refresh(user)
            return user
        return None

    def delete_user(self, user: User) -> bool:
        """
        Удалить пользователя.
        """
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False
