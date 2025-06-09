from aiokafka import AIOKafkaProducer
import json

from aiokafka.errors import KafkaConnectionError

from src.kafka_producer.config import settings_kafka
from src.kafka_producer.producer import KafkaProducer
from src.user.user_activity_service import UserActivityService


class KafkaProducerService(KafkaProducer):
    def __init__(self,):
        super().__init__()

    async def send_user_registered(self, user_data: dict):
        await self.start()  # ОБЯЗАТЕЛЕН
        await self._producer.send_and_wait(
            topic="user_login",
            value=user_data,
        )

auth_kaffka = KafkaProducerService()
from aiokafka import AIOKafkaConsumer
import json
import asyncio

KAFKA_TOPIC = "user-events"

async def consume_user_events():
    for _ in range(5):  # до 5 попыток
        try:
            consumer = AIOKafkaConsumer(
                "user_login",
                bootstrap_servers=settings_kafka.KAFKA_BOOTSTRAP_SERVERS,
                group_id="user-activity-group",
                value_deserializer=lambda m: json.loads(m.decode("utf-8"))
            )
            await consumer.start()
            print("Kafka запустилась корректно")
            break
        except KafkaConnectionError as e:
            print("Kafka не доступна, пробую снова через 5 секунд...")
            await asyncio.sleep(5)
    else:
        print("Не удалось подключиться к Kafka")
        return

    try:
        async for msg in consumer:
            event = msg.value
            # обработка
    finally:
        await consumer.stop()


async def handle_user_registered(event: dict):
    user_id = event["user_id"]
    registered_at = event["registered_at"]

    # Используем сервис активности (или UoW)
    service = UserActivityService
    await service.log_registration_event(user_id, registered_at)
