from .base_exceptions import AppException, NoContentResponse, FailedActionException


class CordsNotFoundException(AppException):
    def __init__(self, route_id: int | None= None):
        detail = f"coordinates with route ID {route_id} not found" if route_id is not None \
            else "Coordinates not found"
        super().__init__(status_code=404, detail=detail)


class CordPermissionException(AppException):
    def __init__(self, action):
        detail = f"You do not have permission to {action}." if action else "You do not have permission."

        super().__init__(status_code=400, detail=detail)


class CordFailedDeleteException(FailedActionException):
    def __init__(self):
        super().__init__(action="delete coordinate")


class CordsAddedException(NoContentResponse):
    def __init__(self):
        msg = "Coordinates successfully added to route"
        super().__init__(status_code=204, detail={"msg": msg})


class CordsDeletedException(NoContentResponse):
    def __init__(self):
        msg = "Coordinates successfully deleted from route"
        super().__init__(status_code=204, detail={"msg": msg})
