from fastapi import HTTPException

from src.authentication.utils.auth_utils import is_valid_email
from src.authentication.utils.security import hash_password, verify_password, create_refresh_jwt_token
from src.models.models import User
from src.repositories.user_repositories import UserRepository
from sqlalchemy.orm import Session
from datetime import datetime, timedelta


class UserAuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register_user(self, name: str, email: str, password: str) -> User | None:
        # TODO проверка на никнейм и сложность пароля, похожесть пароля на email и ник
        if not is_valid_email(email):
            raise HTTPException(status_code=400, detail="Invalid email format")

        if self.user_repo.get_user_by_email(email):
            raise HTTPException(status_code=400, detail="Email is already registered")

        hashed_password = hash_password(password)

        return self.user_repo.create_user(name, email, hashed_password)

    def login_user(self, email: str, password: str) -> str:
        user = self.user_repo.get_user_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_refresh_jwt_token(user)
        return token

    def logout_user(self, db: Session) -> None:
        # Логика для выхода, например, удаление токена из базы или завершение сессии
        # Здесь можно оставить заглушку, поскольку выход не всегда требует логики на сервере
        pass

    def generate_jwt_token(self, user: User) -> str:
        """
        Генерация JWT токена (заглушка, нужно будет добавить реальную логику).
        """
        # Примерный код для генерации JWT токена
        expiration = datetime.utcnow() + timedelta(hours=1)
        return f"token-for-{user.email}-expiring-at-{expiration}"