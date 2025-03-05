from typing import Any

from .cord_schemas import CoordinateInternal, CoordinateCreateIn
from ..utils.schema_utils import add_internal_params


def create_cords_create_internal(
        schemas: list[Any],
        user_id,
        route_id,
        order,
):

    coordinates_internal = [add_internal_params(
            schema=schemas[index],
            cls_internal=CoordinateInternal(),
            raise_exception=False,
            user_id=user_id,
            route_id=route_id,
            order=index + order
        ) for index in range(len(schemas))
    ]
    return coordinates_internal
