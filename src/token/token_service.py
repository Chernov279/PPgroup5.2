from fastapi import HTTPException, Security, Depends
from fastapi.security import OAuth2PasswordBearer

from src.authentication.schemas import TokenOut
from src.dependencies.user_dependencies import get_user_service
from src.models.models import User
from src.utils.token_utils import verify_jwt_token, create_access_jwt_token, create_refresh_jwt_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class TokenService:
    @staticmethod
    def create_access_token_service(refresh_token: str) -> TokenOut | None:
        payload = verify_jwt_token(refresh_token)
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid token")
        access_token = create_access_jwt_token(payload)
        return TokenOut(access_token=access_token)

    @staticmethod
    def create_refresh_token_service(user_id: int) -> str | None:
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        refresh_token = create_refresh_jwt_token(user_id=user_id)
        return refresh_token

    @staticmethod
    def get_user_id_by_token_service(token: str = Security(oauth2_scheme)) -> int | None:
        payload = verify_jwt_token(token)
        user_id = payload.get("sub")
        if user_id:
            return int(user_id)
        return None

    @staticmethod
    def get_user_status_by_token_service(token: str = Security(oauth2_scheme)) -> str | None:
        payload = verify_jwt_token(token)
        user_status = payload.get("status", None)
        if user_status:
            return user_status
        return None

    @staticmethod
    def get_user_by_token_service(
            token: str = Security(oauth2_scheme),
            user_service = Depends(get_user_service)
    ) -> User | None:
        payload = verify_jwt_token(token)
        user_id = payload.get("sub")
        if user_id:
            return user_service.get_user_or_404_service(int(user_id))
        return None
