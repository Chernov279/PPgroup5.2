from datetime import datetime, date, timezone
from typing import Optional

from sqlalchemy import Integer, String, DateTime, Float, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func

from .base_model import DeclarativeBaseModel, PrimaryId, TimeBaseModel


# TODO сделать отдельную модель для избранных роутов

class User(DeclarativeBaseModel, PrimaryId, TimeBaseModel):
    """
    Модель пользователя.

    Атрибуты:
        name (str): Имя пользователя.
        email (str): Уникальный email пользователя.
        telephone_number (str | None): Номер телефона, необязателен.
        surname (str | None): Фамилия пользователя.
        patronymic (str | None): Отчество пользователя.
        location (str | None): Местоположение пользователя.
        sex (str | None): Пол пользователя.
        hashed_password (str): Хэшированный пароль пользователя.
        birth (str | None): Дата рождения пользователя.
        is_active (bool): Флаг активности пользователя.
        last_active_time (datetime): Время последней активности пользователя.
        status (str | None): Статус пользователя.
        created_at (datetime): Время создания.
        updated_at (datetime | None): Время последнего обновления записи.

        routes (list[Route]): Маршруты, созданные пользователем.
        ratings (list[Rating]): Оценки маршрутов, оставленные пользователем.
    """

    __tablename__ = 'users'

    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    telephone_number: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    surname: Mapped[str] = mapped_column(String, nullable=True)
    patronymic: Mapped[str] = mapped_column(String, nullable=True)
    location: Mapped[str] = mapped_column(String, nullable=True)
    sex: Mapped[str] = mapped_column(String, nullable=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    birth: Mapped[date] = mapped_column(Date, nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=True)
    last_active_time: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=True)

    routes: Mapped[list["Route"]] = relationship("Route", back_populates="user", cascade="all, delete-orphan")
    ratings: Mapped[list["Rating"]] = relationship("Rating", back_populates="user", cascade="all, delete-orphan")


class Route(DeclarativeBaseModel, TimeBaseModel, PrimaryId):
    """
    Модель маршрута.

    Атрибуты:
        user_id (int): ID пользователя, создавшего маршрут.
        distance (float | None): Расстояние маршрута.
        users_travel_time (int | None): Время, затраченное на маршрут.
        users_travel_speed (int | None): Скорость передвижения по маршруту.
        users_transport (str | None): Вид транспорта, использованный для маршрута.
        comment (str | None): Комментарий к маршруту.
        locname_start (str | None): Начальная точка маршрута.
        locname_finish (str | None): Конечная точка маршрута.
        created_at (datetime): Время создания.
        updated_at (datetime | None): Время последнего обновления записи.

        user (User): Пользователь, создавший маршрут.
        ratings (list[Rating]): Оценки маршрута.
        coordinates (list[Coordinate]): Координаты маршрута.
    """

    __tablename__ = "routes"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    distance: Mapped[float] = mapped_column(Float, nullable=True)
    users_travel_time: Mapped[int] = mapped_column(Integer, nullable=True)
    users_travel_speed: Mapped[int] = mapped_column(Integer, nullable=True)
    users_transport: Mapped[str] = mapped_column(String, nullable=True)
    comment: Mapped[str] = mapped_column(String, nullable=True)
    locname_start: Mapped[str] = mapped_column(String, nullable=True)
    locname_finish: Mapped[str] = mapped_column(String, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="routes")
    ratings: Mapped[list["Rating"]] = relationship("Rating", back_populates="route", cascade="all, delete-orphan")
    coordinates: Mapped[list["Coordinate"]] = relationship("Coordinate", back_populates="route", cascade="all, delete-orphan")


class Coordinate(DeclarativeBaseModel):
    """
    Модель координаты маршрута.

    Атрибуты:
        order (int): Порядковый номер координаты.
        route_id (int): ID маршрута.
        user_id (int): ID пользователя, добавившего координату.
        latitude (float): Широта координаты.
        longitude (float): Долгота координаты.
        location (str): Название места.

        route (Route): Связанный маршрут.
    """
    __tablename__ = 'coordinates'

    order: Mapped[int] = mapped_column(Integer, primary_key=True)

    route_id: Mapped[int] = mapped_column(ForeignKey("routes.id", ondelete="CASCADE"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)

    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    location: Mapped[str] = mapped_column(String, nullable=True)

    route: Mapped["Route"] = relationship("Route", back_populates="coordinates")


class Rating(DeclarativeBaseModel, TimeBaseModel):
    """
    Модель оценки маршрута.

    Атрибуты:
        route_id (int): ID маршрута.
        user_id (int): ID пользователя, оставившего оценку.
        value (int): Оценка маршрута.
        comment (str | None): Комментарий к оценке.
        created_at (datetime): Время создания.
        updated_at (datetime | None): Время последнего обновления записи.

        route (Route): Связанный маршрут.
        user (User): Пользователь, оставивший оценку.
    """

    __tablename__ = 'ratings'

    route_id: Mapped[int] = mapped_column(ForeignKey("routes.id", ondelete="CASCADE"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)

    value: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[str] = mapped_column(String, nullable=True)

    route: Mapped["Route"] = relationship("Route", back_populates="ratings")
    user: Mapped["User"] = relationship("User", back_populates="ratings")


class RefreshToken(DeclarativeBaseModel, TimeBaseModel):
    """
    Модель refresh-токена (серверное состояние сессии).

    Один refresh-токен = одна строка в таблице.
    Используется для:
    - обновления access-токена,
    - logout с одного устройства,
    - logout со всех устройств пользователя.

    Атрибуты:
        id (int): Surrogate PK. Используется только БД, не участвует в бизнес-логике.
        user_id (int): ID пользователя.
        token_hash (str): SHA-256 хэш refresh-токена. Уникален.
        device_fingerprint (str | None): Опциональная информация об устройстве.
        expires_at (datetime): Время истечения refresh-токена.
        revoked_at (datetime | None): Время отзыва токена. NULL = токен активен.
        created_at (datetime): Время создания токена.
        updated_at (datetime | None): Время последнего обновления записи.

        user (User): Пользователь, которому принадлежит токен.
    """

    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    token_hash: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        unique=True,
    )

    device_fingerprint: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    # -------- Lifecycle --------
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    revoked_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="refresh_tokens",
    )

    @property
    def is_active(self) -> bool:
        """
        Возвращает True, если refresh-токен:
        - не отозван
        - не истёк
        """
        now = datetime.now(timezone.utc)
        return self.revoked_at is None and self.expires_at > now