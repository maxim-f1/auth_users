from fastapi import APIRouter
from starlette import status
from starlette.responses import Response

from src.database.redis.depends import get_redis_session
from src.domain.authentication.depends import validate_user_credentials_depends, delete_tokens_depends, \
    update_tokens_depends
from src.domain.authentication.service import create_tokens
from src.domain.user.depends import user_create_depends

auth_rest_v1 = APIRouter(
    tags=["Authentications"],
)


@auth_rest_v1.post(
    path='/sign-up/',
    status_code=status.HTTP_204_NO_CONTENT
)
async def sign_up(
        response: Response,
        user: user_create_depends,
        redis_session: get_redis_session
):
    await create_tokens(response, user.id, user.role, redis_session)


@auth_rest_v1.post(
    path='/sign-in/',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def sign_in(
        response: Response,
        user: validate_user_credentials_depends,
        redis_session: get_redis_session
):
    await create_tokens(response, user.id, user.role, redis_session)


@auth_rest_v1.delete(
    path='/sign-out/',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def sign_out(tokens: delete_tokens_depends):
    pass


@auth_rest_v1.get(
    path='/refresh/',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def refresh_tokens(tokens: update_tokens_depends):
    pass
