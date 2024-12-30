from typing import Annotated

from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from src.config.database.db_helper import Session
from src.repositories.uow.auth_token import AuthTokenUOW
from src.token.token_repositories import TokenRepository


class TokenService:
    def __init__(
            self,
            db: Session = None,
    ):
        if db:
            self.auth_token_uow = AuthTokenUOW(db)
        else:
            self.auth_token_uow = AuthTokenUOW()

    def login_user_service(
            self,
            form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    ) -> JSONResponse:
        user = self.auth_token_uow.get_login_user_uow(form_data.username, form_data.password)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        refresh_token = self.auth_token_uow.create_refresh_token_uow(user_id=user.id)
        access_token = self.auth_token_uow.create_access_token_uow(refresh_token)
        response = JSONResponse(content={
            "access_token": access_token,
            "token_type": "bearer",
        })
        self.auth_token_uow.set_refresh_token_cookie_uow(response=response, refresh_token=refresh_token)
        return response

    def get_access_token_service(self, request: Request) -> dict[str, str | None]:
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise HTTPException(status_code=400, detail="Refresh token is missing")

        access_token = self.auth_token_uow.create_access_token_uow(refresh_token)
        return {"access_token": access_token, "token_type": "bearer"}
