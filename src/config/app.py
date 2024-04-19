from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='users_')

    host: str
    port: int

    debug: bool


APP_CONFIG = AppConfig()
