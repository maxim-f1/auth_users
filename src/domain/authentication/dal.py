from uuid import UUID, uuid4

from src.config.auth import AUTH_CONFIG
from src.database.redis.connection import RedisSession
from src.domain.authentication.dto import RefreshTokenDTO
from src.domain.authentication.exception import AuthenticationExceptions
from src.domain.user.dto import RoleEnum


class AuthenticationDAO:
    def __init__(self, redis_session: RedisSession):
        self.redis_session = redis_session

    async def create_refresh_token(
            self,
            user_id: str | UUID,
            role: str | RoleEnum
    ) -> str:
        refresh_token = str(uuid4())
        if isinstance(role, RoleEnum):
            role = str(role.value)
        await self.redis_session.set_item(
            f'{refresh_token},{str(user_id)}',
            role,
            AUTH_CONFIG.refresh_exp_sec
        )
        return refresh_token

    async def pop_refresh_token(
            self,
            *,
            refresh_token: str | UUID | None = None,
            user_id: str | UUID | None = None
    ) -> RefreshTokenDTO | None:
        pattern = '*'
        if refresh_token is None and user_id is None:
            raise AuthenticationExceptions.RefreshNotFound
        elif user_id is not None:
            pattern = f'*,{str(user_id)}'
        elif refresh_token is not None:
            pattern = f'{str(refresh_token)},*'

        tokens_keys = await self.redis_session.get_keys(pattern=pattern)
        if len(tokens_keys) == 0:
            return None
        token_key = tokens_keys[0]

        role = await self.redis_session.get_value(token_key)
        await self.redis_session.delete_item(token_key)
        return RefreshTokenDTO.fabric(token_key, role)