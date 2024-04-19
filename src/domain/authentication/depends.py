from typing import Annotated

import fastapi

from src.domain.authentication.service import validate_user_credentials, delete_tokens, update_tokens
from src.domain.user.dto import UserSecureCredentialsDTO

validate_user_credentials_depends = Annotated[
    UserSecureCredentialsDTO, fastapi.Depends(validate_user_credentials)
]

delete_tokens_depends = Annotated[
    None, fastapi.Depends(delete_tokens)
]

update_tokens_depends = Annotated[
    None, fastapi.Depends(update_tokens)
]