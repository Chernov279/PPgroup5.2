from asyncio import gather

from fastapi import APIRouter, status
from src.healthcheck.dependencies import check_kafka, check_redis, check_postgres
from src.kafka.consumers.consumers import kafka_consumers

healthcheck = APIRouter(prefix="/health", tags=["Healthcheck"])


@healthcheck.get("/kafka", status_code=status.HTTP_200_OK)
async def health_kafka():
    await check_kafka(kafka_consumers)
    return {"kafka": "ok"}


@healthcheck.get("/redis", status_code=status.HTTP_200_OK)
async def health_redis():
    await check_redis()
    return {"redis": "ok"}


@healthcheck.get("/postgres", status_code=status.HTTP_200_OK)
async def health_postgres():
    await check_postgres()
    return {"postgres": "ok"}


@healthcheck.get("/all", status_code=status.HTTP_200_OK)
async def health_all():
    await gather(
        check_kafka(kafka_consumers),
        check_redis(),
        check_postgres()
    )
    return {"status": "ok"}
