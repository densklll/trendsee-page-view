from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

_BACKEND_ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_BACKEND_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Порты с хоста при `docker compose up db redis` (см. docker-compose.yml).
    # В контейнере API переменные DATABASE_URL / REDIS_URL задаёт compose.
    database_url: str = (
        "postgresql://postgres:postgres@127.0.0.1:5433/publications"
    )
    redis_url: str = "redis://127.0.0.1:6380/0"
    jwt_secret: str = "super-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    publication_cache_ttl: int = 600


settings = Settings()
