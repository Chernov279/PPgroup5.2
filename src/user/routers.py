from fastapi import Depends, APIRouter

from src.models.models import User
from src.repositories.user_repositories import UserRepository
from src.services.user_service import get_user_service
from src.user.schemas import UserOut

user = APIRouter(prefix="/user", tags=["/user"])

@user.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, user: UserRepository = Depends(get_user_service)):
    return user.get_user_or_404(user_id)
