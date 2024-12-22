"""
Этот файл генерирует тестовые данные для базы данных.

Использует модуль Faker для создания фальшивых данных пользователей,
маршрутов, оценок и координат.

"""
from faker import Faker
from sqlalchemy import func

from PPgroup5.pythonBackEnd.database.database import User, Route, Coordinate, Estimation, session
import random

fake = Faker()

# id Для удаленных пользователей, чтобы маршруты не терялись при удалении пользователем профиля.
if not session.query(User).filter(User.id == 0).first():
    session.add(User(
        id=0,
        name="Deleted users",
        email="0",
        telephone_number="0",
        hashed_password="0",
        salt_hashed_password="0",
        token_mobile="0"
    ))

# Добавление случайного пользователя для корректного нахождения последнего id
# последнего зарегистрированного пользователя
session.add(User(
    name=fake.name(),
    hashed_password=fake.password(),
    telephone_number=str(random.randint(10 ** 10, 10 ** 11 - 1)),
    salt_hashed_password=fake.password(),
    token_mobile=random.randint(10000, 100000)
))
session.commit()

# Получение максимального ID пользователя
max_user_id = session.query(func.max(User.id)).scalar()

# Добавление случайного маршрута для пользователя для корректного нахождения последнего id
# последнего зарегистрированного роута
session.add(Route(
    user_id=max_user_id,
    distance=random.uniform(1, 100)
))
session.commit()

# Получение максимального ID маршрута
max_route_id = session.query(func.max(Route.route_id)).scalar()

# Генерация тестовых данных для пользователей, маршрутов, оценок и координат
for i in range(1, 50):
    # Генерация случайных данных для пользователя
    user = User(
        name=fake.name(),
        hashed_password=fake.password(),
        telephone_number=str(random.randint(10**10, 10**11 - 1)),
        salt_hashed_password=fake.password(),
        token_mobile=random.randint(10000, 100000)
    )
    session.add(user)

    # Генерация случайных данных для маршрута
    route = Route(
        user_id=random.randint(max_user_id, max_user_id + i),
        distance=random.uniform(1, 100),
        users_travel_time=random.uniform(1, 10000)
    )
    session.add(route)

    # Генерация случайных данных для оценки маршрута
    estimation = Estimation(
        route_id=random.randint(max_route_id, max_route_id + i),
        estimation_value=random.randint(0, 5),
        estimator_id=random.randint(max_user_id, max_user_id + i),
        datetime=fake.date_time(),
        user_id=random.randint(max_user_id, max_user_id + i)
    )
    session.add(estimation)

# Добавление случайных координат для маршрутов
for u in range(1, 50):
    route_id = random.randint(max_route_id, max_route_id + 49)  # Генерация случайного существующего route_id
    user_id = random.randint(max_user_id, max_user_id + 49)  # Генерация случайного user_id
    for y in range(5):
        coordinate = Coordinate(
            latitude=random.uniform(-90, 90),
            longitude=random.uniform(-180, 180),
            operation_time=fake.date_time(),
            route_id=route_id,
            user_id=user_id,
            order=y + 1
        )
        session.add(coordinate)

session.commit()
