from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='users_')

    host: str = 'localhost'
    port: int = 8001

    debug: bool = True


APP_CONFIG = AppConfig()
