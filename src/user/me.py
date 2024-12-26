from fastapi import APIRouter, Depends, HTTPException

from src.authentication.utils import is_telephone_number, is_valid_email
from src.database.database import Session, get_db, Route, Estimation, User
from src.schemas.schemas import user_search, time_redakt, avg_estimation

profile = APIRouter(
    prefix="/me",
    tags=["current_user_profile"]
)


@profile.get("/profile")
def get_current_user(user_id: int, session: Session = Depends(get_db)):
    """
    Получение текущего профиля пользователя.

    Аргументы:
    - user_id: ID пользователя.
    - session: Сессия базы данных.

    Возвращает:
    - Данные профиля пользователя, включая его любимые маршруты и созданные им оценки и маршруты.
    """
    user = user_search(user_id, session)
    routes = session.query(Route).filter(Route.user_id == user_id).all()
    routes_out = []
    id = 1
    for route in routes[::-1]:
        user_name = user.name
        if user.surname:
            user_name = f"{user.name} {user.surname}"
        routes_out.append(
                Route(
                    id=id,
                    users_travel_time=time_redakt(route.users_travel_time),
                    comment=route.comment,
                    route_id=route.route_id,
                    user_id=route.user_id,
                    distance=round(route.user_id, 2),
                    avg_travel_time_on_foot=route.avg_travel_time_on_foot,
                    avg_travel_velo_time=route.avg_travel_velo_time,
                    avg_estimation=avg_estimation(route.route_id, session),
                    user_name=user_name,
                    created_time=str(route.operation_time)
                        )
                    )
        id += 1

    estimations = session.query(Estimation).filter(Estimation.estimator_id == user_id).all()
    if user.favorite_routes:
        favorite_routes = session.query(Route).filter(Route.route_id.in_(user.favorite_routes)).all()
    else:
        favorite_routes = []
    return {"status": "success",
            "data": {
                "user": User(
                    id=user_id,
                    name=user.name,
                    email=user.email,
                    telephone_number=user.telephone_number,
                    surname=user.surname,
                    patronymic=user.patronymic,
                    location=user.location,
                    sex=user.sex,
                    token_mobile=user.token_mobile,
                    birth=user.birth,
                    authorized_time=str(user.authorized_time)
                ),
                "favorite_routes": favorite_routes,
                "routes": routes_out,
                "estimations": estimations
            },
            "details": None
            }


# @profile.put("/profile")
# def update_user(user_data: User, session: Session = Depends(get_db)):
#     """
#     Обновление профиля пользователя.
#
#     Аргументы:
#     - user_data: Данные пользователя для обновления.
#     - session: Сессия базы данных.
#
#     Возвращает:
#     - Обновленные данные профиля пользователя.
#
#     Если приходит пустое значение, то данные сохраняются такими, какими были в базе данных.
#     """
#     user = session.query(User).filter(User.id == user_data.id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#
#     if user_data.telephone_number:
#         if not is_telephone_number(user_data.telephone_number):
#             raise HTTPException(status_code=400, detail={
#                 "status": "error",
#                 "data": None,
#                 "details": "Bad telephone_number"
#             })
#         if session.query(User).filter(
#             User.telephone_number == user_data.telephone_number,
#             User.id != user_data.id
#         ).first():
#             raise HTTPException(status_code=400, detail="Telephone number already exists")
#
#     if user_data.email:
#         if not is_valid_email(user_data.email):
#             print(user_data.email)
#             raise HTTPException(status_code=400, detail={
#                 "status": "error",
#                 "data": None,
#                 "details": "Bad email"
#             })
#         if session.query(User).filter(
#             User.email == user_data.email,
#             User.id != user_data.id
#         ).first():
#             raise HTTPException(status_code=400, detail="Email already exists")
#
#     user_data_dict = user_data.dict(exclude_unset=True)
#
#     for attr, value in user_data_dict.items():
#         if value is not None:
#             setattr(user, attr, value)
#     session.commit()
#     session.refresh(user)
#
#     return {"status": "success",
#             "data": User(
#                 id=user.id,
#                 name=user.name,
#                 email=user.email,
#                 telephone_number=user.telephone_number,
#                 surname=user.surname,
#                 patronymic=user.patronymic,
#                 location=user.location,
#                 sex=user.sex,
#                 token_mobile=user.token_mobile,
#                 birth=user.birth,
#                 authorized_time=str(user.authorized_time)
#             ),
#             "details": None
#             }

    # # if "password" in user_data_dict:
    # #     password = user_data_dict.pop("password")
    # #     generated_salt, hashed_password = creating_hash_salt(password)
    # #     user_data_dict["hashed_password"] = hashed_password
    # #     user_data_dict["salt_hashed_password"] = generated_salt

#
# @profile.delete("/profile")
# def delete_user(user_id: int, session: Session = Depends(get_db)):
#     """
#     Удаление профиля пользователя.
#
#     Аргументы:
#     - user_id: ID пользователя.
#     - session: Сессия базы данных.
#
#     Возвращает:
#     - Статус успеха после удаления пользователя и связанных данных.
#     """
#     user = user_search(user_id, session)
#
#     session.query(Estimation).filter(Estimation.estimator_id == user_id).update({'estimator_id': 0})
#     session.query(Estimation).filter(Estimation.user_id == user_id).update({'user_id': 0})
#     session.query(Coordinate).filter(Coordinate.user_id == user_id).update({'user_id': 0})
#     session.query(Route).filter(Route.user_id == user_id).update({'user_id': 0})
#     session.delete(user)
#     session.commit()
#     return {
#         "status": "success",
#         "data": None,
#         "details": None
#     }
