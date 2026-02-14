from .base_exceptions import AppException, FailedActionException


class UserNotFoundException(AppException):
    def __init__(self, user_id: int | None = None):
        detail = f"User with ID {user_id} not found" if user_id is not None else "User not found"
        super().__init__(status_code=404, detail=detail)


class UserHasNotPermission(AppException):
    def __init__(self, action: str | None = None):
        detail = f"User does not have permission to {action}." if action is not None \
            else "User does not have permission to action."
        super().__init__(status_code=403, detail=detail)


class UserDeletedSuccessException(AppException):
    def __init__(self, user_id):
        detail = f"User with id {user_id} was deleted" if user_id else "User deleted"
        super().__init__(status_code=204, detail=detail)


class UserFailedCreateException(FailedActionException):
    def __init__(self):
        super().__init__(action="create user")


class UserFailedUpdateException(FailedActionException):
    def __init__(self):
        super().__init__(action="update user data")


class UserFailedDeleteException(FailedActionException):
    def __init__(self):
        super().__init__(action="delete user")
