from typing import Annotated

import fastapi
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.postgres.connection import get_session_generator

get_session = Annotated[
    AsyncSession,
    fastapi.Depends(get_session_generator, use_cache=True),
]
