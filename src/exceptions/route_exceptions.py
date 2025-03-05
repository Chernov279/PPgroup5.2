from .base_exceptions import AppException, FailedActionException, NoContentResponse


class RouteDeletedSuccessResponse(NoContentResponse):
    def __init__(self, route_id: int = None):
        msg = f"Route with ID {route_id} was successfully deleted" if route_id else "Route was successfully deleted"
        super().__init__(status_code=204, detail={"msg": msg})


class RouteNotFoundException(AppException):
    def __init__(self, route_id: int = None):
        detail = f"Route with ID {route_id} not found" if route_id is not None \
            else "Route not found"
        super().__init__(status_code=404, detail=detail)


class RoutePermissionException(AppException):
    def __init__(self, action: str = None):
        detail = f"You do not have permission to {action} this route." if action else "You do not have permission."
        super().__init__(status_code=403, detail=detail)


class RouteFailedCreateException(FailedActionException):
    def __init__(self):
        super().__init__(action="create route")


class RouteFailedUpdateException(FailedActionException):
    def __init__(self):
        super().__init__(action="update route")


class RouteFailedDeleteException(FailedActionException):
    def __init__(self):
        super().__init__(action="delete route")
