from src.exceptions.base_exceptions import AppException


def valid_limit(limit):
    if not isinstance(limit, int):
        raise AppException(detail="limit not integer")
    if limit < 0:
        raise AppException(detail="limit less than 0")
    if limit > 2 ** 32 - 1:
        raise AppException(detail="limit more than 2**32, not int32")


def valid_offset(offset):
    if not isinstance(offset, int):
        raise AppException(detail="offset not integer")
    if offset < 0:
        raise AppException(detail="offset less than 0")
    if offset > 2 ** 32 - 1:
        raise AppException(detail="offset more than 2**32, not int32")
