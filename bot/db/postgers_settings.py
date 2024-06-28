import os
from pydantic import SecretStr
from pydantic_settings import BaseSettings
from sqlalchemy import URL


class PostgresSettings(BaseSettings):
    """Конфигурация PostgresQL."""

    POSTGRES_HOST: str = os.getenv('POSTGRES_HOST')
    POSTGRES_PORT: int = int(os.getenv('POSTGRES_PORT'))
    POSTGRES_USER: str = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD: SecretStr = SecretStr(os.getenv('POSTGRES_PASSWORD'))
    POSTGRES_DB: str = os.getenv('POSTGRES_DB')

    @property
    def postgres_connection_url(self) -> URL:
        return URL.create(
            drivername="postgresql+psycopg2",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD.get_secret_value(),
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            database=self.POSTGRES_DB,
        )


settings = PostgresSettings()
