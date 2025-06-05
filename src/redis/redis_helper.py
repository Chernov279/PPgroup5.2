from redis.asyncio import Redis
from contextlib import asynccontextmanager

from src.redis.redis_config import settings_redis

redis0 = Redis.from_url(settings_redis.REDIS_URL0, decode_responses=True)
redis1 = Redis.from_url(settings_redis.REDIS_URL1, decode_responses=True)


@asynccontextmanager
async def get_redis(redis):
    try:
        yield redis
    finally:
        await redis.close()

