from .authentication.routers import auth
from .user.routers import user


routes = [
    user,
    auth,
        ]