from .base_exceptions import AppException


class RouteNotFoundException(AppException):
    def __init__(self, route_id: int = None):
        detail = f"Route with ID {route_id} not found" if route_id is not None \
            else "Route not found"
        super().__init__(status_code=404, detail=detail)


class RouteFailedActionException(AppException):
    def __init__(self, action: str = None):
        detail = f"Failed to {action}." if action is not None else "Failed the action."
        super().__init__(status_code=400, detail=detail)
