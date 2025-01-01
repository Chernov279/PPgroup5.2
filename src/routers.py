from .authentication.auth_router import auth
from .token.token_router import token
from .user.user_router import user


routers = [
    user,
    auth,
    token,
]
