from fastapi import HTTPException

from src.authentication.schemas import AccessTokenOut, TokensOut
from src.authentication.utils.auth_utils import is_valid_email
from src.authentication.utils.security import hash_password, verify_password
from src.user.user_repositories import UserRepository
from sqlalchemy.orm import Session


class UserAuthService:
    def __init__(self, user_repo: UserRepository = None):
        self.user_repo = user_repo

    def register_user(self, name: str, email: str, password: str) -> AccessTokenOut | None:
        # TODO проверка на никнейм и сложность пароля, похожесть пароля на email и ник
        if not is_valid_email(email):
            raise HTTPException(status_code=400, detail="Invalid email format")

        if self.user_repo.get_user_by_email(email):
            raise HTTPException(status_code=400, detail="Email is already registered")

        hashed_password = hash_password(password)
        user = self.user_repo.create_user(name, email, hashed_password)
        refresh_token =""
        access_token =""
        return TokensOut(
            refresh_token=refresh_token,
            access_token=access_token
        )

    def login_user(self, email: str, password: str) -> TokensOut | None:
        user = self.user_repo.get_user_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        refresh_token = TokenService.create_refresh_token_service(user_id=user.id)
        access_token = TokenService.create_access_token_service(refresh_token)
        return TokensOut(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    def logout_user(self, db: Session) -> None:
        # Логика для выхода, например, удаление токена из базы или завершение сессии
        # Здесь можно оставить заглушку, поскольку выход не всегда требует логики на сервере
        pass
