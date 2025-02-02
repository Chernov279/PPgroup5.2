# from fastapi import Depends, APIRouter
#
# from .auth_dependecies import get_user_auth_service, get_user_auth_service_db
# from .auth_service import UserAuthService
# from .auth_schemas import UserAuthIn, UserLoginIn, AccessTokenOut
#
# auth = APIRouter(prefix="/auth", tags=["auth"])
#TODO роутер на сгенерирование пароля с заданными данными
#
# @auth.post("/register", response_model=AccessTokenOut, summary="Register a new user")
# def register_user_route(
#     user_auth: UserAuthIn,
#     user_auth_service: UserAuthService = Depends(get_user_auth_service_db),
# ):
#     """
#     Регистрация нового пользователя.
#
#     ### Входные данные:
#     - `user_auth` (UserAuthIn): Объект с информацией для регистрации пользователя.
#       - Поля:
#         - `email` (str): Email пользователя.
#         - `password` (str): Пароль пользователя.
#         - `name` (str): Никнейм пользователя.
#
#     ### Логика:
#     Проверяет, является ли email уникальным.
#     Сохраняет пользователя в базе данных, если данные успешно прошли валидацию.
#     Генерирует refresh_token и сохраняет его в куках на стороне клиента.
#     Генерирует токен доступа - access_token.
#     Возвращает токен в теле ответа случае успешной регистрации.
#
#     ### Возвращаемые данные:
#     - `AccessTokenOut`:
#       - Поля:
#         - `access_token` (str): Токен доступа.
#         - `token_type` (str): Тип токена (default="Bearer").
#     """
#     return user_auth_service.register_user(user_auth)
#
#
# @auth.post("/login", response_model=AccessTokenOut, summary="Authentication user")
# def login_user_route(
#     user_login: UserLoginIn,
#     user_auth_service: UserAuthService = Depends(get_user_auth_service_db),
# ):
#     """
#     Авторизация пользователя.
#
#     ### Входные данные:
#     - `user_login` (UserLoginIn): Объект с учетными данными пользователя.
#       - Поля:
#         - `email` (str): Email пользователя.
#         - `password` (str): Пароль пользователя.
#
#     ### Логика:
#     Проверяет, существует ли пользователь с указанным email.
#     Проверяет, что введённый пароль соответствует сохранённому (хэшированному).
#     Генерирует refresh_token и сохраняет его в куках на стороне клиента.
#     Генерирует токен доступа - access_token.
#     Возвращает токен в случае успешной авторизации.
#
#     ### Возвращаемые данные:
#     - `AccessTokenOut`:
#       - Поля:
#         - `access_token` (str): Токен доступа.
#         - `token_type` (str): Тип токена (default="Bearer").
#     """
#     return user_auth_service.login_user(user_login)
#
#
# @auth.post("/logout", summary="logout user")
# def login_user_route(
#     user_auth_service: UserAuthService = Depends(get_user_auth_service),
# ):
#     """
#     Выход пользователя из системы.
#
#     ### Входные данные:
#     - Нет явных входных данных. Для выполнения используется cookie `refresh_token`.
#
#     ### Логика:
#     Удаляет `refresh_token` из cookies, отправив пустой токен либо токен с истёкшим сроком действия.
#     PS: Старый токен не перестает быть валидным и все еще может использоваться.
#
#     ### Возвращаемые данные:
#     - Нет возвращаемых данных. В ответе будет HTTP-статус 200 (OK), если операция успешна.
#     """
#     return user_auth_service.logout_user()
