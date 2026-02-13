from asyncio import gather

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.healthcheck.dependencies import check_postgres, check_redis
from src.db.db_helper import get_db_session
# from src.kafka.consumers.consumers import kafka_consumers

health = APIRouter(prefix="/health", tags=["Health"])


# @healthcheck.get("/kafka", status_code=status.HTTP_200_OK)
# async def health_kafka():
#     await check_kafka(kafka_consumers)
#     return {"kafka": "ok"}

@health.get("/", status_code=status.HTTP_200_OK)
async def health_status():
    return {"status": "ok"}

@health.get("/redis", status_code=status.HTTP_200_OK)
async def health_redis():
    await check_redis()
    return {"redis": "ok"}


@health.get("/postgres", status_code=status.HTTP_200_OK)
async def health_postgres(db_session: AsyncSession = Depends(get_db_session)):
    await check_postgres(db_session)
    return {"postgres": "ok"}


@health.get("/all", status_code=status.HTTP_200_OK)
async def health_all(db_session: AsyncSession = Depends(get_db_session)):
    await gather(
        # check_kafka(kafka_consumers),
        check_redis(),
        check_postgres(db_session)
    )
    return {"status": "ok"}
