import asyncio
from datetime import datetime, timezone

from fastapi import Depends
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from src.api.dependencies import get_refresh_token, get_token_sub_required


class UserActivityMiddleware(BaseHTTPMiddleware):
    """
    Middleware для обновления активности пользователя, выполняющего запрос.
    Получается id пользователя через его токен и выполняется обновление.
    """
    def __init__(
            self,
            app,
            service: ...
    ):
        super().__init__(app)
        self._service = service

    async def dispatch(self, request: Request, call_next):

        user_id = get_token_sub_required(request)
        if user_id:
            asyncio.create_task(
                self._service.update_user_activity_service(
                    user_id=user_id,
                    last_active_time=datetime.now(timezone.utc),
                    hard=False,
                )
            )

        response = await call_next(request)
        return response