from datetime import datetime, timedelta
from typing import Optional

from src.user.user_repository import UserRepository
from src.user.user_schemas import UserActivity


class UserActivityService:
    # Класс для отслеживания активности пользователя: обновляет активность пользователя и возвращает значение

    def __init__(self, db_session = None, user_repository: Optional[UserRepository] = None):
        if user_repository is None:
            self.user_repository = UserRepository(db_session)
        else:
            self.user_repository = user_repository

    INACTIVITY_THRESHOLD = timedelta(minutes=5)  # Время, после которого пользователь считается оффлайн
    INACTIVITY_UPDATE_THRESHOLD = timedelta(minutes=3)

    async def update_user_activity_service(self, user_id: int):
        """Обновляет активность текущего пользователя в базе данных"""
        user = await self.user_repository.get_user_by_id(user_id, UserActivity.get_selected_columns())
        if not user:
            return

        current_time = datetime.utcnow()

        if current_time - user.last_active_time > self.INACTIVITY_UPDATE_THRESHOLD:
            await self.user_repository.update_user_activity(user_id, last_active_time=current_time, is_active=True)

    async def get_activity(self, user_id: int) -> dict:
        """Возвращает активность пользователя и форматирует ее"""
        user = await self.user_repository.get_user_by_id(user_id, UserActivity.get_selected_columns())
        if not user:
            return {"is_active": False, "last_active_time": None, "formatted": "Неизвестно"}

        now = datetime.utcnow()
        if user.is_active and now - user.last_active_time > self.INACTIVITY_THRESHOLD:
            user.is_active = False

        formatted = self.format_user_activity(user.last_active_time, user.is_active)
        return {"is_active": user.is_active, "last_active_time": user.last_active_time, "formatted": formatted}

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
