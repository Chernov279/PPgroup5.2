from typing import Optional

from src.exceptions.base_exceptions import AppException


class InvalidTokenUserException(AppException):
    def __init__(self, user_id: Optional[int] = None):
        detail = f"User with ID {user_id} from token does not exist or token is invalid." \
            if user_id is not None else\
            "User from token does not exist or token is invalid"
        super().__init__(status_code=401, detail=detail)


class TokenMissingException(AppException):
    def __init__(self, token_type: Optional[str] = None):
        detail = f"{token_type} is missing"\
            if token_type is not None else \
            "Token is missing"
        super().__init__(status_code=401, detail=detail)


class InvalidTokenException(AppException):
    """Исключение при невалидном токене"""
    def __init__(self, detail: str = "Invalid token"):
        super().__init__(status_code=401, detail=detail)


class TokenRevokedException(AppException):
    """Исключение при отозванном токене"""
    def __init__(self, detail: str = "Token has been revoked"):
        super().__init__(status_code=403, detail=detail)


class TokenExpiredException(AppException):
    """Исключение при истекшем токене"""
    def __init__(self, detail: str = "Token has expired"):
        super().__init__(status_code=401, detail=detail)

