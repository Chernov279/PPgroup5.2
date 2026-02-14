import logging
import time
from typing import List

from sqlalchemy import text
from aiokafka.errors import KafkaConnectionError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.base_model import DeclarativeBaseModel
from src.kafka.consumers.base_consumer import BaseKafkaConsumer
from src.kafka.producers.producer import kafka_producer
from src.redis.redis_helper import redis_dbs


logger = logging.getLogger(__name__)


async def check_kafka(kafka_consumers: List[BaseKafkaConsumer]):
    """
    Проверка Kafka:
      1) send_and_wait (producer) — проверка, что брокер принял сообщение (ack)
      2) проверка, что хотя бы один consumer в переданном списке помечен как запущенный (._running True)
         - если kafka_consumers is None -> логируем и пропускаем проверку по consumer-ам
    Если нужно полное E2E (consumer реально обработал сообщение), см. ниже вариант с correlation_id и shared event.
    """
    logger.info("Kafka healthcheck: sending health message to topic=%s", 'healthcheck')
    try:
        await kafka_producer.send('healthcheck', {'ts': time.time()}, wait=True)
        logger.info("Kafka healthcheck: producer send_and_wait succeeded")
    except KafkaConnectionError as e:
        logger.exception("Kafka connection error during send")
        raise RuntimeError(f"Kafka unavailable: {e}") from e
    except Exception as e:
        logger.exception("Kafka general error during send")
        raise RuntimeError(f"Kafka send failed: {e}") from e
    number_running_consumers = 0
    non_running_consumers = []
    for cons in kafka_consumers:
        running = bool(
            getattr(cons, "_running", False)
            or getattr(cons, "_started", False)
            or getattr(cons, "is_running", False)
        )
        if running:
            number_running_consumers += 1
        else:
            non_running_consumers.append(cons)

    if not non_running_consumers:
        logger.info("Kafka healthcheck: all consumers are running")

    else:
        names = [getattr(cons, "group_id", str(cons)) for cons in non_running_consumers]
        logger.error(
            "Kafka healthcheck: some consumers aren't running (%s/%s running). Problematic: %s",
            number_running_consumers,
            len(kafka_consumers),
            ", ".join(names),
            )
        raise RuntimeError("Some Kafka consumers aren't running: " + ", ".join(names))


async def check_redis():
    """
    Проверяет каждую подключенную redis db вызовом ping().
    Поднимает RuntimeError в случае ошибки.
    """
    logger.info("Redis healthcheck: checking %d redis DBs", len(redis_dbs))
    for idx, redis_db in enumerate(redis_dbs):
        try:
            pong = await redis_db.ping()
            if not pong:
                logger.error("Redis healthcheck: redis_db[%d] returned falsy pong", idx)
                raise RuntimeError(f"Redis {idx} did not return PONG")
            logger.debug("Redis healthcheck: redis_db[%d] PONG OK", idx)
        except Exception as e:
            logger.exception("Redis healthcheck: redis_db[%d] ping failed", idx)
            raise RuntimeError(f"Redis unavailable (db index {idx}): {e}") from e
    logger.info("Redis healthcheck: all redis DBs OK")


async def check_postgres(session: AsyncSession):
    logger.info("Postgres healthcheck: checking declared tables presence")
    result = await session.execute(
        text("""
            SELECT tablename
            FROM pg_tables
            WHERE schemaname = 'public'
        """)
    )
    existing_tables = {row[0] for row in result.fetchall()}

    declared_tables = set(DeclarativeBaseModel.metadata.tables.keys())

    missing_tables = declared_tables - existing_tables
    if missing_tables:
        logger.error("Postgres healthcheck: missing tables: %s", ", ".join(sorted(missing_tables)))
        raise RuntimeError(f"Missing tables: {', '.join(missing_tables)}")
    logger.info("Postgres healthcheck: all declared tables present")
