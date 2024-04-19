import enum
import datetime
from typing import Annotated
from uuid import UUID

from pydantic import SecretStr, Field

from src.domain.abc.dto import AbstractDTO, PhoneStr


class GenderEnum(str, enum.Enum):
    MALE = 'M'
    FEMALE = 'F'

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class RoleEnum(str, enum.Enum):
    CLIENT = 'CLIENT'

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

    def __lt__(self, other):
        return self.list().index(self) < self.list().index(other)

    def __le__(self, other):
        return self.list().index(self) <= self.list().index(other)

    def __gt__(self, other):
        return self.list().index(self) > self.list().index(other)

    def __ge__(self, other):
        return self.list().index(self) >= self.list().index(other)


class UserCreateDTO(AbstractDTO):
    phone: Annotated[str, PhoneStr]
    password: SecretStr
    role: RoleEnum


class UserGetDTO(AbstractDTO):
    id: UUID = Field(...)
    phone: str = Field(...)
    role: RoleEnum = Field(...)
    first_name: str | None = Field(None)
    surname: str | None = Field(None)
    patronymic: str | None = Field(None)
    gender: GenderEnum | None = Field(None)
    birthdate: datetime.date | None = Field(None)
    tg_id: int | None = Field(...)


class UserUpdateDTO(AbstractDTO):
    id: UUID = Field(...)
    first_name: str | None = Field(None)
    surname: str | None = Field(None)
    patronymic: str | None = Field(None)
    gender: GenderEnum | None = Field(None)
    birthdate: datetime.date | None = Field(None)


class UserSecureCredentialsDTO(AbstractDTO):
    id: UUID = Field(...)
    role: RoleEnum = Field(...)
    password: str = Field(...)
