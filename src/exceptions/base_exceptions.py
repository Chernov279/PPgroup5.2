from fastapi import HTTPException


class AppException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class ValidationException(AppException):
    def __init__(self, field: str, message: str):
        detail = f"Validation error on {field}: {message}"
        super().__init__(status_code=422, detail=detail)
