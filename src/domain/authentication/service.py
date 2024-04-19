import hashlib
from typing import List, Annotated
from uuid import uuid4, UUID

from fastapi import Body, Response, Security, HTTPException
from fastapi.security import HTTPBearer, APIKeyCookie, HTTPAuthorizationCredentials
from jwt import PyJWT, InvalidTokenError
from pydantic import SecretStr
from starlette.requests import Request

from src.config.auth import AUTH_CONFIG
from src.database.redis.depends import get_redis_session
from src.database.postgres.depends import get_session
from src.domain.authentication.dal import AuthenticationDAO
from src.domain.authentication.dto import UserSignInDTO, AccessTokenDTO, RefreshTokenDTO
from src.domain.authentication.exception import AuthenticationExceptions
from src.domain.user.dal import UserDAO
from src.domain.user.dto import UserSecureCredentialsDTO, RoleEnum
from src.utils.time import get_now_with_delta


class Hasher:
    @staticmethod
    def get_password_hash(password: str | SecretStr) -> str:
        if isinstance(password, SecretStr):
            password = password.get_secret_value()
        salt = uuid4().hex
        return f'{hashlib.sha256(salt.encode() + password.encode()).hexdigest()}:{salt}'

    @staticmethod
    def verify_password(plain_password: str, hashed_password_with_salt: str) -> bool:
        hashed_password, salt = hashed_password_with_salt.split(':')
        return hashed_password == hashlib.sha256(salt.encode() + plain_password.encode()).hexdigest()


class JWT:
    jwt = PyJWT(
        {
            'verify_signature': True, 'verify_aud': False, 'verify_iat': False, 'verify_exp': True, 'verify_nbf': False,
            'verify_iss': False, 'verify_sub': True, 'verify_jti': True, 'verify_at_hash': False, 'require_aud': False,
            'require_iat': False, 'require_exp': True, 'require_nbf': False, 'require_iss': False, 'require_sub': True,
            'require_jti': True, 'require_at_hash': False, 'leeway': 99999,
        }
    )

    @classmethod
    def encode(cls, claims: dict[str, str | int]) -> str:
        return cls.jwt.encode(claims, AUTH_CONFIG.secret, algorithm=AUTH_CONFIG.algorithm)

    @classmethod
    def decode(cls, token: str) -> dict[str, str | int]:
        try:
            return cls.jwt.decode(token, AUTH_CONFIG.secret, algorithms=[AUTH_CONFIG.algorithm])
        except InvalidTokenError:
            raise AuthenticationExceptions.InvalidCredentials


refresh_bearer_depends = Annotated[
    HTTPAuthorizationCredentials | None,
    Security(
        HTTPBearer(
            scheme_name='Bearer', description='Set refresh token to header (without Bearer in start).',
            auto_error=False
        )
    )
]

refresh_cookies_depends = Annotated[
    str | None,
    Security(
        APIKeyCookie(
            name=AUTH_CONFIG.refresh_key, description='Set refresh token to cookies.', auto_error=False,
        )
    )
]

access_bearer_depends = Annotated[
    HTTPAuthorizationCredentials | None,
    Security(
        HTTPBearer(
            scheme_name='Bearer', description='Set refresh token to header (without Bearer in start).',
            auto_error=False
        )
    )
]

access_cookies_depends = Annotated[
    str | None,
    Security(
        APIKeyCookie(
            name=AUTH_CONFIG.access_key, description='Set refresh token to cookies.', auto_error=False,
        )
    )
]


def check_access(
        allowed_roles: List[RoleEnum],
        bearer_token: access_bearer_depends,
        cookies_token: access_cookies_depends
) -> AccessTokenDTO:
    if bearer_token is not None:
        token = bearer_token.credentials
    elif cookies_token is not None:
        token = cookies_token
    else:
        raise AuthenticationExceptions.AccessNotFound

    token_payload = AccessTokenDTO.model_validate(JWT.decode(token))

    if token_payload.exp < int(get_now_with_delta().timestamp()):
        raise AuthenticationExceptions.AccessExpires

    if token_payload.role not in allowed_roles:
        raise AuthenticationExceptions.InvalidRole

    return token_payload


async def check_refresh(
        refresh_bearer_token: refresh_bearer_depends,
        refresh_cookies_token: refresh_cookies_depends,
        redis_session: get_redis_session
) -> RefreshTokenDTO:
    if refresh_bearer_token is not None:
        refresh_token = refresh_bearer_token.credentials
    elif refresh_cookies_token is not None:
        refresh_token = refresh_cookies_token
    else:
        raise AuthenticationExceptions.RefreshNotFound

    refresh_payload = await AuthenticationDAO(redis_session).pop_refresh_token(refresh_token=refresh_token)
    if refresh_payload is None:
        raise AuthenticationExceptions.InvalidCredentials
    return refresh_payload


class RoleFilter:
    __slots__ = ('allowed_roles',)

    def __init__(self, allowed_roles: List[RoleEnum]):
        self.allowed_roles = allowed_roles

    async def __call__(
            self,
            response: Response,
            access_bearer_token: access_bearer_depends,
            access_cookies_token: access_cookies_depends,
            refresh_bearer_token: refresh_bearer_depends,
            refresh_cookies_token: refresh_cookies_depends,
            redis_session: get_redis_session
    ) -> AccessTokenDTO:
        try:
            access_payload = check_access(self.allowed_roles, access_bearer_token, access_cookies_token)
            return access_payload
        except HTTPException as e:
            if e in (AuthenticationExceptions.AccessNotFound, AuthenticationExceptions.AccessExpires):
                access_payload = await update_tokens(
                    response, refresh_bearer_token, refresh_cookies_token, redis_session
                )
                return access_payload


async def validate_user_credentials(
        session: get_session, credentials: UserSignInDTO = Body(...)
) -> UserSecureCredentialsDTO:
    user = await UserDAO(session).get_by_phone(credentials.phone)
    if user is None:
        raise AuthenticationExceptions.InvalidCredentials
    if not Hasher.verify_password(credentials.password, user.password):
        raise AuthenticationExceptions.InvalidCredentials
    return user


async def update_tokens(
        response: Response,
        refresh_bearer_token: refresh_bearer_depends,
        refresh_cookies_token: refresh_cookies_depends,
        redis_session: get_redis_session
) -> AccessTokenDTO:
    refresh_payload = await check_refresh(refresh_bearer_token, refresh_cookies_token, redis_session)
    access_payload = await create_tokens(response, refresh_payload.user_id, refresh_payload.role, redis_session)
    return access_payload


async def create_tokens(
        response: Response,
        user_id: UUID,
        role: RoleEnum,
        redis_session: get_redis_session
) -> AccessTokenDTO:
    await AuthenticationDAO(redis_session).pop_refresh_token(user_id=user_id)  # pop old token

    refresh_token = await AuthenticationDAO(redis_session).create_refresh_token(user_id, role)
    response.set_cookie(
        AUTH_CONFIG.refresh_key,
        refresh_token,
        AUTH_CONFIG.refresh_exp_sec,
        **AUTH_CONFIG.cookies_kwargs()
    )

    access_payload = AccessTokenDTO.access_fabric(user_id, role, AUTH_CONFIG.access_exp_sec)
    response.set_cookie(
        AUTH_CONFIG.access_key,
        JWT.encode(claims=access_payload.model_dump(mode='json')),
        AUTH_CONFIG.access_exp_sec,
        **AUTH_CONFIG.cookies_kwargs()
    )
    return access_payload


async def delete_tokens(
        request: Request,
        response: Response,
        redis_session: get_redis_session
):
    refresh_token = request.cookies.get(AUTH_CONFIG.refresh_key)
    if refresh_token is not None:
        await AuthenticationDAO(redis_session).pop_refresh_token(refresh_token=refresh_token)

    response.delete_cookie(AUTH_CONFIG.refresh_key)
    response.delete_cookie(AUTH_CONFIG.access_key)