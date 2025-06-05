from redis.asyncio import Redis
from contextlib import asynccontextmanager

from src.redis.redis_config import settings_redis

redis = Redis.from_url(settings_redis.REDIS_URL, decode_responses=True)


@asynccontextmanager
async def get_redis():
    try:
        yield redis
    finally:
        await redis.close()
