from src.redis.avg_rat_cache import AvgRatingCache
from src.redis.redis_helper import get_redis, redis
from src.redis.token_cache import TokenCache


async def get_token_cache():
    async with get_redis(redis) as redis_cli:
        yield TokenCache(redis_cli)


async def get_avg_rat_cache():
    async with get_redis(redis) as redis_cli:
        yield AvgRatingCache(redis_cli)
