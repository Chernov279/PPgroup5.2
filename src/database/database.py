from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, Boolean, ARRAY
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

from config.configuration import settings

Base = declarative_base()
engine = create_engine(settings.database_url)
# Создание сессии для работы с базой данных
Session = sessionmaker(engine)
session = Session()


# Функция для получения сессии базы данных, которая автоматически закрывает сессию после использования
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


class User(Base):
    """
    Модель пользователя в базе данных.

    Поля:
    id (int): Уникальный идентификатор пользователя.
    name (str): Имя пользователя.
    email (str): Email пользователя.
    telephone_number (str): Номер телефона пользователя.
    surname (str): Фамилия пользователя.
    patronymic (str): Отчество пользователя.
    location (str): Местоположение пользователя (город проживания).
    sex (str): Пол пользователя (male = мужчина, female = женщина).
    favorite_routes (list[int]): Список избранных маршрутов.
    hashed_password (str): Хэшированный пароль пользователя.
    salt_hashed_password (str): Соль для хэширования пароля.
    token_mobile (str): Токен мобильного приложения.
    authorizated_at (DateTime): Время авторизации пользователя.
    birth (str): Дата рождения пользователя.
    routes (relationship): Связь с маршрутами.
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String)
    telephone_number = Column(String)
    surname = Column(String)
    patronymic = Column(String)
    location = Column(String)
    sex = Column(String)
    favorite_routes = Column(ARRAY(Integer), default=[])
    hashed_password = Column(String, nullable=False)
    salt_hashed_password = Column(String, nullable=False)
    token_mobile = Column(String, nullable=False)
    authorized_time = Column(DateTime)
    birth = Column(String)
    routes = relationship("Route", back_populates="user")


class Route(Base):
    """
    Модель маршрута.

    Поля:
    route_id (int): Уникальный идентификатор маршрута.
    user_id (int): ID пользователя, создавшего маршрут.
    distance (float): Расстояние маршрута.
    users_travel_time (int): Время путешествия пользователя (в секундах).
    avg_travel_time_on_foot (int): Среднее время путешествия пешком.
    avg_travel_velo_time (int): Среднее время путешествия на велосипеде.
    comment (str): Комментарий к маршруту.
    operation_time (DateTime): Время создания маршрута.
    user (relationship): Связь с пользователем.
    estimations (relationship): Связь с оценками маршрута.
    coordinates (relationship): Связь с координатами маршрута.
    """
    __tablename__ = 'routes'
    route_id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    distance = Column(Float)
    users_travel_time = Column(Integer)
    avg_travel_time_on_foot = Column(Integer)
    avg_travel_velo_time = Column(Integer)
    comment = Column(String)
    operation_time = Column(DateTime)
    user = relationship("User", back_populates="routes")
    estimations = relationship("Estimation", back_populates="route")
    coordinates = relationship("Coordinate", back_populates="routes")


class Coordinate(Base):
    """
    Модель координаты.

    Поля:
    cord_id (int): Уникальный идентификатор координаты.
    route_id (int): ID маршрута.
    user_id (int): ID пользователя, добавившего координату.
    latitude (float): Широта.
    longitude (float): Долгота.
    order (int): Порядок координаты в маршруте.
    locname (str): Название местоположения.
    operation_time (DateTime): Время добавления координаты.
    routes (relationship): Связь с маршрутом.
    """
    __tablename__ = 'coordinates'
    cord_id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    route_id = Column(Integer, ForeignKey('routes.route_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    locname = Column(String)
    routes = relationship("Route", back_populates="coordinates")


class Estimation(Base):
    """
    Модель оценки маршрута.

    Поля:
    estimation_id (int): Уникальный идентификатор оценки.
    route_id (int): ID маршрута.
    user_id (int): ID пользователя, создавшего маршрут.
    estimation_value (int): Значение оценки.
    estimator_id (int): ID пользователя, оценившего маршрут.
    datetime (DateTime): Время оценки.
    comment (str): Комментарий к оценке.
    route (relationship): Связь с маршрутом.
    """
    __tablename__ = 'estimations'
    estimation_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    route_id = Column(Integer, ForeignKey('routes.route_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    estimation_value = Column(Integer, nullable=False)
    estimator_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    datetime = Column(DateTime, nullable=False)
    comment = Column(String)
    route = relationship("Route", back_populates="estimations")
