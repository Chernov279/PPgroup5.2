from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.responses import JSONResponse

from .dependencies import get_auth_service, get_refresh_token
from .schemas import AccessTokenOut, AuthRegisterIn, TokensOut, AuthLoginIn, LogoutAllOut, LogoutOut
from .service import AuthService


auth = APIRouter(prefix="/auth", tags=["Authentication"])


@auth.post(
    "/register",
    response_model=TokensOut,
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация нового пользователя",
    response_description="Пользователь успешно зарегистрирован, возвращены токены",
    responses={
        201: {"description": "Пользователь успешно создан"},
        400: {"description": "Неверные входные данные"},
        409: {"description": "Пользователь уже существует"},
        422: {"description": "Ошибка валидации"},
    }
)
async def register_user(
        user_data: AuthRegisterIn,
        auth_service: AuthService = Depends(get_auth_service),
) -> TokensOut:
    """
    Регистрация нового пользователя.

    Этот эндпоинт создает нового пользователя с предоставленной информацией.
    При успешной регистрации возвращаются access и refresh токены.

    **Тело запроса (обязательные поля):**
    - `name` (str): Имя пользователя
    - `email` (str): Email пользователя (должен быть уникальным)
    - `password` (str): Пароль пользователя (будет захэширован)

    **Тело запроса (опциональные поля):**
    - `surname` (str): Фамилия пользователя
    - `patronymic` (str): Отчество пользователя

    **Ответ:**
    - `access_token` (str): JWT access токен для авторизации в API
    - `refresh_token` (str): Refresh токен для получения новых access токенов
    - `token_type` (str): Всегда "bearer"

    **Примечание:** Refresh токен также устанавливается в HTTP-only cookie.
    """
    return await auth_service.register_user(user_data)


@auth.post(
    "/login",
    response_model=TokensOut,
    summary="Аутентификация пользователя по email и паролю",
    response_description="Аутентификация успешна, возвращены токены",
    responses={
        200: {"description": "Аутентификация успешна"},
        401: {"description": "Неверные учетные данные"},
        403: {"description": "Аккаунт не активен"},
        404: {"description": "Пользователь не найден"},
    }
)
async def login_user(
        login_data: AuthLoginIn,
        auth_service: AuthService = Depends(get_auth_service),
) -> TokensOut:
    """
    Аутентификация пользователя по email и паролю.

    Этот эндпоинт проверяет учетные данные пользователя и возвращает
    access и refresh токены при успешной аутентификации.

    **Тело запроса:**
    - `email` (str): Email пользователя
    - `password` (str): Пароль пользователя

    **Ответ:**
    - `access_token` (str): JWT access токен для авторизации в API
    - `refresh_token` (str): Refresh токен для получения новых access токенов
    - `token_type` (str): Всегда "bearer"

    **Примечание:** Refresh токен также устанавливается в HTTP-only cookie.
    """
    # Вызываем метод сервиса, передавая данные для входа
    return await auth_service.login_user(login_data)


@auth.post(
    "/oauth2",
    response_model=TokensOut,
    summary="OAuth2-совместимый эндпоинт для получения токенов",
    response_description="Токены сгенерированы для совместимости с OAuth2",
    responses={
        200: {"description": "Токены успешно сгенерированы"},
        401: {"description": "Неверные учетные данные"},
    }
)
async def login_oauth2(
        form_data: OAuth2PasswordRequestForm = Depends(),
        auth_service: AuthService = Depends(get_auth_service),
) -> TokensOut:
    """
    OAuth2-совместимый эндпоинт для аутентификации.

    Этот эндпоинт обеспечивает совместимость с OAuth2 для сторонних клиентов.
    Использует данные формы вместо JSON для аутентификации.

    **Данные формы:**
    - `username` (str): Email пользователя (в OAuth2 используется поле username для email)
    - `password` (str): Пароль пользователя

    **Ответ:**
    - `access_token` (str): JWT access токен для авторизации в API
    - `refresh_token` (str): Refresh токен для получения новых access токенов
    - `token_type` (str): Всегда "bearer"

    **Примечание:** Этот эндпоинт в основном для интеграции с Swagger UI и OAuth2 клиентами.
    """
    return await auth_service.login_oauth2(
        username=form_data.username,
        password=form_data.password
    )


@auth.post(
    "/refresh",
    response_model=TokensOut,
    summary="Обновление access токена",
    response_description="Новый access токен сгенерирован",
    responses={
        200: {"description": "Токен успешно обновлен"},
        401: {"description": "Неверный или истекший refresh токен"},
        403: {"description": "Refresh токен отозван"},
    }
)
async def refresh_access_token(
        refresh_token: str = Depends(get_refresh_token),
        auth_service: AuthService = Depends(get_auth_service),
) -> TokensOut:
    """
    Получение нового access токена с помощью refresh токена.

    Этот эндпоинт позволяет получить новый access токен, когда текущий истекает.
    Refresh токен может быть предоставлен либо в теле запроса, либо в HTTP-only cookie.

    **Тело запроса (опционально, если токен в cookie):**
    - `refresh_token` (str): Валидный refresh токен

    **Cookie (опционально, если токен в теле запроса):**
    - `refresh_token`: HTTP-only cookie, содержащая refresh токен

    **Ответ:**
    - `access_token` (str): Новый JWT access токен
    - `refresh_token` (str): Новый refresh токен (ротация токенов)
    - `token_type` (str): Всегда "bearer"

    **Примечание:** При использовании ротации refresh токенов старый токен становится невалидным.
    """

    return await auth_service.refresh_tokens(refresh_token)


@auth.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    summary="Выход из текущей сессии",
    response_description="Пользователь вышел из текущего устройства",
    responses={
        200: {"description": "Успешно вышел из системы"},
        400: {"description": "Refresh токен не предоставлен"},
        401: {"description": "Неверный refresh токен"},
    }
)
async def logout_user(
        refresh_token: str = Depends(get_refresh_token),
        auth_service: AuthService = Depends(get_auth_service),
) -> LogoutOut:
    """
    Выход пользователя из текущего устройства.

    Этот эндпоинт делает невалидным текущий refresh токен,
    выполняя выход пользователя из текущего устройства/сессии.

    **Тело запроса (опционально, если токен в cookie):**
    - `refresh_token` (str): Refresh токен для отзыва

    **Cookie (опционально, если токен в теле запроса):**
    - `refresh_token`: HTTP-only cookie, содержащая refresh токен

    **Ответ:**
    - `message` (str): "Успешно вышел из системы"
    - `details` (str): Дополнительная информация
    """

    return await auth_service.logout_user(refresh_token)


@auth.post(
    "/logout-all",
    status_code=status.HTTP_200_OK,
    summary="Выход со всех устройств",
    response_description="Пользователь вышел со всех устройств",
    responses={
        200: {"description": "Успешно вышел со всех устройств"},
        400: {"description": "Refresh токен не предоставлен"},
        401: {"description": "Неверный refresh токен"},
    }
)
async def logout_all_devices(
        refresh_token: str = Depends(get_refresh_token),
        auth_service: AuthService = Depends(get_auth_service),
) -> LogoutAllOut:
    """
    Выход пользователя со всех устройств.

    Этот эндпоинт делает невалидными ВСЕ refresh токены пользователя,
    выполняя выход со всех устройств и сессий.

    **Тело запроса (опционально, если токен в cookie):**
    - `refresh_token` (str): Любой валидный refresh токен пользователя

    **Cookie (опционально, если токен в теле запроса):**
    - `refresh_token`: HTTP-only cookie, содержащая refresh токен

    **Ответ:**
    - `message` (str): "Успешно вышел со всех устройств"
    - `devices_logged_out` (int): Количество завершенных сессий
    - `timestamp` (str): Время выполнения операции
    """

    return await auth_service.logout_all_devices(refresh_token)
