from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base_model import BaseModel


class User(BaseModel):
    # """
    # Модель пользователя в базе данных.
    #
    # Поля:
    # id (int): Уникальный идентификатор пользователя.
    # name (str): Имя пользователя.
    # email (str): Email пользователя.
    # telephone_number (str): Номер телефона пользователя.
    # surname (str): Фамилия пользователя.
    # patronymic (str): Отчество пользователя.
    # location (str): Местоположение пользователя (город проживания).
    # sex (str): Пол пользователя (male = мужчина, female = женщина).
    # favorite_routes (list[int]): Список избранных маршрутов.
    # hashed_password (str): Хэшированный пароль пользователя.
    # authorizated_at (DateTime): Время авторизации пользователя.
    # birth (str): Дата рождения пользователя.
    # routes (relationship): Связь с маршрутами.
    # """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String)
    telephone_number = Column(String)
    surname = Column(String)
    patronymic = Column(String)
    location = Column(String)
    sex = Column(String)
    # TODO сделать отдельную модель для избранных роутов
    hashed_password = Column(String, nullable=False)
    authorized_time = Column(DateTime, default=func.now())
    last_updated_time = Column(DateTime, default=func.now(), onupdate=func.now())
    birth = Column(String)
    routes = relationship("Route", back_populates="user")
    ratings = relationship("Rating", back_populates="user")


class Route(BaseModel):
    # """
    # Модель маршрута.
    #
    # Поля:
    # route_id (int): Уникальный идентификатор маршрута.
    # user_id (int): ID пользователя, создавшего маршрут.
    # distance (float): Расстояние маршрута.
    # users_travel_time (int): Время путешествия пользователя (в секундах).
    # avg_travel_time_on_foot (int): Среднее время путешествия пешком.
    # avg_travel_velo_time (int): Среднее время путешествия на велосипеде.
    # comment (str): Комментарий к маршруту.
    # operation_time (DateTime): Время создания маршрута.
    # user (relationship): Связь с пользователем.
    # estimations (relationship): Связь с оценками маршрута.
    # coordinates (relationship): Связь с координатами маршрута.
    # """
    __tablename__ = 'routes'
    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    distance = Column(Float)
    users_travel_time = Column(Integer)
    users_travel_speed = Column(Integer)
    users_transport = Column(String)
    comment = Column(String)
    created_time = Column(DateTime, default=func.now())
    locname_start = Column(String)
    locname_finish = Column(String)
    user = relationship("User", back_populates="routes")
    ratings = relationship("Rating", back_populates="route")
    coordinates = relationship("Coordinate", back_populates="routes")


class Coordinate(BaseModel):
    # """
    # Модель координаты.
    #
    # Поля:
    # cord_id (int): Уникальный идентификатор координаты.
    # route_id (int): ID маршрута.
    # user_id (int): ID пользователя, добавившего координату.
    # latitude (float): Широта.
    # longitude (float): Долгота.
    # order (int): Порядок координаты в маршруте.
    # locname (str): Название местоположения.
    # operation_time (DateTime): Время добавления координаты.
    # routes (relationship): Связь с маршрутом.
    # """
    __tablename__ = 'coordinates'
    cord_id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    route_id = Column(Integer, ForeignKey('routes.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    routes = relationship("Route", back_populates="coordinates")


class Rating(BaseModel):
    # """
    # Модель оценки маршрута.
    #
    # Поля:
    # estimation_id (int): Уникальный идентификатор оценки.
    # route_id (int): ID маршрута.
    # user_id (int): ID пользователя, создавшего маршрут.
    # estimation_value (int): Значение оценки.
    # estimator_id (int): ID пользователя, оценившего маршрут.
    # datetime (DateTime): Время оценки.
    # comment (str): Комментарий к оценке.
    # route (relationship): Связь с маршрутом.
    # """
    __tablename__ = 'ratings'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    route_id = Column(Integer, ForeignKey('routes.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    value = Column(Integer, nullable=False)
    created_time = Column(DateTime, default=func.now())
    comment = Column(String)
    route = relationship("Route", back_populates="ratings")
    user = relationship("User", back_populates="ratings")
