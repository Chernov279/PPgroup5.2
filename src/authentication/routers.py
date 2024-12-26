from fastapi import Depends, APIRouter

from src.authentication.auth_dependecies import get_user_auth_service
from src.authentication.auth_service import UserAuthService
from src.authentication.schemas import UserAuthIn
from src.user.schemas import UserOut

auth = APIRouter(prefix="/auth", tags=["auth"])


@auth.post("/register", response_model=UserOut, summary="Register a new user")
def register_user_route(
    user_auth: UserAuthIn,
    user_auth_service: UserAuthService = Depends(get_user_auth_service),
):
    """
    Регистрация нового пользователя.
    """
    return user_auth_service.register_user(user_auth.name, user_auth.email, user_auth.password)


# @auth.post("/login")
# def login(login_user: UserLogin, session: Session = Depends(get_db)):
#     """
#     Авторизует пользователя в системе.
#
#     Args:
#         login_user (UserLogin): Данные для авторизации.
#         session (Session, optional): Сессия базы данных. Defaults to Depends(get_db).
#
#     Raises:
#         HTTPException: В случае неверного логина или пароля.
#
#     Returns:
#         dict: Словарь с результатом операции.
#     """
#     telephone_number, email, user = is_login(login_user.login, nothing, nothing, error_login_udentified)
#     if user:
#         if authenticated_user(login_user.password, user.hashed_password, user.salt_hashed_password):
#             return {"status": "success",
#                     "data": {
#                         "user": MyUserOut(
#                             id=user.id,
#                             name=user.name,
#                             email=user.email,
#                             telephone_number=user.telephone_number,
#                             surname=user.surname,
#                             patronymic=user.patronymic,
#                             location=user.location,
#                             sex=user.sex,
#                             token_mobile=user.token_mobile,
#                             favorite_routes=user.favorite_routes,
#                             birth=user.birth,
#                             authorized_time=str(user.authorized_time)
#                         )
#                     },
#                     "details": None
#                     }
#
#     raise HTTPException(status_code=404, detail={
#         "status": "error",
#         "data": None,
#         "details": "Incorrect login or password"
#     })
