from pathlib import Path

from pydantic import ValidationError
from pydantic_settings import BaseSettings


class KafkaSettings(BaseSettings):
    # получение чувствительных данных из корневой папки

    KAFKA_BOOTSTRAP_SERVERS: str
    KAFKA_TOPIC: str = "user-events"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        # missing_fields = [
        #     field for field in [
        #         "PROJECT_NAME",
        #         "DEBUG",
        #         "VERSION"
        #     ]
        #     if not getattr(self, field, None)
        # ]
        # if missing_fields:
        #     raise ValueError(f"Следующие параметры не переданы или пустые: {', '.join(missing_fields)}")

    # получение данных из файла .env
    model_config = {
        "env_file": str(Path(__file__).parent.parent.parent / ".env"),
        "extra": "ignore"
    }


try:
    settings_kafka = KafkaSettings()
except ValidationError as e:
    print("Ошибка валидации Pydantic:", e)
except ValueError as e:
    print("Ошибка инициализации настроек:", e)
