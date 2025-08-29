from src.kafka.producers.producer import BaseKafkaProducer, kafka_producer


class UserActivityProducer:
    def __init__(self, producer: BaseKafkaProducer):
        self._p = producer
        self._topic = "user_activity"

    async def send_user_activity(self, event: str, user_id: int, wait: bool = False):
        payload = {"event": event, "user_id": user_id}
        await self._p.send(self._topic, payload, wait=wait)


user_activity_producer = UserActivityProducer(kafka_producer)
