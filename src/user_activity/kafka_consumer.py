from src.config import db_helper
from src.kafka.consumer import BaseKafkaConsumer
from src.user_activity.user_activity_service import UserActivityService


class UserActiveKafkaConsumer(BaseKafkaConsumer):
    topics = ["user_active"]
    group_id = "user-activity-group"

    async def _handle_message(self, event: dict):
        user_id = event.get("user_id")
        print(user_id, "UserActiveKafkaConsumer")
        if user_id is None:
            print("Invalid event, no user_id")
            return

        async with db_helper.get_db_session() as session:
            service = UserActivityService(db_session=session)
            await service.update_active_user_service(user_id)


user_activity_kafka_consumer = UserActiveKafkaConsumer()
