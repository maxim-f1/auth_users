from typing import Annotated

import fastapi

from src.database.redis.connection import RedisSession


get_redis_session = Annotated[
    RedisSession, fastapi.Depends(RedisSession)
]
