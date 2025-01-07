from src.exceptions.base_exceptions import AppException


class RatingNotFoundException(AppException):
    def __init__(self, route_id: int = None, user_id: int = None):
        detail = f"Rating with Route ID {route_id} by user {user_id} not found" if route_id and user_id else f"Rating not found"
        super().__init__(status_code=404, detail=detail)


class RatingAlreadyExistsException(AppException):
    def __init__(self, route_id: int = None, user_id: int = None):
        detail = f"Rating with Route ID {route_id} by user {user_id} already exists" if route_id and user_id else f"Rating already exists"
        super().__init__(status_code=404, detail=detail)


class RatingFailedActionException(AppException):
    def __init__(self, action: str = None):
        detail = f"Failed to {action}." if action is not None else f"Failed the rating action."
        super().__init__(status_code=400, detail=detail)
