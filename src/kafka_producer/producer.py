from typing import Optional

from aiokafka import AIOKafkaProducer
import asyncio
import json

from src.kafka_producer.config import settings_kafka


class KafkaProducer:
    def __init__(self):
        self._producer: Optional[AIOKafkaProducer] = None
        self._started: bool = False

    async def start(self):
        if not self._started:
            self._producer = AIOKafkaProducer(
                bootstrap_servers=settings_kafka.KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v).encode("utf-8")
            )
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

    async def startup_connection(self):
        await asyncio.sleep(10)
        for i in range(10):
            try:
                await self.start()
                print("Kafka connected")
                break
            except Exception as e:
                print(f"Kafka not ready (attempt {i + 1}/10): {e}")
                await asyncio.sleep(5)
        else:
            raise RuntimeError("Kafka connection failed after 10 attempts")


try:
    kafka_producer = KafkaProducer()
except Exception as e:
    raise e
