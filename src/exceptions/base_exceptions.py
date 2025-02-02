from fastapi import HTTPException
from fastapi.responses import JSONResponse


class AppException(HTTPException):
    def __init__(self, status_code: int = 500, detail: str = None):
        super().__init__(status_code=status_code, detail=detail)


class ValidationException(AppException):
    def __init__(self, field: str, message: str):
        detail = f"Validation error on {field}: {message}"
        super().__init__(status_code=422, detail=detail)


class NoContentResponse:
    def __init__(self, status_code: int = 200, **content):
        self.status_code = status_code
        if hasattr(content, "content"):
            self.content = content
        elif isinstance(content, dict):
            self.content = content
        else:
            raise ValidationException(f"NoContentResponse", f"parameter 'content' is not valid obj")

    def get_response(self):
        return JSONResponse(status_code=self.status_code, content=self.content)
