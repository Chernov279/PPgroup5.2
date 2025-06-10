import datetime
from typing import Optional

from src.user.user_schemas import UserBaseSchema


class UserActivityInternal(UserBaseSchema):
    is_active: Optional[bool]
    last_active_time: Optional[datetime.datetime]
