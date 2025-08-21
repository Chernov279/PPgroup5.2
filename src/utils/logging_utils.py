import contextvars
import logging

_request_id_ctx = contextvars.ContextVar("request_id", default="-")


def set_request_id(rid: str) -> None:
    _request_id_ctx.set(rid)


def get_request_id() -> str:
    return _request_id_ctx.get("-")


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = get_request_id()
        return True
    