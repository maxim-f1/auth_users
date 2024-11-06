from pydantic_settings import BaseSettings
from sqlalchemy import URL


class PostgresConfig(BaseSettings):
    user: str = 'postgres'
    host: str = 'postgres'
    port: int = 5432
    db: str = 'postgres'
    driver: str = 'postgresql+asyncpg'
    password: str = 'postgres'
    ddl_show: bool = False

    def connection_url(self) -> URL:
        return URL.create(
            drivername=self.driver,
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.db,
        )


POSTGRES_CONFIG = PostgresConfig(_env_file='.env', _env_prefix='POSTGRES_')
