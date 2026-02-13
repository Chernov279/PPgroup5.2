from fastapi import APIRouter
from .auth import auth
from .users import users
from .routes import routes
from .ratings import ratings

v1_router = APIRouter(prefix="/api/v1")

v1_router.include_router(auth)
v1_router.include_router(users)
v1_router.include_router(routes)
v1_router.include_router(ratings)