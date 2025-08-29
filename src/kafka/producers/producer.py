import logging
from typing import Optional

from aiokafka import AIOKafkaProducer
import asyncio
import json

from aiokafka.errors import KafkaConnectionError

from src.kafka.config import settings_kafka

logger = logging.getLogger(__name__)


class BaseKafkaProducer:
    """
    Базовый Kafka producer
    - start(): поднимает AIOKafkaProducer и подключается к
    - stop(): idempotent — если не запущен, возвращает.
    - send(topic, message, wait=False):
        * wait=True  -> send_and_wait (ждём подтверждения от брокера)
        * wait=False -> fire-and-forget (через create_task + callback для логирования ошибок)
    """

    def __init__(self):
        self._producer: Optional[AIOKafkaProducer] = None
        self._started: bool = False

    async def _create_and_start(self) -> None:
        """Внутренний метод: создаёт producer и стартует его (без retry)."""
        self._producer = AIOKafkaProducer(
            bootstrap_servers=settings_kafka.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        await self._producer.start()
        self._started = True
        logger.info("Kafka producer started (bootstrap=%s)", settings_kafka.KAFKA_BOOTSTRAP_SERVERS)

    async def start(self, attempts: int = 5, timeout: float = 5.0) -> None:
        """
        Попытаться стартовать producer с фиксированными retry.
        """
        if self._started:
            logger.debug("Kafka producer already started")
            return

        last_exc = None
        for i in range(attempts):
            try:
                await self._create_and_start()
                return
            except KafkaConnectionError as e:
                last_exc = e
                logger.warning("Kafka producer connect attempt %d/%d failed: %s", i + 1, attempts, e)
                await asyncio.sleep(timeout)
            except Exception as e:
                last_exc = e
                logger.exception("Unexpected error while starting kafka producer (attempt %d/%d)", i + 1, attempts)
                await asyncio.sleep(timeout)

        logger.error("Kafka producer failed to start after %d attempts", attempts)
        raise RuntimeError("Kafka producer failed to start") from last_exc

    async def stop(self) -> None:
        """Остановить producer — idempotent."""
        if not self._started:
            logger.debug("Kafka producer stop() called but producer not started")
            return

        try:
            if self._producer is not None:
                await self._producer.stop()
        except Exception:
            logger.exception("Error while stopping kafka producer")
        finally:
            self._producer = None
            self._started = False
            logger.info("Kafka producer stopped")

    async def _send_and_wait(self, topic: str, message: dict):
        """Внутренний awaited send -> ждем ack от брокера (metadata)."""
        assert self._producer is not None, "Producer not started"
        metadata = await self._producer.send_and_wait(topic, message)
        return metadata

    async def send(self, topic: str, message: dict, wait: bool = False):
        """
        Отправить сообщение.
        - wait=True: дождаться подтверждения (send_and_wait) — полезно для важных событий.
        - wait=False: fire-and-forget: запускается в фоне; ошибки логируются через callback.
        """
        if not self._started or self._producer is None:
            await self.start()

        from src.kafka.producers.producer_message_enricher import MessageEnricher
        enriched_message = MessageEnricher.enrich(message)

        logger.debug("Kafka producer sending topic=%s, preview=%s", topic, _preview(enriched_message))
        logger.info("Kafka producer send topic=%s", topic)

        if wait:
            return await self._send_and_wait(topic, enriched_message)
        else:
            task = asyncio.create_task(self._send_and_wait(topic, enriched_message))
            task.add_done_callback(self._send_done_callback)
            return None

    @staticmethod
    def _send_done_callback(task: asyncio.Task) -> None:
        """Callback, который логирует ошибку fire-and-forget отправки (если она была)."""
        try:
            exc = task.exception()
        except asyncio.CancelledError:
            logger.debug("Fire-and-forget send task was cancelled")
            return

        if exc:
            logger.exception("Fire-and-forget kafka send failed: %s", exc)


def _preview(message: dict, max_len: int = 200) -> str:
    """Короткая preview-строка для логов"""
    try:
        s = json.dumps(message, ensure_ascii=False)
    except Exception:
        s = str(message)
    if len(s) > max_len:
        return s[:max_len] + "..."
    return s


try:
    kafka_producer = BaseKafkaProducer()
except Exception as e:
    raise e
