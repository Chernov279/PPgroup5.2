from datetime import datetime, date, timezone
from typing import Optional

from sqlalchemy import Integer, String, DateTime, Float, ForeignKey, Date, Boolean, Text, CheckConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func

from .base_model import DeclarativeBaseModel, PrimaryId, TimeBaseModel


# TODO сделать отдельную модель для избранных роутов


class User(DeclarativeBaseModel, PrimaryId, TimeBaseModel):
    """
    Модель пользователя системы.

    Attributes:
        id (int): Уникальный идентификатор пользователя
        name (str): Имя пользователя (обязательно)
        email (str): Email (уникальный, обязательный)
        telephone_number (str): Номер телефона (уникальный, опционально)
        email_verified (bool): Подтвержден ли email
        surname (str): Фамилия (опционально)
        patronymic (str): Отчество (опционально)
        location (str): Город/страна (опционально)
        sex (str): Пол ('M'/'F' или NULL)
        birth (date): Дата рождения (с проверкой валидности)
        hashed_password (str): Хэшированный пароль
        last_active_time (datetime): Время последней активности
        status_id (int): Ссылка на статус пользователя
        created_at (datetime): Время создания
        updated_at (datetime): Время последнего обновления

        status_ref (UserStatus): Статус пользователя (joined загрузка)
        routes (list[Route]): Маршруты созданные пользователем
        ratings (list[Rating]): Оценки оставленные пользователем

    Properties:
        permissions (dict): Права пользователя из статуса
        can_edit_any_content (bool): Может редактировать любой контент
        full_name (str): Полное имя (фамилия + имя + отчество)
        age (int): Возраст пользователя

    Constraints:
        ck_valid_user_birth: Дата рождения между 1900-01-01 и текущей датой
        ck_valid_sex: Пол только 'M', 'F' или NULL
    """

    __tablename__ = 'users'

    # Основная информация
    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        comment="Имя пользователя"
    )

    # Контактные данные
    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
        index=True,
        comment="Уникальный email пользователя"
    )
    telephone_number: Mapped[Optional[str]] = mapped_column(
        String,
        unique=True,
        nullable=True,
        comment="Уникальный номер телефона в международном формате"
    )
    email_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="Подтвержден ли email пользователя"
    )

    # Дополнительная информация
    surname: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
        comment="Фамилия пользователя"
    )

    # Демографические данные
    location: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
        comment="Город или страна проживания"
    )
    sex: Mapped[Optional[str]] = mapped_column(
        String(1),
        nullable=True,
        comment="Пол: 'M' - мужской, 'F' - женский"
    )
    birth: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
        comment="Дата рождения пользователя"
    )

    # Безопасность
    hashed_password: Mapped[str] = mapped_column(
        String,
        nullable=False,
        comment="Хэшированный пароль (bcrypt/scrypt)"
    )

    # Активность
    last_active_time: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        nullable=True,
        index=True,
        comment="Время последней активности. Обновляется через Redis"
    )

    # Статус и права
    status_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('user_statuses.id', ondelete="RESTRICT"),
        nullable=False,
        default=1,
        comment="Ссылка на статус пользователя. По умолчанию: обычный пользователь"
    )

    # Relationships
    status_ref: Mapped["UserStatus"] = relationship(
        "UserStatus",
        lazy='joined',  # Всегда подгружаем статус JOIN'ом
        innerjoin=True,
        comment="Статус пользователя с правами доступа"
    )

    routes: Mapped[list["Route"]] = relationship(
        "Route",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="dynamic",
        comment="Маршруты созданные пользователем"
    )

    ratings: Mapped[list["Rating"]] = relationship(
        "Rating",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="dynamic",
        comment="Оценки оставленные пользователем"
    )

    @property
    def permissions(self) -> dict:
        """Права пользователя из связанного статуса"""
        return self.status_ref.permissions if self.status_ref else {}

    @property
    def can_edit_any_content(self) -> bool:
        """Может ли пользователь редактировать любой контент"""
        return self.permissions.get('can_edit_any_content', False)

    @property
    def full_name(self) -> str:
        """Полное имя пользователя (фамилия + имя + отчество)"""
        parts = []
        if self.surname:
            parts.append(self.surname)
        parts.append(self.name)
        return ' '.join(parts) if parts else self.name

    @property
    def age_in_years(self) -> Optional[int]:
        """Возраст пользователя в годах"""
        if not self.birth:
            return None

        today = date.today()
        age = today.year - self.birth.year

        # Проверяем, был ли уже день рождения в текущем году
        if (today.month, today.day) < (self.birth.month, self.birth.day):
            age -= 1

        return age

    __table_args__ = (
        # Проверка даты рождения
        CheckConstraint(
            "(birth IS NULL) OR (birth BETWEEN '1900-01-01' AND CURRENT_DATE)",
            name='ck_valid_user_birth',
            comment="Дата рождения должна быть между 1900-01-01 и текущей датой"
        ),
        # Проверка пола
        CheckConstraint(
            "(sex IS NULL) OR (sex IN ('F', 'M'))",
            name='ck_valid_sex',
            comment="Пол может быть только 'F' (женский), 'M' (мужской) или NULL"
        ),
        # Проверка email
        CheckConstraint(
            "email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'",
            name='ck_valid_email'
        ),
    )

class UserStatus(DeclarativeBaseModel, PrimaryId):
    """
    Модель статусов пользователей с правами доступа.

    Attributes:
        id (int): Уникальный идентификатор статуса
        code (str): Машинный код статуса (уникальный, индексируется)
        name (str): Человекочитаемое название статуса
        permissions (dict): Права доступа в формате JSON
        description (str): Описание статуса (опционально)
        is_default (bool): Является ли статусом по умолчанию
        priority (int): Приоритет для сортировки (чем выше, тем важнее)

        users (list[User]): Пользователи с этим статусом

    Examples:
        Статус 'user':
            code='user', name='Обычный пользователь',
            permissions={'can_edit_own_content': True, 'max_routes_per_day': 10}

        Статус 'admin':
            code='admin', name='Администратор',
            permissions={'can_edit_any_content': True, 'can_ban_users': True}
    """

    __tablename__ = 'user_statuses'

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
        comment="Уникальный машинный код статуса (например, 'user', 'admin')"
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Человекочитаемое название статуса"
    )

    permissions: Mapped[dict] = mapped_column(
        JSONB,
        default=lambda: {
            # Базовые права
            "can_edit_own_content": True,
            "can_delete_own_content": True,
            "can_create_content": True,

            # Модераторские права
            "can_edit_any_content": False,
            "can_delete_any_content": False,
            "can_ban_users": False,

            # Лимиты
            "max_routes_per_day": 10,
            "max_comments_per_day": 50,

            # Премиум возможности
            "can_use_premium_features": False,
            "can_export_data": False,

            # API ограничения
            "api_rate_limit": 100,  # запросов в минуту
            "api_burst_limit": 20,  # запросов в секунду

            # Дополнительные флаги
            "is_hidden": False,  # скрытый пользователь
            "can_see_hidden": False,  # видит скрытых
        },
        nullable=False,
        comment="Права доступа в формате JSONB. Меняется через админку без деплоя"
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Подробное описание статуса и его возможностей"
    )
    is_default: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        comment="Автоматически присваивается новым пользователям"
    )
    priority: Mapped[int] = mapped_column(
        Integer,
        default=0,
        comment="Приоритет для сортировки (0-100). Чем выше, тем больше прав"
    )

    # Relationships
    users: Mapped[list["User"]] = relationship(
        "User",
        back_populates="status_ref",
        cascade="all, delete-orphan",
        lazy="dynamic",
        comment="Все пользователи с этим статусом"
    )


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

    @property
    def is_active(self) -> bool:
        """
        Возвращает True, если refresh-токен:
        - не отозван
        - не истёк
        """
        now = datetime.now(timezone.utc)
        return self.revoked_at is None and self.expires_at > now