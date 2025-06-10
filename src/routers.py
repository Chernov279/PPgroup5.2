from .healthcheck.healthcheck_router import healthcheck
from .authentication.auth_router import auth
from .coordinate.cord_router import coordinate
from .rating_route.rat_router import rating
from .route.route_router import route
from .token_app.token_router import token
from .user.user_router import user
from .user_activity.kafka_consumer import user_activity_kafka_consumer

routers = [
    user,
    auth,
    token,
    route,
    rating,
    coordinate,
    healthcheck
]

kafka_consumers = [
    user_activity_kafka_consumer
]
