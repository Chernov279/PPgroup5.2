from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends

from src.models.models import User
from src.config.database.db_helper import get_db


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_or_404(self, user_id: int) -> User | None:
        """
        Получить пользователя по ID или выбросить ошибку, если пользователь не найден.
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def get_user_by_email(self, email: str) -> User | None:
        """
        Получить пользователя по email.
        """
        return self.db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def create_user(self, email: str, hashed_password: str, name: str) -> User:
        """
        Создать нового пользователя.
        """
        db_user = User(email=email, hashed_password=hashed_password, name=name)
        try:
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="User not created")

    def update_user(self, user_id: int, name: str, is_active: bool) -> User:
        """
        Обновить информацию о пользователе.
        """
        db_user = self.get_user_by_id(user_id)
        if db_user:
            db_user.name = name
            db_user.is_active = is_active
            try:
                self.db.commit()
                self.db.refresh(db_user)
                return db_user
            except Exception as e:
                self.db.rollback()
                raise HTTPException(status_code=500, detail="User not updated")
        else:
            raise HTTPException(status_code=404, detail="User not found")

    def delete_user(self, user_id: int) -> bool:
        """
        Удалить пользователя.
        """
        db_user = self.get_user_by_id(user_id)
        if db_user:
            try:
                self.db.delete(db_user)
                self.db.commit()
                return True
            except Exception as e:
                self.db.rollback()
                raise HTTPException(status_code=500, detail="User not deleted")
        else:
            raise HTTPException(status_code=404, detail="User not found")
