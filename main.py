import datetime
from fastapi import FastAPI, Depends, HTTPException
from geopy.distance import great_circle as GC

from fastapi.middleware.cors import CORSMiddleware
from PPgroup5.pythonBackEnd.auth.auth import router
from PPgroup5.pythonBackEnd.current_user.me import profile
from PPgroup5.pythonBackEnd.models.models import OtherUserOut, MyUserOut, EstimationGet, RouteOut
from PPgroup5.pythonBackEnd.database.database import User, Route, Coordinate, Estimation, get_db, Session
from PPgroup5.pythonBackEnd.schemas.schemas import not_found_error, Route_Data, user_search, route_search, time_redakt, \
    avg_estimation, get_lock_by_cords

app = FastAPI(title='Veloapp')
app.include_router(router)
app.include_router(profile)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["*"],
)


@app.get("/")
def get_routes(session: Session = Depends(get_db)):
    """
    Получение списка маршрутов.

    Возвращает:
    - Статус выполнения запроса.
    - Список маршрутов с подробной информацией.
    """
    # добавить pages
    routes = session.query(Route).filter(Route.user_id != 0).all()
    routes = sorted(routes[-15:], key=lambda x: x.route_id)
    routes_out = []
    id = 1
    for route in routes[::-1]:

        user = session.query(User).filter(User.id == route.user_id).first()
        user_name = user.name
        if user.surname:
            user_name = f"{user.name} {user.surname}"

        routes_out.append(
                RouteOut(
                    id=id,
                    users_travel_time=time_redakt(route.users_travel_time),
                    comment=route.comment,
                    route_id=route.route_id,
                    user_id=route.user_id,
                    distance=round(route.distance, 2) if route.distance else 0,
                    avg_travel_time_on_foot=route.avg_travel_time_on_foot,
                    avg_travel_velo_time=route.avg_travel_velo_time,
                    avg_estimation=avg_estimation(route.route_id, session),
                    user_name=user_name,
                    created_time=str(route.operation_time)
                        )
                    )
        id += 1
    return {"status": "success",
            "data": routes_out,
            "details": None
            }


@app.get("/users/{user_id}")
def get_user_by_id(user_id: int, session: Session = Depends(get_db)):
    """
    Получение информации о пользователе по его ID.

    Параметры:
    - user_id (int): Идентификатор пользователя.

    Возвращает:
    - Статус выполнения запроса.
    - Неполная информация о пользователе и его маршрутах.
    """
    # профиль другого пользователя
    user = user_search(user_id, session)
    routes = session.query(Route).filter(Route.user_id == user_id).all()
    all_distance = 0
    all_travel_time = 0
    if not routes:
        routes_out = None
        all_avg_estimations = None
    else:
        all_avg = []
        routes_out = []
        id = 1
        for route in routes[::-1]:
            if route.distance:
                all_distance += route.distance
            if route.users_travel_time:
                all_travel_time += route.users_travel_time
            if avg_estimation(route.route_id, session):
                all_avg.append(avg_estimation(route.route_id, session))
            user_name = user.name
            if user.surname:
                user_name = f"{user.name} {user.surname}"
            routes_out.append(
                    RouteOut(
                        id=id,
                        users_travel_time=time_redakt(route.users_travel_time),
                        comment=route.comment,
                        route_id=route.route_id,
                        user_id=route.user_id,
                        distance=round(route.distance, 2) if route.distance else 0,
                        avg_travel_time_on_foot=route.avg_travel_time_on_foot,
                        avg_travel_velo_time=route.avg_travel_velo_time,
                        avg_estimation=avg_estimation(route.route_id, session),
                        user_name=user_name,
                        created_time=str(route.operation_time)
                            )
                        )
            id += 1
        if len(all_avg) == 0:
            all_avg_estimations = None
        else:
            all_avg_estimations = round(sum(all_avg) / len(all_avg), 2)

    return {"status": "success",
            "data": {
                "user": OtherUserOut(
                    id=user.id,
                    name=user.name,
                    surname=user.surname,
                    patronymic=user.patronymic,
                    location=user.location,
                    sex=user.sex,
                    authorized_time=str(user.authorized_time)
                ),
                "routes": routes_out,
                "all_distance": round(all_distance, 2),
                "all_avg_estimations": all_avg_estimations,
                "all_travel_time": time_redakt(all_travel_time)
                },
            "details": None
            }


@app.get("/route/{route_id}")
def get_route(route_id: int, user_id: int = None, session: Session = Depends(get_db)):
    """
    Получение информации о маршруте по его ID и ID пользователя, если дан.

    Параметры:
    - route_id (int): Идентификатор маршрута.
    - user_id (int, опционально): Идентификатор пользователя для проверки избранных маршрутов.

    Возвращает:
    - Статус выполнения запроса.
    - Подробная информация о маршруте.
    """
    user = session.query(User).filter(User.id == user_id).first()
    route = route_search(route_id, session)
    coordinates = session.query(Coordinate).filter(Coordinate.route_id == route_id).all()
    coordinates.sort(key=lambda x: x.cord_id)
    coordinates = list(map(lambda x: (x.longitude, x.latitude), coordinates))
    is_favorite_route = None
    if user:
        is_favorite_route = route_id in user.favorite_routes
    user = session.query(User).filter(User.id == route.user_id).first()
    user_name = user.name
    if user.surname:
        user_name = f"{user.name} {user.surname}"
    return {
        "status": "success",
        "data": {"route": RouteOut(
            id=1,
            users_travel_time=time_redakt(route.users_travel_time),
            comment=route.comment,
            route_id=route.route_id,
            user_id=route.user_id,
            distance=round(route.distance, 2),
            avg_estimation=avg_estimation(route_id, session),
            avg_travel_time_on_foot=route.avg_travel_time_on_foot,
            avg_travel_velo_time=route.avg_travel_velo_time,
            user_name=user_name,
            created_time=str(route.operation_time)
        ),
                 "coordinates": coordinates,
                 "is_favorite_route": is_favorite_route,
                 },
        "details": None
    }


@app.post("/route/{route_id}")
def add_remove_route_to_favorite(route_id: int, user_id: int, session: Session = Depends(get_db)):
    user = user_search(user_id, session)
    route_search(route_id, session)
    if user.favorite_routes is None:
        user.favorite_routes = [route_id]
        is_favorite = False
    elif route_id not in user.favorite_routes:
        user.favorite_routes = user.favorite_routes + [route_id]
        is_favorite = True
    else:
        user.favorite_routes = list(filter(lambda x: x != route_id, user.favorite_routes))
        is_favorite = False
    session.commit()
    session.refresh(user)
    return {
        "status": "success",
        "data": {
            "is_favorite": is_favorite,
            "user_favorite_routes": user.favorite_routes},
        "details": None
    }


@app.get("/token_mobile/{token_mobile}")
def check_token(token_mobile: str, session: Session = Depends(get_db)):
    """
    Проверка токена мобильного приложения.

    Параметры:
    - token_mobile (str): Токен мобильного приложения.

    Возвращает:
    - Статус выполнения запроса.
    - Информация о пользователе.
    """
    user = session.query(User).filter(User.token_mobile == token_mobile).first()
    not_found_error(user, "Token_mobile")
    return {"status": "success",
            "data": MyUserOut(
                id=user.id,
                name=user.name,
                email=user.email,
                telephone_number=user.telephone_number,
                surname=user.surname,
                patronymic=user.patronymic,
                location=user.location,
                sex=user.sex,
                token_mobile=user.token_mobile,
                authorized_time=str(user.authorized_time)
            ),
            "details": None
            }


# estimations
@app.post("/routes/{route_id}/estimation")
def create_estimation(user_id: int, estimator_data: EstimationGet, session: Session = Depends(get_db)):
    """
    Создание новой оценки для маршрута.

    Параметры:
    - user_id (int): Идентификатор пользователя, оставляющего оценку.
    - estimator_data (EstimationGet): Данные оценки.

    Возвращает:
    - Статус выполнения запроса.
    - Информация о созданной оценке.
    """
    route = session.query(Route).filter(Route.route_id == estimator_data.route_id).first()
    not_found_error(route, "Route")
    new_estimation = Estimation(
        user_id=route.user_id,
        route_id=estimator_data.route_id,
        estimation_value=estimator_data.estimation,
        estimator_id=user_id,
        comment=estimator_data.comment,
        datetime=datetime.datetime.now()
    )
    session.add(new_estimation)
    session.commit()
    return {
        "status": "success",
        "data": {
            "estimator_id": new_estimation.estimator_id,
            "route_id": new_estimation.route_id,
            "estimation_id": new_estimation.estimation_id,
            "estimation_value": new_estimation.estimation_value,
            "datetime": new_estimation.datetime,
            "comment": new_estimation.comment
        },
        "details": None
    }


@app.get("/routes/{route_id}/estimation")
def get_estimations_by_route_id(user_id: int, route_id: int, session: Session = Depends(get_db)):
    """
    Получение списка оценок для маршрута по его ID.

    Параметры:
    - user_id (int): Идентификатор пользователя.
    - route_id (int): Идентификатор маршрута.

    Возвращает:
    - Статус выполнения запроса.
    - Список оценок и среднее значение оценок.
    """
    estimations = session.query(Estimation).filter(Estimation.route_id == route_id).all()
    if not estimations:
        return {"status": "success",
                "data": {
                    "estimations": None,
                    "average_value": None,
                    "len_estimations": None,
                    "my_estimation_value": None
                },
                "details": None}
    len_estimations = len(estimations)
    average_value = sum([estimation.estimation_value for estimation in estimations]) / len_estimations
    my_estimation = session.query(Estimation).filter(Estimation.estimator_id == user_id,
                                                     Estimation.route_id == route_id).first()
    my_estimation_value = None
    if my_estimation:
        my_estimation_value = my_estimation.estimation_value
    return {
        "status": "success",
        "data": {
            "estimations": estimations,
            "average_value": average_value,
            "len_estimations": len_estimations,
            "my_estimation_value": my_estimation_value
        },
        "details": None
    }


@app.put("/routes/{route_id}/estimation/{estimation.estimation_id}")
def update_estimation(estimator_id: int, route_id: int, estimation_value: float, session: Session = Depends(get_db)):
    """
     Обновление существующей оценки маршрута.

     Параметры:
     - estimator_id (int): Идентификатор пользователя, обновляющего оценку.
     - route_id (int): Идентификатор маршрута.
     - estimation_value (float): Новое значение оценки.

     Возвращает:
     - Статус выполнения запроса.
     - Обновленная информация об оценке.
     """
    estimation = session.query(Estimation).filter(
        Estimation.route_id == route_id, Estimation.estimator_id == estimator_id).first()
    not_found_error(estimation, "Estimation")
    estimation.estimation_value = estimation_value
    estimation.datetime = datetime.datetime.now()
    session.commit()
    session.refresh(estimation)
    return {
        "status": "success",
        "data": {
            "estimation": estimation
        },
        "details": None
    }


@app.delete("/routes/{route_id}/estimation/{estimation.estimation_id}")
def delete_estimation(estimation_id: int, session: Session = Depends(get_db)):
    """
    Удаление оценки маршрута.

    Параметры:
    - estimation_id (int): Идентификатор оценки.

    Возвращает:
    - Статус выполнения запроса.
    """
    estimation = session.query(Estimation).filter(Estimation.estimation_id == estimation_id).first()
    not_found_error(estimation, "Estimation")
    session.delete(estimation)
    session.commit()
    return {
        "status": "success",
        "data": None,
        "details": None
    }


@app.post("/route/")
def post_route_arrow(route_info: Route_Data, session: Session = Depends(get_db)):
    """
    Создание нового маршрута.

    Параметры:
    - route_info (Route_Data): Данные маршрута.

    Возвращает:
    - Статус выполнения запроса.
    - Информация о созданном маршруте.
    """
    user = session.query(User).filter(User.token_mobile == route_info.token_mobile).first()
    not_found_error(user, "User")
    if len(route_info.latitude_longitude) < 2:
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "data": None,
            "details": None
        })

    dist = 0
    for i in range(len(route_info.latitude_longitude)-1):
        dist += GC((route_info.latitude_longitude[i][0], route_info.latitude_longitude[i][1]), (route_info.latitude_longitude[i+1][0], route_info.latitude_longitude[i+1][1])).km
    new_route = Route(
        user_id=user.id,
        distance=dist,
        users_travel_time=round(route_info.users_travel_time / 1000, 0),
        operation_time=datetime.datetime.now()
    )
    session.add(new_route)
    session.commit()
    session.refresh(new_route)
    for cord in range(len(route_info.latitude_longitude)):
        new_coordinate = Coordinate(
            route_id=new_route.route_id,
            user_id=user.id,
            latitude=route_info.latitude_longitude[cord][0],
            longitude=route_info.latitude_longitude[cord][1],
        )
        session.add(new_coordinate)
    session.commit()
    session.refresh(new_route)
    return {
        "status": "success",
        "data": {"route": new_route},
        "details": None
    }
