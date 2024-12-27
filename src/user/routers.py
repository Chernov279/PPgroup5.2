from typing import List

from fastapi import Depends, APIRouter

from src.dependencies.user_dependencies import get_user_service
from src.services.user_service import UserService
from src.user.schemas import UserOut, UserCreateIn, UserUpdateIn

user = APIRouter(prefix="/users", tags=["/users"])


@user.get("/", response_model=List[UserOut])
def get_all_users_route(user_service: UserService = Depends(get_user_service)):
    return user_service.get_users_service()


@user.get("/{user_id}", response_model=UserOut)
def get_user_route(user_id: int, user_service: UserService = Depends(get_user_service)):
    return user_service.get_user_or_404_service(user_id)


@user.post("/create", response_model=UserOut)
def create_user_route(user_data: UserCreateIn, user_service: UserService = Depends(get_user_service)):
    return user_service.create_user_service(user_data.name, user_data.email, user_data.hashed_password)


@user.put("/{user_id}", response_model=UserOut)
def update_user_route(user_data: UserUpdateIn, user_service: UserService = Depends(get_user_service)):
    return user_service.update_user_service(user_data.user_id, user_data.name)


@user.delete("/{user_id}", response_model=bool)
def delete_user_route(user_id: int, user_service: UserService = Depends(get_user_service)):
    return user_service.delete_user_service(user_id)
