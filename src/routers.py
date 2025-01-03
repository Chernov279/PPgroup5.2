from .authentication.auth_router import auth
from .route.route_router import route
from .token.token_router import token
from .user.user_router import user


routers = [
    user,
    auth,
    token,
    route
]
