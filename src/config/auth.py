from typing import Dict, Any

from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='auth_')

    secret: str = 'secret'
    algorithm: str = 'HS256'

    session_ttl_sec: int = 60 * 15

    refresh_key: str = 'refresh'
    refresh_exp_sec: int = 60 * 60 * 24 * 14

    access_key: str = 'access'
    access_exp_sec: int = 60 * 2

    def cookies_kwargs(self) -> Dict[str, Any]:
        kwargs = {
            'samesite': 'none',
            'secure': False,
            'httponly': False
        }
        return kwargs


AUTH_CONFIG = AuthConfig()
