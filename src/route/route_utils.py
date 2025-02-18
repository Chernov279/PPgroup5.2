from src.exceptions.base_exceptions import AppException
from src.route.route_schemas import RouteDetailOut
from src.utils.schema_utils import add_internal_params


def create_route_detail_by_model(route, route_details=None, raise_exception=False):
    detail_route = add_internal_params(route, RouteDetailOut, raise_exception=raise_exception)

    if isinstance(route_details, dict):
        for key, value in route_details.items():
            if hasattr(detail_route, key):
                setattr(detail_route, key, value)
            elif raise_exception:
                raise AppException()
    else:
        setattr(detail_route, "user_name", route.user.name)

        len_coordinates = len(route.coordinates)
        setattr(detail_route, "amount_points", len_coordinates)

        ratings = route.ratings
        len_ratings = len(ratings)
        setattr(detail_route, "amount_ratings", len_ratings)
        if len_ratings != 0:
            avg_rating = round(sum(map(lambda x: x.value, ratings)) / len_ratings, 2)
            setattr(detail_route, "avg_rating", avg_rating)
        else:
            setattr(detail_route, "avg_rating", None)
    return detail_route
