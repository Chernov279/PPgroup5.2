from redis.asyncio import Redis
from contextlib import asynccontextmanager

from src.config import settings
from src.redis.redis_config import settings_redis

redis = Redis.from_url(settings.REDIS_URL, decode_responses=True)

redis_dbs = (redis,)


@asynccontextmanager
async def get_redis(redis):
    try:
        yield redis
    finally:
        await redis.close()

