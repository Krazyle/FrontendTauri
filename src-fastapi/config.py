from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


_BACKEND_DIR = Path(__file__).resolve().parent
_ENV_FILES = (
    _BACKEND_DIR / ".env",
    _BACKEND_DIR.parent / ".env",
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_ENV_FILES,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str | None = None
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "geon"

    pg_featureserv_url: str = "http://localhost:9000"
    app_external_url: str = "http://localhost:8000"

    default_schema_name: str = "user_data"
    default_geometry_column: str = "geom"
    default_id_column: str = "fid"
    default_srid: int = 4326
    default_crs: str = "http://www.opengis.net/def/crs/OGC/1.3/CRS84"

    proxy_timeout_seconds: float = 10.0

    collections_default_import_status: str = "importing"
    cors_allowed_origins: list[str] = ["*"]

    @property
    def sqlalchemy_database_url(self) -> str:
        if self.database_url:
            return normalize_database_url(self.database_url)

        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


def normalize_database_url(database_url: str) -> str:
    if database_url.startswith("postgresql://"):
        return database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    if database_url.startswith("postgres://"):
        return database_url.replace("postgres://", "postgresql+asyncpg://", 1)
    return database_url


@lru_cache
def get_settings() -> Settings:
    return Settings()
