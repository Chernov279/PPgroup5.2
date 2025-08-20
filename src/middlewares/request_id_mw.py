import uuid
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response
from ..utils.logging_utils import set_request_id

logger = logging.getLogger(__name__)


class RequestIdMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, header_name: str = "X-Request-ID"):
        super().__init__(app)
        self.header_name = header_name

    async def dispatch(self, request: Request, call_next):
        req_id = request.headers.get(self.header_name) or str(uuid.uuid4())
        set_request_id(req_id)
        try:
            response: Response = await call_next(request)
        except Exception:
            logger.exception("Unhandled exception while processing request")
            raise
        response.headers[self.header_name] = req_id
        return response
