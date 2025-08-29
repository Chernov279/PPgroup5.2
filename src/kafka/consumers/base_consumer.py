import asyncio
import json
import logging
from abc import ABC, abstractmethod
from typing import Optional

from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaConnectionError

from src.kafka.config import settings_kafka

logger = logging.getLogger(__name__)


class BaseKafkaConsumer(ABC):
    """
    Базовый потребитель Kafka.
    - start(): поднимает AIOKafkaConsumer и запускает background task _consume_loop
    - stop(): отменяет task и гарантированно вызывает consumer.stop()
    - _handle_message(): реализуется в подклассе
    """

    topics: list[str] = []
    group_id: str = "default-group"

    def __init__(self):
        self._consumer: Optional[AIOKafkaConsumer] = None
        self._task: Optional[asyncio.Task] = None
        self._running: bool = False

    async def start(self) -> None:
        """Подключение и запуск фонового цикла"""
        if self._running:
            logger.debug("Consumer already running for topics=%s", self.topics)
            return

        if not self.topics:
            raise ValueError("No topics specified for consumer")

        self._consumer = AIOKafkaConsumer(
            *self.topics,
            bootstrap_servers=settings_kafka.KAFKA_BOOTSTRAP_SERVERS,
            group_id=self.group_id,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        )

        # Пытаемся подключиться к Kafka
        attempts = 5
        timeout = 5
        for i in range(attempts):
            try:
                await self._consumer.start()
                self._running = True
                logger.info("Kafka consumer started for topics=%s group=%s", self.topics, self.group_id)
                break
            except KafkaConnectionError as e:
                logger.warning("Kafka connect attempt %d/%d failed: %s", i + 1, attempts, e)
                await asyncio.sleep(timeout)
        else:
            raise RuntimeError(f"Failed to start Kafka consumer for topics {self.topics}")

        # запускаем фоновую таску для чтения сообщений
        self._task = asyncio.create_task(self._consume_loop(), name=f"kafka-consumer-{self.group_id}")

    async def _consume_loop(self) -> None:
        """Выполнение логики со стороны kafka consumer ов"""
        assert self._consumer is not None, "Consumer not initialized"
        try:
            async for msg in self._consumer:
                try:
                    await self._handle_message(msg.value)
                except Exception:
                    logger.exception("Error handling kafka message from topic=%s partition=%s offset=%s",
                                     msg.topic, msg.partition, msg.offset)
        except asyncio.CancelledError:
            # отмена — ожидаем выйти и корректно остановить consumer в finally
            logger.debug("Consume task cancelled for topics=%s", self.topics)
            raise
        except Exception:
            logger.exception("Unexpected error in consumer loop for topics=%s", self.topics)
        finally:
            if self._consumer is not None:
                try:
                    await self._consumer.stop()
                    logger.info("Kafka consumer stopped (finalized) for topics=%s", self.topics)
                except Exception:
                    logger.exception("Error while stopping consumer for topics=%s", self.topics)
            self._running = False
            self._task = None

    async def stop(self) -> None:
        """Останавливает фоновую таску и consumer"""
        if not self._running and self._task is None:
            logger.debug("stop() called but consumer not running for topics=%s", self.topics)
            return

        self._running = False

        if self._task:
            # отмена работы текущей таски
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                logger.debug("Consume task cancelled and awaited for topics=%s", self.topics)
            except Exception:
                logger.exception("Error while awaiting consumer task for topics=%s", self.topics)
            finally:
                self._task = None

        if self._consumer is not None:
            try:
                await self._consumer.stop()
            except Exception:
                logger.exception("Error stopping consumer for topics=%s", self.topics)
            finally:
                self._consumer = None

        logger.info("Kafka consumer fully stopped for topics=%s", self.topics)

    @abstractmethod
    async def _handle_message(self, event: dict):
        """Бизнес-логика обработки сообщения"""
        ...
