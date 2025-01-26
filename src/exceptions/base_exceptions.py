from fastapi import HTTPException
from fastapi.responses import JSONResponse


class AppException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class ValidationException(AppException):
    def __init__(self, field: str, message: str):
        detail = f"Validation error on {field}: {message}"
        super().__init__(status_code=422, detail=detail)


class NoContentException(AppException):
    def __init__(self, message: str = "Success"):
        super().__init__(status_code=200, detail=message)

    def get_response(self):
        return JSONResponse(status_code=200, content={})
