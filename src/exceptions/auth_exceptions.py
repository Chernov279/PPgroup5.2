from src.exceptions.base_exceptions import AppException


class InvalidEmailException(AppException):
    def __init__(self):
        detail = f"Invalid email"
        super().__init__(status_code=400, detail=detail)


class InvalidCredentialsException(AppException):
    def __init__(self):
        detail = f"Invalid login or password"
        super().__init__(status_code=401, detail=detail)


class EmailAlreadyExistsException(AppException):
    def __init__(self):
        detail = f"User with this email already exists"
        super().__init__(status_code=409, detail=detail)
