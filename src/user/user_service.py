from typing import List

from fastapi import HTTPException

from src.models.models import User
from src.user.user_repositories import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def get_user_or_404_service(self, user_id: int) -> User:
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def get_users_service(self) -> List[User]:
        user = self.user_repo.get_users()
        return user

    def create_user_service(self, name: str, email: str, hashed_password: str, ) -> User | None:
        """
        Создать нового пользователя.
        """
        try:
            return self.user_repo.create_user(name, email, hashed_password)
        except Exception as e:
            raise HTTPException(status_code=500, detail="User not created")

    def update_user_service(self, user_id: int, name: str) -> User | None:
        """
        Обновить данные пользователя.
        """
        try:
            user = self.user_repo.update_user(user_id, name)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user
        except HTTPException as e:
            raise e
        except Exception:
            raise HTTPException(status_code=500, detail="User not updated")

    def delete_user_service(self, user_id: int) -> bool:
        """
        Удалить пользователя.
        """
        try:
            success = self.user_repo.delete_user(user_id)
            if not success:
                raise HTTPException(status_code=404, detail="User not found")
            return success
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail="User not deleted")
    #
    # def get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)]) -> User | None:
    #     """
    #     Получить пользователя по токену.
    #     """
    #     user_id = verify_jwt_token(token).get("sub", None)
    #     if user_id:
    #         return self.db.query(User).filter(User.id == int(user_id)).first()

