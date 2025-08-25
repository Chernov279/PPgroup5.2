import asyncio
import logging

import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings_project
from src.config.logging_config import configure_logging
from src.kafka.consumers import kafka_consumers
from src.kafka.producer import kafka_producer
from src.middlewares.request_id_mw import RequestIdMiddleware
from src.routers import routers

configure_logging(level="INFO")
logger = logging.getLogger(__name__)


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


app = get_application()
app.add_middleware(RequestIdMiddleware)


@app.on_event("startup")
async def startup_event():
    await kafka_producer.start()
    await asyncio.gather(*(cons.start() for cons in kafka_consumers))
    logger.info("Event Startup ended")


@app.on_event("shutdown")
async def shutdown_event():
    await asyncio.gather(*(cons.stop() for cons in kafka_consumers), return_exceptions=True)
    await kafka_producer.stop()
    logger.info("Event shutdown ended")

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", reload=True)
