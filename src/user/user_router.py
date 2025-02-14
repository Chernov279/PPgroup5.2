from typing import List, Annotated

from fastapi import Depends, APIRouter

from .user_service import UserService
from .user_schemas import UserDetailOut, UserShortOut

user = APIRouter(prefix="/users", tags=["User"])


@user.get("/", response_model=List[UserShortOut])
async def get_all_users_route(
        users: Annotated[List[UserShortOut], Depends(UserService.get_all_users_service)]
):
    return users


@user.get("/me", response_model=UserDetailOut)
async def get_user_me_route(
        user_out: Annotated[UserDetailOut, Depends(UserService.get_user_me_service)]
):
    return user_out


@user.get("/{user_id}", response_model=UserDetailOut)
async def get_user_route(
        user_out: Annotated[UserDetailOut, Depends(UserService.get_user_by_id_service)]
):
    return user_out


# @user.post("/", response_model=UserDetailOut)
# async def create_user_route(
#         user_out: Annotated[UserDetailOut, Depends(UserService.create_user_service)]
# ):
#     return user_out


@user.put("/", response_model=UserDetailOut)
async def update_user_route(
        user_out: Annotated[UserDetailOut, Depends(UserService.update_user_service)]
):
    return user_out


@user.delete("/")
async def delete_user_route(
        user_out: Annotated[UserDetailOut, Depends(UserService.delete_user_service)]
):
    return user_out
