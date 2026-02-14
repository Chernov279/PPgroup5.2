import logging

from src.kafka.consumers.base_consumer import BaseKafkaConsumer

logger = logging.getLogger(__name__)


class UserActiveKafkaConsumer(BaseKafkaConsumer):
    topics = ["user_activity"]
    group_id = "user-activity-group"

    async def _handle_message(self, event: dict) -> None:
        user_id = event.get("user_id")
        logger.debug("Received user_active event: %s", event)
        if user_id is None:
            logger.warning("Invalid user_active event without user_id: %s", event)
            return

        try:
            pass
        except Exception:
            logger.exception("Failed handling user_active event for user_id=%s", user_id)


user_activity_kafka_consumer = UserActiveKafkaConsumer()
