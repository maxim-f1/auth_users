from typing import Annotated

import fastapi

from src.domain.user.dto import UserGetDTO
from src.domain.user.service import user_create

user_create_depends = Annotated[
    UserGetDTO,
    fastapi.Depends(user_create)
]
