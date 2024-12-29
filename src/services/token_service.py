from fastapi import HTTPException

from src.authentication.schemas import TokenOut
from src.utils.token_utils import verify_jwt_token, create_access_jwt_token, create_refresh_jwt_token


class TokenService:
    @staticmethod
    def create_access_token_service(refresh_token: str) -> TokenOut | None:
        payload = verify_jwt_token(refresh_token)
        if payload.get("type") != "access":
            HTTPException(status_code=401, detail="Invalid token")
        access_token = create_access_jwt_token(payload)
        return TokenOut(access_token=access_token)

    @staticmethod
    def create_refresh_token_service(user_id: int) -> str | None:
        if not user_id:
            HTTPException(status_code=401, detail="Invalid token")
        refresh_token = create_refresh_jwt_token(user_id=user_id)
        return refresh_token
