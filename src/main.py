import asyncio

import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings_project
from src.kafka.producer import kafka_producer
from src.routers import routers, kafka_consumers


def get_application() -> FastAPI:
    application = FastAPI(
        title=settings_project.PROJECT_NAME,
        debug=settings_project.DEBUG
    )
    for router in routers:
        application.include_router(router)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings_project.CORS_ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return application


async def get_kafka_consumers():
    for consumer in kafka_consumers:
        await consumer.start()
        asyncio.create_task(consumer.consume())

app = get_application()


@app.on_event("startup")
async def startup_event():
    await kafka_producer.startup_connection()
    await get_kafka_consumers()


@app.on_event("shutdown")
async def shutdown_event():
    if kafka_producer:
        await kafka_producer.stop()

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", reload=True)