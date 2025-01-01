from typing import List

from fastapi import HTTPException

from ..config.database.db_helper import Session
from ..models.models import User
from ..repositories.uow.user_token import UserTokenUOW
from .user_schemas import UserCreateIn, UserUpdateIn
from .user_repositories import UserRepository


class UserService:
    def __init__(self, db: Session = None):
        if db:
            self.user_repo = UserRepository(db)
            self.user_token_uwo = UserTokenUOW(db)
        else:
            self.user_repo = UserRepository()
            self.user_token_uwo = UserTokenUOW()

    def get_user_or_404_service(self, user_id: int) -> User:
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def get_users_service(self) -> List[User]:
        user = self.user_repo.get_users()
        return user

    def create_user_service(self, user_data: UserCreateIn) -> User | None:
        """
        Создать нового пользователя.
        """
        try:
            return self.user_repo.create_user(user_data.name, user_data.email, user_data.hashed_password)
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail="User not created")

    def get_user_me_service(self, token: str):
        user = self.user_token_uwo.get_user_by_token_uow(token)
        if user:
            return user
        return HTTPException(status_code=404, detail="User not found")

    def update_user_service(
            self,
            user_data: UserUpdateIn,
            token: str
    ) -> User | None:
        """
        Обновить данные пользователя.
        """
        try:
            user = self.user_token_uwo.get_user_by_token_uow(token)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            updated_user = self.user_repo.update_user(user, user_data)
            if updated_user:
                return updated_user
            raise HTTPException(status_code=500, detail="User not updated")
        except HTTPException as e:
            raise e
        except Exception:
            raise HTTPException(status_code=500, detail="User not updated")

    def delete_user_service(self, token: str) -> HTTPException:
        """
        Удалить пользователя.
        """
        try:
            user = self.user_token_uwo.get_user_by_token_uow(token)
            success = self.user_repo.delete_user(user)
            if not success:
                raise HTTPException(status_code=404, detail="User not found")
            return HTTPException(status_code=200, detail="User successfully deleted")
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail="User not deleted")
