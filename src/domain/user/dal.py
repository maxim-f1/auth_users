from typing import Iterable
from uuid import UUID

from sqlalchemy import select

from src.domain.abc.dal import AbstractDAO
from src.domain.user.dto import UserGetDTO, UserCreateDTO, UserUpdateDTO, UserSecureCredentialsDTO, RoleEnum
from src.domain.user.model import UserModel


class UserDAO(
    AbstractDAO[
        UserModel,
        UserGetDTO,
        UserCreateDTO,
        UserUpdateDTO
    ]
):
    model = UserModel
    get_scheme = UserGetDTO
    create_scheme = UserCreateDTO
    update_scheme = UserUpdateDTO

    async def get_by_phone(self, phone: str) -> UserSecureCredentialsDTO | None:
        query = select(
            self.model
        ).where(
            self.model.phone == phone
        )
        result = await self.session.scalar(query)
        if result is None:
            return None

        return UserSecureCredentialsDTO.model_validate(result)

    async def get_by_tg_id(self, telegram_id: int) -> model | None:
        query = select(
            self.model
        ).where(
            self.model.tg_id == telegram_id
        )

        return await self.session.scalar(query)

    async def get_by_role(self, role: RoleEnum) -> Iterable[model]:
        query = select(
            self.model
        ).where(
            self.model.role == role
        )

        return await self.session.scalars(query)

    async def check_role(self, user_id: UUID, role: RoleEnum):
        query = select(
            self.model.role
        ).where(
            self.model.id == user_id,
            self.model.role == role
        )
        user = (await self.session.execute(query)).one_or_none()
        return user is not None
