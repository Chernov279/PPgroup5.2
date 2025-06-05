import json

from redis.asyncio import Redis
from typing import Optional
from datetime import timedelta


class AvgRatingCache:
    def __init__(self, redis_client: Redis, ttl: timedelta = timedelta(hours=1)):
        self.redis = redis_client
        self.ttl = ttl

    def _make_key(self, route_id: int) -> str:
        return f"rating:avg:{route_id}"

    async def set_rating(self, route_id: int, rating: float) -> None:
        key = self._make_key(route_id)
        await self.redis.set(name=key, value=rating, ex=self.ttl)

    async def get_rating(self, route_id: int) -> Optional[float]:
        key = self._make_key(route_id)
        data = await self.redis.get(key)
        if not data:
            return None
        return data

    async def invalidate(self, route_id: int) -> None:
        key = self._make_key(route_id)
        await self.redis.delete(key)
