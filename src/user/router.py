from typing import List, Annotated

from fastapi import Depends, APIRouter, Path, Query
from starlette import status
from starlette.responses import Response

from .dependencies import get_user_service
from .service import UserService
from .schemas import UserDetailOut, UserShortOut, UserUpdateIn, UserActivityOut, UserUpdateActivityOut
from ..authentication.dependencies import get_token_sub_optional, get_token_sub_required
from ..schemas.database_params_schemas import MultiGetParams

user = APIRouter(prefix="/users", tags=["User"])


@user.get(
    "/",
    response_model=List[UserShortOut],
    summary="Получение списка пользователей",
    response_description="Список пользователей",
    responses={
        200: {"description": "Пользователи успешно получены"},
        422: {"description": "Ошибка валидации"},
    },
)
async def get_all_users(
    token_sub: Annotated[int | None, Depends(get_token_sub_optional)],
    params: MultiGetParams = Depends(),
    user_service: UserService = Depends(get_user_service),
) -> List[UserShortOut]:
    """
    Получение списка пользователей с поддержкой пагинации и фильтрации.

    Требуется аутентификация.
    """
    return await user_service.get_all_users(token_sub, params)


@user.get(
    "/me",
    response_model=UserDetailOut,
    summary="Получение текущего пользователя",
    response_description="Данные текущего пользователя",
    responses={
        200: {"description": "Данные пользователя получены"},
        401: {"description": "Неавторизован"},
    },
)
async def get_me(
    token_sub: Annotated[int, Depends(get_token_sub_required)],
    user_service: UserService = Depends(get_user_service),
) -> UserDetailOut:
    """
    Возвращает данные текущего аутентифицированного пользователя.
    """
    return await user_service.get_user_me(token_sub)


@user.get(
    "/activity/{user_id}",
    response_model=UserActivityOut,
    summary="Получение активности пользователя",
    response_description="Статус активности пользователя",
)
async def get_user_activity(
    token_sub: Annotated[int | None, Depends(get_token_sub_optional)],
    user_service: UserService = Depends(get_user_service),
    user_id: int = Path(..., description="ID пользователя", gt=0),
) -> UserActivityOut:
    """
    Получение информации о последней активности пользователя.
    """
    return await user_service.get_user_activity(token_sub, user_id)


@user.get(
    "/{user_id}",
    response_model=UserDetailOut,
    summary="Получение пользователя по ID",
    response_description="Данные пользователя",
    responses={
        200: {"description": "Пользователь найден"},
        401: {"description": "Не авторизован"},
        404: {"description": "Пользователь не найден"},
    },
)
async def get_user_by_id(
    token_sub: Annotated[int | None, Depends(get_token_sub_optional)],
    user_id: int = Path(..., description="ID пользователя", gt=0),
    user_service: UserService = Depends(get_user_service),
) -> UserDetailOut:
    """
    Получение пользователя по его идентификатору.
    """
    return await user_service.get_user_by_id(token_sub, user_id)


@user.put(
    "/me",
    response_model=UserDetailOut,
    summary="Обновление данных пользователя",
    response_description="Данные пользователя обновлены",
    responses={
        200: {"description": "Данные обновлены"},
        400: {"description": "Неверные данные"},
        401: {"description": "Неавторизован"},
    },
)
async def update_me(
    user_in: UserUpdateIn,
    token_sub: Annotated[int, Depends(get_token_sub_required)],
    user_service: UserService = Depends(get_user_service),
) -> UserDetailOut:
    """
    Обновление данных текущего пользователя.
    """
    return await user_service.update_user(user_in, token_sub)


@user.patch(
    "/activity",
    response_model=UserUpdateActivityOut,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Обновление активности пользователя",
    response_description="Активность обновлена",
)
async def update_user_activity(
    token_sub: Annotated[int, Depends(get_token_sub_optional)],
    hard: bool = Query(
        default=False,
        description="Форс-обновление активности без учета порогов",
    ),
    user_id: int = Path(..., description="ID пользователя", gt=0),
    user_service: UserService = Depends(get_user_service),
) -> Response:
    """
    Обновление активности пользователя.

    - `hard=false` — обновление с учетом порога неактивности
    - `hard=true` — принудительное обновление
    """
    await user_service.update_user_time_activity(token_sub, user_id, hard)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@user.delete(
    "/me",
    status_code=status.HTTP_204_NO_CONTENT,  # 204 для удаления
    summary="Удаление пользователя",
    responses={
        204: {"description": "Пользователь удалён"},
        401: {"description": "Неавторизован"},
        404: {"description": "Пользователь не найден"},
    },
)
async def delete_me(
    token_sub: Annotated[int, Depends(get_token_sub_required)],
    user_service: UserService = Depends(get_user_service),
) -> Response:
    """
    Удаление текущего пользователя.
    """
    await user_service.delete_user(token_sub)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
