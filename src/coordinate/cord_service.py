from typing import Annotated, List

from fastapi import Depends

from ..config.database.db_helper import get_db
from ..config.token_config import oauth2_scheme
from .cord_repository import CoordinateRepository
from .cord_schemas import CoordinatesIn, CoordinatesInDB
from ..exceptions.coordinate_exceptions import CordsBadRequest, CordsNotFoundException, CordsAddedException, \
    CordsDeletedException
from ..exceptions.route_exceptions import RouteNotFoundException
from ..exceptions.token_exceptions import InvalidTokenUserException
from ..exceptions.user_exceptions import UserHasNotPermission
from ..unit_of_work.route_uow import RouteUOW
from ..unit_of_work.token_uow import TokenUOW


class CoordinateService:
    def get_all_cords(
            self,
            db_session=Depends(get_db)
    ):
        cords = CoordinateRepository(db_session).get_all_cords()
        return cords

    def get_cords_by_route(
            self,
            route_id: int,
            offset: int = 0,
            limit: int = 30,
            db_session=Depends(get_db)
    ):
        if not (0 < limit <= 100):
            limit = 30
        cords = CoordinateRepository(db_session).get_cords_by_route_id(route_id, offset, limit)
        if not cords:
            raise CordsNotFoundException(route_id)
        return cords

    def add_cords_by_route(
            self,
            route_id: int,
            cords: List[CoordinatesIn],
            token: Annotated[str, Depends(oauth2_scheme)],
            db_session=Depends(get_db),
            start_from_end: bool | None = True,

    ):
        if not cords:
            raise CordsBadRequest(route_id)

        user_id = TokenUOW(db_session).user_exists_by_token_uow(token)
        if not user_id:
            raise InvalidTokenUserException(user_id)

        user_id_route = RouteUOW(db_session).get_user_id_by_route_id(route_id)
        if not user_id_route:
            raise RouteNotFoundException(user_id_route)

        if user_id != user_id_route:
            raise UserHasNotPermission("change route coordinates of other user")

        cord_repo = CoordinateRepository(db_session)

        if start_from_end:
            latest_order = cord_repo.get_latest_order(route_id)
            print(latest_order)
            if latest_order is None:
                latest_order = 0
            else:
                latest_order += 1
            cords_db = [CoordinatesInDB(
                route_id=route_id,
                user_id=user_id,
                latitude=cords[order].latitude,
                longitude=cords[order].longitude,
                order=order + latest_order
            )
                for order in range(len(cords))
            ]
        else:
            first_order = cord_repo.get_first_order(route_id)
            if first_order is None:
                first_order = 0
            else:
                first_order -= 1
            cords_db = [CoordinatesInDB(
                route_id=route_id,
                user_id=user_id,
                latitude=cords[order].latitude,
                longitude=cords[order].longitude,
                order=first_order - order
            )
                for order in range(len(cords))
            ]
        for cord in cords_db:
            print(cord)
        cord_repo.add_cords(
            cords_db
        )
        raise CordsAddedException()

    def delete_all_cords_by_route(
            self,
            route_id,
            token: Annotated[str, Depends(oauth2_scheme)],
            db_session=Depends(get_db)
    ):
        user_id = TokenUOW(db_session).user_exists_by_token_uow(token)
        if not user_id:
            raise InvalidTokenUserException(user_id)

        user_id_route = RouteUOW(db_session).get_user_id_by_route_id(route_id)
        if not user_id_route:
            raise RouteNotFoundException(route_id)

        if user_id != user_id_route:
            raise UserHasNotPermission("delete route coordinates of other user")

        CoordinateRepository(db_session).delete_cords(
            route_id
        )

        raise CordsDeletedException()
