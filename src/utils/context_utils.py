import contextvars
import logging

_request_id_ctx = contextvars.ContextVar("request_id", default="-")
_user_id_ctx = contextvars.ContextVar("user_id", default=None)


def set_request_id(rid: str) -> None:
    _request_id_ctx.set(rid)


def get_request_id() -> str:
    return _request_id_ctx.get("-")


def set_user_id(uid: str) -> None:
    _user_id_ctx.set(uid)


def get_user_id() -> str | None:
    return _user_id_ctx.get(None)


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = get_request_id()
        return True
    