from src.exceptions.base_exceptions import ValidationException


def valid_limit(limit):
    if not isinstance(limit, int):
        raise ValidationException(field="valid_limit", message="limit not integer")
    if limit < 0:
        raise ValidationException(field="valid_limit", message="limit less than 0")
    if limit > 2 ** 32 - 1:
        raise ValidationException(field="valid_limit", message="limit more than 2**32, not int32")


def valid_offset(offset):
    if not isinstance(offset, int):
        raise ValidationException(field="valid_offset", message="offset not integer")
    if offset < 0:
        raise ValidationException(field="valid_offset", message="offset less than 0")
    if offset > 2 ** 32 - 1:
        raise ValidationException(field="valid_offset", message="offset more than 2**32, not int32")
