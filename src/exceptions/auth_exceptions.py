from src.exceptions.base_exceptions import AppException


class InvalidEmailException(AppException):
    """Исключение для невалидной электронной почты."""
    def __init__(self):
        super().__init__(status_code=400, detail="Invalid email address")


class InvalidCredentialsException(AppException):
    """Исключение для неверной пары логин/пароль."""
    def __init__(self):
        super().__init__(status_code=401, detail="Invalid email or password")


class EmailAlreadyExistsException(AppException):
    """Исключение для уже зарегистрированного email."""
    def __init__(self):
        super().__init__(status_code=409, detail="User with this email already exists")


class InvalidUsernameException(AppException):
    """Исключение для невалидного имени пользователя."""
    def __init__(self, detail: str = "Invalid username format"):
        super().__init__(status_code=400, detail=detail)


class InvalidPasswordException(AppException):
    """Исключение для слабого пароля."""
    def __init__(self, detail: str = "Password does not meet security requirements"):
        super().__init__(status_code=400, detail=detail)
