from typing import List, Annotated

from fastapi import Depends, APIRouter

from ..config.token_config import oauth2_scheme
from .user_dependencies import get_user_service_db
from .user_service import UserService
from .user_schemas import UserOut, UserCreateIn, UserUpdateIn

user = APIRouter(prefix="/users", tags=["/users"])


@user.get("/", response_model=List[UserOut])
def get_all_users_route(
        user_service: UserService = Depends(get_user_service_db)
):
    return user_service.get_users_service()


@user.get("/me", response_model=UserOut)
def get_user_me_route(
        token: Annotated[str, Depends(oauth2_scheme)],
        user_service: UserService = Depends(get_user_service_db)
):
    return user_service.get_user_me_service(token)


@user.post("/create", response_model=UserOut)
def create_user_route(
        user_data: UserCreateIn,
        user_service: UserService = Depends(get_user_service_db)
):
    return user_service.create_user_service(user_data)


@user.get("/{user_id}", response_model=UserOut)
def get_user_route(
        user_id: int,
        user_service: UserService = Depends(get_user_service_db)
):
    return user_service.get_user_or_404_service(user_id)


@user.put("/{user_id}", response_model=UserOut)
def update_user_route(
        user_data: UserUpdateIn,
        token: Annotated[str, Depends(oauth2_scheme)],
        user_service: UserService = Depends(get_user_service_db),
):
    return user_service.update_user_service(user_data, token)


@user.delete("/{user_id}")
def delete_user_route(
        token: Annotated[str, Depends(oauth2_scheme)],
        user_service: UserService = Depends(get_user_service_db)):
    return user_service.delete_user_service(token)

