from src.exceptions.base_exceptions import AppException


class NotFoundException(AppException):
    def __init__(self, model):
        detail = f"{model.__name__} not found"
        super().__init__(status_code=404, detail=detail)