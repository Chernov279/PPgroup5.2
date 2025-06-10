from datetime import datetime, timedelta
from typing import Optional

from src.exceptions.base_exceptions import AppException
from src.user.user_repository import UserRepository
from src.user.user_schemas import UserActivity
from src.user_activity.unit_of_work import UserActivityUnitOfWork


class UserActivityService:
    # Класс для отслеживания активности пользователя: обновляет активность пользователя и возвращает значение

    def __init__(self, db_session=None, user_repository: Optional[UserRepository] = None):
        if db_session is not None:
            self.user_repository = UserRepository(db_session)
            self.user_activity_uow = UserActivityUnitOfWork(db_session)
        elif user_repository is not None:
            self.user_repository = user_repository
            self.user_activity_uow = UserActivityUnitOfWork(user_repository.db_session)
        else:
            raise AppException(detail=f"No session for {self.__class__.__name__}")

    INACTIVITY_THRESHOLD = timedelta(minutes=5)  # Время, после которого пользователь считается оффлайн
    INACTIVITY_UPDATE_THRESHOLD = timedelta(minutes=3)

    async def update_user_activity_service(self, user_id: int):
        """Обновляет активность текущего пользователя в базе данных. """
        user = await self.user_repository.get_user_by_id(user_id, UserActivity.get_selected_columns())
        if not user:
            return

        current_time = datetime.utcnow()

        if current_time - user.last_active_time > self.INACTIVITY_UPDATE_THRESHOLD:
            await self.user_activity_uow.update_user_activity_uow(user_id, is_active=False)
        # else:
        #     await self.user_activity_uow.update_user_activity_uow(user_id, is_active=True)

    async def get_activity(self, user_id: int) -> dict:
        """Возвращает активность пользователя и форматирует ее"""
        user = await self.user_repository.get_user_by_id(user_id, UserActivity.get_selected_columns())
        if not user:
            return {"is_active": False, "last_active_time": None, "formatted": "Неизвестно"}

        now = datetime.utcnow()
        is_active = user.is_active
        if user.is_active and now - user.last_active_time > self.INACTIVITY_THRESHOLD:
            is_active = False
            await self.user_activity_uow.update_user_activity_uow(user_id, is_active=False)

        formatted = self.format_user_activity(user.last_active_time, is_active)
        return {"is_active": is_active, "last_active_time": user.last_active_time, "formatted": formatted}

    async def update_active_user_service(self, user_id: int):
        current_time = datetime.utcnow()

        await self.user_activity_uow.update_active_user_uow(user_id, last_active_time=current_time, is_active=True)
        return {"is_active": True, "last_active_time": current_time}

    @staticmethod
    def format_user_activity(last_active_time: datetime, is_active: bool) -> str:
        """Форматирует время последней активности"""
        if is_active:
            return "В сети"

        now = datetime.utcnow()
        diff = now - last_active_time

        if diff < timedelta(minutes=1):
            return "Только что"
        elif diff < timedelta(hours=1):
            minutes = diff.seconds // 60
            return f"{minutes} минут назад"
        elif diff < timedelta(days=1):
            hours = diff.seconds // 3600
            return f"{hours} часов назад"
        elif diff < timedelta(days=2):
            return "Вчера"
        elif diff < timedelta(days=7):
            days = diff.seconds // (3600 * 24)
            return f"{days} дней назад"
        elif diff < timedelta(days=29):
            weeks = diff.seconds // (3600 * 24 * 7)
            return f"{weeks} недель назад"
        elif diff < timedelta(days=365):
            months = diff.seconds // (3600 * 24 * 7 * 30)
            return f"{months} месяцев назад"
        else:
            return "Давно"