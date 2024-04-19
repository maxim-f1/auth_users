import datetime
from uuid import uuid4

from sqlalchemy import String, UUID, func, ForeignKey, BigInteger, Date
from sqlalchemy.orm import Mapped, mapped_column

from src.database.postgres.abstract_model import AbstractModel


class RoleModel(AbstractModel):
    __tablename__ = 'role_table'

    name: Mapped[str] = mapped_column(String(8), primary_key=True)


class GenderModel(AbstractModel):
    __tablename__ = 'gender_table'

    name: Mapped[str] = mapped_column(String(1), primary_key=True)


class UserModel(AbstractModel):
    __tablename__ = 'user_table'

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, server_default=func.gen_random_uuid()
    )

    role: Mapped[str] = mapped_column(
        String(8), ForeignKey(RoleModel.name, ondelete='CASCADE'), nullable=False
    )
    gender: Mapped[str] = mapped_column(
        String(1), ForeignKey(GenderModel.name, ondelete='CASCADE'), nullable=True
    )

    password: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[str] = mapped_column(String(15), unique=True, nullable=False)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=True)

    first_name: Mapped[str] = mapped_column(String(32), nullable=True)
    surname: Mapped[str] = mapped_column(String(32), nullable=True)
    patronymic: Mapped[str] = mapped_column(String(32), nullable=True)
    birthdate: Mapped[datetime.date] = mapped_column(Date, nullable=True)
