from aiokafka import AIOKafkaProducer
import asyncio
import json

from src.kafka_producer.config import settings_kafka


class KafkaProducer:
    def __init__(self):
        self._producer = AIOKafkaProducer(
            bootstrap_servers=settings_kafka.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )
        self._started = False

    async def start(self):
        if not self._started:
            await self._producer.start()
            self._started = True

    async def stop(self):
        if self._started:
            await self._producer.stop()
            self._started = False

    async def send(self, topic: str, message: dict):
        if not self._started:
            await self.start()
        await self._producer.send(topic, message)


try:
    kafka_producer = KafkaProducer()
except Exception as e:
    raise e
