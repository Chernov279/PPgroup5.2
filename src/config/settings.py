from pathlib import Path
from typing import List
from pydantic import computed_field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ============================================
    # Проект
    # ============================================
    PROJECT_NAME: str = "VeloApp"
    DEBUG: bool = False
    VERSION: str = "1.0"
    CORS_ALLOWED_ORIGINS: List[str] = ["*"]

    # ============================================
    # База данных
    # ============================================
    POSTGRES_DB: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int = 5432
    POSTGRES_ECHO_LOG: bool = False

    # ============================================
    # Redis
    # ============================================
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str | None = None

    # ============================================
    # Kafka
    # ============================================
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"

    # ============================================
    # JWT
    # ============================================
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # ============================================
    # Computed fields (строятся автоматически)
    # ============================================
    @computed_field
    @property
    def POSTGRES_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @computed_field
    @property
    def POSTGRES_URL_SYNC(self) -> str:
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @computed_field
    @property
    def REDIS_URL(self) -> str:
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    # ============================================
    # Validators
    # ============================================
    @field_validator("CORS_ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_cors(cls, v: str | List[str]) -> List[str]:
        """Поддержка строки через запятую из .env"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        if len(v) < 32:
            raise ValueError("SECRET_KEY должен быть не менее 32 символов")
        return v
    
    # model_config = SettingsConfigDict(
    #     env_file=str(Path(__file__).parent.parent.parent / ".env"),
    #     extra="ignore",
    #     env_file_encoding="utf-8",
    # )
    
settings = Settings() # type: ignore