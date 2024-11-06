from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='redis_')

    host: str = 'redis'
    port: int = 6179
    driver: str = 'redis'
    user: str = 'default'
    password: str = 'password'
    api_index: int = 1
    bot_index: int = 2
    encoding: str = 'utf8'
    decode_responses: bool = True

    def get_redis_attributes(self, index: int) -> dict[str, str | int | bool]:
        return {
            'url': self.get_connection_url(index),
            'encoding': self.encoding,
            'decode_responses': self.decode_responses,
        }

    def get_connection_url(self, index: int) -> str:
        return f'{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}//{index}'


REDIS_CONFIG = RedisConfig()
