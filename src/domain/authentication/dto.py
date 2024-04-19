from typing import Self, Annotated
from uuid import UUID

from src.domain.user.dto import RoleEnum
from src.domain.abc.dto import CustomSecretStr, AbstractDTO, PhoneStr
from src.utils.time import get_now_with_delta


class UserSignInDTO(AbstractDTO):
    phone: Annotated[str, PhoneStr]
    password: CustomSecretStr


class AccessTokenDTO(AbstractDTO):
    sub: UUID
    role: RoleEnum
    exp: int

    @classmethod
    def access_fabric(cls, id: UUID, role: RoleEnum, exp: int) -> Self:
        return cls(
            sub=id,
            exp=int(get_now_with_delta(seconds=exp).timestamp()),
            role=role
        )


class RefreshTokenDTO(AbstractDTO):
    user_id: UUID
    role: RoleEnum

    @classmethod
    def fabric(cls, refresh_token_key: str, role: str):
        return cls(
            user_id=refresh_token_key.split(',')[1],
            role=role
        )