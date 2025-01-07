from src.exceptions.base_exceptions import AppException


class InvalidTokenUserException(AppException):
    def __init__(self, user_id: int):
        detail = f"User with ID {user_id} from token does not exist or is invalid."
        super().__init__(status_code=401, detail=detail)
