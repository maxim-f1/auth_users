from sqlalchemy import func, TIMESTAMP
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class AbstractModel(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    created_at: Mapped[int] = mapped_column(TIMESTAMP, server_default=func.current_timestamp(), nullable=True)
    updated_at: Mapped[int] = mapped_column(TIMESTAMP, server_onupdate=func.current_timestamp(), nullable=True)
    deleted_at: Mapped[int] = mapped_column(TIMESTAMP, nullable=True)

    def __repr__(self):
        attrs = ', '.join(f"{key}={value}" for key, value in self.to_dict().items())
        return f'{self.__class__.__name__}({attrs})'

    def to_dict(self):
        result = {
            field.name: getattr(self, field.name)
            for field in self.__table__.c  # noqa
            if field.name not in ['created_at', 'updated_at', 'deleted_at']
        }
        return result
