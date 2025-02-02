import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings_project
from .routers import routers


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


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", reload=True)
