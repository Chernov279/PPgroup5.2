import pytest

from src.exceptions.base_exceptions import AppException
from src.utils.database_utils import valid_limit, valid_offset


def test_valid_limit():
    valid_limit(0)
    valid_limit(100)
    valid_limit(2 ** 32 - 1)

    with pytest.raises(AppException, match="limit not integer"):
        valid_limit("100")
    with pytest.raises(AppException, match="limit less than 0"):
        valid_limit(-1)
    with pytest.raises(AppException) as exc_info:
        valid_limit(2 ** 32)
    assert "not int32" in str(exc_info.value)


def test_valid_offset():
    valid_offset(0)
    valid_offset(50)
    valid_offset(2 ** 32 - 1)

    with pytest.raises(AppException, match="offset not integer"):
        valid_offset("50")
    with pytest.raises(AppException, match="offset less than 0"):
        valid_offset(-1)
    with pytest.raises(AppException) as exc_info:
        valid_offset(2 ** 32)
    assert "not int32" in str(exc_info.value)
