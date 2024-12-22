from geopy import Nominatim
from pydantic import BaseModel, validator
from typing import List
from fastapi import HTTPException, Depends

from src.database.database import User, Route, Coordinate, Estimation, Session, get_db


class Route_Data(BaseModel):
    """
    Модель данных маршрута.

    Поля:
    - users_travel_time: Время путешествия.
    - latitude_longitude: Список координат (широта и долгота).
    - token_mobile: Мобильный токен пользователя.
    """
    users_travel_time: int
    latitude_longitude: List[List[float]]
    token_mobile: str

    @validator('latitude_longitude', each_item=True)
    def check_list_length(cls, v):
        """
        Валидатор для проверки длины вложенного списка координат.

        Аргументы:
        - v: Список координат.

        Исключения:
        - HTTPException: Если длина списка не равна 2.
        """
        if len(v) != 2:
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": None,
                "details": "len is not 2"
                })
        return v


def not_found_error(arg, name):
    """
    Функция для генерации ошибки, если объект не найден.

    Аргументы:
    - arg: Объект, который нужно проверить.
    - name: Имя объекта для отображения в сообщении об ошибке.

    Исключения:
    - HTTPException: Если объект не найден.
    """
    if not arg:
        raise HTTPException(status_code=404, detail={
            "status": "error",
            "data": None,
            "details": f"{name} not found"
        })


def user_search(user_id, session: Session = Depends(get_db)):
    """
    Функция для поиска пользователя по ID.

    Аргументы:
    - user_id: ID пользователя.

    Возвращает:
    - Пользователь (User) или вызывает ошибку, если пользователь не найден.
    """
    user = session.query(User).filter(User.id == user_id).first()
    not_found_error(user, "User")
    return user


def route_search(route_id, session: Session = Depends(get_db)):
    """
    Функция для поиска маршрута по ID.

    Аргументы:
    - route_id: ID маршрута.

    Возвращает:
    - Маршрут (Route) или вызывает ошибку, если маршрут не найден.
    """
    route = session.query(Route).filter(Route.route_id == route_id).first()
    not_found_error(route, "Route")
    return route


def coordinate_search(cord_id, session: Session = Depends(get_db)):
    """
    Функция для поиска координаты по ID.

    Аргументы:
    - cord_id: ID координаты.

    Возвращает:
    - Координата (Coordinate) или вызывает ошибку, если координата не найдена.
    """
    coordinate = session.query(Coordinate).filter(Coordinate.cord_id == cord_id).first()
    not_found_error(coordinate, "Coordinate")
    return coordinate


def get_lock_by_cords(latitude, longitude):
    """
    Функция для получения названия местоположения по координатам.

    Аргументы:
    - latitude: Широта.
    - longitude: Долгота.

    Возвращает:
    - Название местоположения или None, если местоположение не найдено.
    """
    try:
        geoLoc = Nominatim(user_agent="GetLoc")
        locname = geoLoc.reverse(f"{str(latitude)}, {str(longitude)}")
        return str(locname)
    except:
        return None


def time_redakt(time):
    """
    Функция для форматирования секунд в часы и минуты.

    Аргументы:
    - time: Время в секундах.

    Возвращает:
    - Время в формате Часы:Минуты:Секунды.
    """
    if not time:
        return "0:00:00"
    minutes = "0" + str((time % 3600) // 60)
    seconds = "0" + str(time % 60)
    return f"{time // 3600}:{minutes[-2:]}:{seconds[-2:]}"


def avg_estimation(route_id, session: Session = Depends(get_db)):
    """
    Функция для высчитывания средней оценки маршрута.

    Аргументы:
    - route_id: id маршрута.

    Возвращает:
    - среднюю оценку маршрута.
    """
    estimations = session.query(Estimation).filter(Estimation.route_id == route_id).all()
    if estimations:
        return round(sum([estimation.estimation_value for estimation in estimations]) / len(estimations), 2)
    return None
