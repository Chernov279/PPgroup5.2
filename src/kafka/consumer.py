import asyncio
import json
from abc import ABC, abstractmethod

from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaConnectionError

from src.kafka.config import settings_kafka


class BaseKafkaConsumer(ABC):
    topics: list[str] = []
    group_id: str = "default-group"

    def __init__(self):
        self._consumer: AIOKafkaConsumer | None = None
        self._running = False

    async def start(self):
        if not self.topics:
            raise ValueError("No topics specified for consumer")
        self._consumer = AIOKafkaConsumer(
            *self.topics,
            bootstrap_servers=settings_kafka.KAFKA_BOOTSTRAP_SERVERS,
            group_id=self.group_id,
            value_deserializer=lambda m: json.loads(m.decode("utf-8"))
        )
        for attempt in range(5):
            try:
                await self._consumer.start()
                self._running = True
                print(f"Consumer for {self.topics} started")
                break
            except KafkaConnectionError as e:
                print(f"Kafka unavailable (attempt {attempt+1}/5): {e}")
                await asyncio.sleep(5)
        else:
            raise RuntimeError(f"Failed to connect to Kafka after 5 attempts")

    async def consume(self):
        if not self._consumer:
            raise RuntimeError("Consumer not initialized")

        try:
            async for msg in self._consumer:
                await self._handle_message(msg.value)
        finally:
            await self.stop()

    async def stop(self):
        if self._consumer and self._running:
            await self._consumer.stop()
            self._running = False
            print(f"Consumer for {self.topics} stopped")

    @abstractmethod
    async def _handle_message(self, event: dict):
        ...
