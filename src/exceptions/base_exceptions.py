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
    def __init__(self, status_code: int = 200, detail=None):
        self.status_code = status_code
        if detail is None:
            self.content = {}
        elif isinstance(detail, dict) or isinstance(detail, str):
            self.content = {"detail": detail}
        else:
            raise ValidationException(f"NoContentResponse", f"parameter 'detail' is not valid obj")

    def get_response(self):
        return JSONResponse(status_code=self.status_code, content=self.content)


class FailedActionException(AppException):
    def __init__(self, action: str = None):
        detail = f"Failed to {action}." if action is not None else f"Failed the action."
        super().__init__(status_code=500, detail=detail)
