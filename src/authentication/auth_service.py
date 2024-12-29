from fastapi import HTTPException

from src.authentication.schemas import UserLoginOut
from src.authentication.utils.auth_utils import is_valid_email
from src.authentication.utils.security import hash_password, verify_password
from src.repositories.user_repositories import UserRepository
from sqlalchemy.orm import Session

from src.services.token_service import TokenService


class UserAuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register_user(self, name: str, email: str, password: str) -> UserLoginOut | None:
        # TODO проверка на никнейм и сложность пароля, похожесть пароля на email и ник
        if not is_valid_email(email):
            raise HTTPException(status_code=400, detail="Invalid email format")

        if self.user_repo.get_user_by_email(email):
            raise HTTPException(status_code=400, detail="Email is already registered")

        hashed_password = hash_password(password)
        user = self.user_repo.create_user(name, email, hashed_password)
        refresh_token = TokenService.create_refresh_token_service(user.id)
        return UserLoginOut(refresh_token=refresh_token)

    def login_user(self, email: str, password: str) -> UserLoginOut | None:
        user = self.user_repo.get_user_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        refresh_token = TokenService.create_refresh_token_service(user_id=user.id)
        return UserLoginOut(refresh_token=refresh_token)

    def logout_user(self, db: Session) -> None:
        # Логика для выхода, например, удаление токена из базы или завершение сессии
        # Здесь можно оставить заглушку, поскольку выход не всегда требует логики на сервере
        pass
