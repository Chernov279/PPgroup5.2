from typing import List, Annotated

from fastapi import Depends, APIRouter

from .user_service import UserService
from .user_schemas import UserDetailOut, UserShortOut, UserUpdateIn, UserPrimaryKey
from ..config.token_config import oauth2_scheme
from ..schemas.database_params_schemas import MultiGetParams
from ..token_app.token_dependencies import get_optional_token

user = APIRouter(prefix="/users", tags=["User"])


@user.get("/", response_model=List[UserShortOut])
async def get_all_users_route(
    token: Annotated[str, Depends(get_optional_token)],
    multi_get_params: MultiGetParams = Depends(),
    user_service: UserService = Depends()
):
    return await user_service.get_all_users(token, multi_get_params)


@user.get("/me", response_model=UserDetailOut)
async def get_user_me_route(
        token: Annotated[str, Depends(oauth2_scheme)],
        user_service: UserService = Depends()
):
    return await user_service.get_user_me(token)


@user.get("/{user_id}", response_model=UserDetailOut)
async def get_user_route(
        token: Annotated[str, Depends(get_optional_token)],
        userPK: UserPrimaryKey = Depends(),
        user_service: UserService = Depends()
):
    return await user_service.get_user_by_id(token, userPK)


@user.put("/", response_model=UserDetailOut)
async def update_user_route(
        user_in: UserUpdateIn,
        token: Annotated[str, Depends(oauth2_scheme)],
        user_service: UserService = Depends(),
):
    return await user_service.update_user(user_in, token)


@user.delete("/")
async def delete_user_route(
        token: Annotated[str, Depends(oauth2_scheme)],
        user_service: UserService = Depends()
):
    return user_service.delete_user(token)
