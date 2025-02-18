from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base_model import BaseModel

# TODO Mapper, mapping
class User(BaseModel):
    # """
    # Модель пользователя в базе данных.
    #
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String, nullable=False)
    email = Column(String)  # UNIQUE
    telephone_number = Column(String)  # UNIQUE
    surname = Column(String)
    patronymic = Column(String)
    location = Column(String)
    sex = Column(String)
    # TODO сделать отдельную модель для избранных роутов
    hashed_password = Column(String, nullable=False)
    authorized_time = Column(DateTime, default=func.now())
    last_updated_time = Column(DateTime, default=func.now(), onupdate=func.now())
    birth = Column(String)
    # is_active = Column(Boolean)
    # last_active_time = Column(DateTime)
    # refresh_token_update_time = Column(Datetime)
    # status = Column(String)

    routes = relationship("Route", back_populates="user")
    ratings = relationship("Rating", back_populates="user")


class Route(BaseModel):
    # """
    # Модель маршрута.
    #
    __tablename__ = 'routes'

    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

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
    #
    # Модель координаты.
    #
    __tablename__ = 'coordinates'

    route_id = Column(Integer, ForeignKey('routes.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, primary_key=True)

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    order = Column(Integer, primary_key=True)
    # location = Column(String)

    routes = relationship("Route", back_populates="coordinates")


class Rating(BaseModel):
    # """
    # Модель оценки маршрута.
    #
    __tablename__ = 'ratings'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

    route_id = Column(Integer, ForeignKey('routes.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    value = Column(Integer, nullable=False)
    created_time = Column(DateTime, default=func.now())

    comment = Column(String)
    route = relationship("Route", back_populates="ratings")
    user = relationship("User", back_populates="ratings")
