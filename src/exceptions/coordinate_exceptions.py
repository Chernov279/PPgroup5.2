from .base_exceptions import AppException, NoContentException


class CordsNotFoundException(AppException):
    def __init__(self, route_id: int = None):
        detail = f"coordinates with route ID {route_id} not found" if route_id is not None \
            else "Coordinates not found"
        super().__init__(status_code=404, detail=detail)


class CordsBadRequest(AppException):
    def __init__(self, route_id: int = None):
        detail = f"No coordinates with route ID {route_id}" if route_id is not None \
            else "No coordinates"
        super().__init__(status_code=400, detail=detail)


class CordsAddedException(NoContentException):
    def __init__(self):
        super().__init__(message="Coordinates successfully added to route")


class CordsDeletedException(NoContentException):
    def __init__(self):
        super().__init__(message="Coordinates successfully deleted from route")
