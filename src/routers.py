from .authentication.auth_routers import auth
from .token.token_routers import token
from .user.routers import user


routers = [
    user,
    auth,
    token,
]
