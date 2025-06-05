import json
from typing import Optional

DEFAULT_TTL = 24 * 60 * 60


class TokenCache:
    def __init__(self, redis_client):
        self.redis = redis_client

    def _refresh_token_key(self, jti: str) -> str:
        return f"refresh:{jti}"

    async def cache_refresh_token(self, jti: str, user_id: int):
        key = self._refresh_token_key(jti)
        value = json.dumps({"user_id": user_id})
        await self.redis.set(key, value, ex=DEFAULT_TTL)

    async def is_refresh_token_valid(self, jti: str) -> bool:
        key = self._refresh_token_key(jti)
        return await self.redis.exists(key) == 1

    async def get_user_id_by_refresh_token(self, jti: str) -> Optional[int]:
        key = self._refresh_token_key(jti)
        data = await self.redis.get(key)
        if not data:
            return None
        try:
            return json.loads(data).get("user_id")
        except (json.JSONDecodeError, TypeError):
            return None

    async def revoke_token(self, jti: str):
        key = self._refresh_token_key(jti)
        await self.redis.delete(key)
