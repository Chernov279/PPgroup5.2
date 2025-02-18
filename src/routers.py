from .authentication.auth_router import auth
# from .coordinate.cord_router import coordinate
# from .rating_route.rat_router import rating
from .route.route_router import route
from .token.token_router import token
from .user.user_router import user


routers = [
    user,
    auth,
    token,
    route,
    # rating,
    # coordinate
]
