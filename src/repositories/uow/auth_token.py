from typing import Union

from fastapi import HTTPException, Depends

from src.authentication.schemas import TokensOut
from src.authentication.utils.security import verify_password
from src.config.database.db_helper import Session
from src.config.token_config import settings_token, oauth2_scheme
from src.models.models import User
from src.token.token_repositories import TokenRepository
from src.utils.token_utils import create_refresh_jwt_token, create_access_jwt_token, verify_jwt_token


class AuthTokenUOW:
    def __init__(
            self,
            db: Session = None,
            token_repository: TokenRepository = None
    ):
        self.db = db
        self.token_repository = token_repository

    @staticmethod
    def create_access_token_uow(refresh_token: str) -> str | None:
        payload = verify_jwt_token(refresh_token)
        if payload.get("type", "") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token")
        return create_access_jwt_token(payload)

    @staticmethod
    def create_refresh_token_uow(user_id: Union[int, str]) -> str | None:
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        if isinstance(user_id, str):
            user_id = int(user_id)
        refresh_token = create_refresh_jwt_token(user_id=user_id)
        return refresh_token

    def get_login_user_uow(self, email: str, password: str) -> User | None:
        user = self.db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return user

    @staticmethod
    def get_user_id_by_token_uow(token: str) -> int | None:
        payload = verify_jwt_token(token)
        user_id = payload.get("sub", None)
        if user_id:
            return int(user_id)
        return None

    @staticmethod
    def get_user_status_by_token_uow(token: str) -> str | None:
        payload = verify_jwt_token(token)
        user_status = payload.get("status", None)
        if user_status:
            return user_status
        return None

    def get_user_by_token_uow(self, token: str = Depends(oauth2_scheme)) -> User | None:
        payload = verify_jwt_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        return self.token_repository.get_current_user(token)

    @staticmethod
    def set_refresh_token_cookie_uow(response, refresh_token: str) -> None:
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=settings_token.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
            path="/get_token",
        )

    # def login_user_service(
    #     self,
    #     form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    #     user_auth_service: UserAuthService = Depends(get_user_auth_service),
    #     ) -> JSONResponse:
    #     payload = user_auth_service.login_user(form_data.username, form_data.password)
    #     response = JSONResponse(content={
    #         "access_token": payload.access_token,
    #         "token_type": "bearer",
    #     })
    #     self.set_refresh_token_cookie(response, payload.refresh_token)
    #     return response
