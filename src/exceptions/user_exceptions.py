from .base_exceptions import AppException


class UserNotFoundException(AppException):
    def __init__(self, user_id: int = None):
        detail = f"User with ID {user_id} not found" if user_id is not None else f"User not found"
        super().__init__(status_code=404, detail=detail)


class UserHasNotPermission(AppException):
    def __init__(self, action: str = None):
        detail = f"User does not have permission to {action}." if action is not None \
            else f"User does not have permission to action."
        super().__init__(status_code=403, detail=detail)


class UserFailedActionException(AppException):
    def __init__(self, action: str = None):
        detail = f"Failed to {action}." if action is not None else f"Failed the action."
        super().__init__(status_code=400, detail=detail)
