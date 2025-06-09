from sqlalchemy import text
from aiokafka.errors import KafkaConnectionError

from src.config import db_helper
from src.kafka_producer.producer import kafka_producer
from src.models.base_model import DeclarativeBaseModel
from src.redis.redis_helper import redis_dbs


async def check_kafka():
    try:
        await kafka_producer.send("healthcheck_topic", {"status": "ping"})
    except KafkaConnectionError as e:
        raise RuntimeError(f"Kafka unavailable: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Kafka general error: {str(e)}")


async def check_redis():
    for redis_db in redis_dbs:
        try:
            pong = await redis_db.ping()
            if not pong:
                raise RuntimeError(f"Redis {redis_db} did not return PONG")
        except Exception as e:
            raise RuntimeError(f"Redis unavailable: {str(e)}")


async def check_postgres():
    async with db_helper.get_db_session() as session:
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
        raise RuntimeError(f"Missing tables: {', '.join(missing_tables)}")
    print("All declared tables are present.")
