from .authentication.routers import auth
from src.token.router import token
from .user.routers import user


routes = [
    user,
    # auth,
    token
        ]