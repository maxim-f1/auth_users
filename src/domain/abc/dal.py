from typing import TypeVar, Generic, Type, Dict, Any, List
from uuid import UUID

from sqlalchemy import update, delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.postgres.abstract_model import AbstractModel
from src.domain.abc.dto import AbstractDTO
from src.utils.time import get_now_with_delta


ModelType = TypeVar('ModelType', bound=AbstractModel)
GetSchemeType = TypeVar('GetSchemeType', bound=AbstractDTO)
CreateSchemeType = TypeVar('CreateSchemeType', bound=AbstractDTO)
UpdateSchemeType = TypeVar('UpdateSchemeType', bound=AbstractDTO)

ID = UUID | int | str


class AbstractDAO(Generic[ModelType, GetSchemeType, CreateSchemeType, UpdateSchemeType]):
    model: Type[ModelType] = AbstractModel
    get_scheme: Type[GetSchemeType] = GetSchemeType
    create_scheme: Type[CreateSchemeType] = CreateSchemeType
    update_scheme: Type[UpdateSchemeType] = UpdateSchemeType

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: CreateSchemeType, **kwargs: Any) -> GetSchemeType:
        query = insert(self.model).returning(self.model).values(**data.model_dump(exclude_none=True), **kwargs)
        result = await self.session.scalar(query)
        new_instance = self.get_scheme.model_validate(result)
        return new_instance

    async def update(self, data: UpdateSchemeType, **kwargs: Dict[str, Any]):
        query = update(
            self.model
        ).where(
            self.model.id == data.id  # noqa
        ).values(
            **data.model_dump(exclude_none=True, exclude={'id'}), **kwargs
        )
        await self.session.execute(query)

    async def create_list(self, data: List[Dict[str, Any]], with_returning: bool = True) -> List[GetSchemeType] | None:
        if len(data) < 1:
            return []
        if not with_returning:
            await self.session.execute(insert(self.model), data)
            return []

        query = insert(self.model).returning(self.model, sort_by_parameter_order=True)
        result = await self.session.scalars(query, data)
        return [self.get_scheme.model_validate(instance) for instance in result]

    async def update_list(self, data: List[Dict[str, Any]]):
        if len(data) < 1:
            return None
        await self.session.execute(update(self.model), data)

    async def delete_list(self, ids: List[ID]):
        if len(ids) < 1:
            return None
        await self.session.execute(delete(self.model).where(self.model.id.in_(ids)))

    async def deactivate(self, instance_id: ID):
        query = update(
            self.model
        ).where(
            self.model.id == instance_id
        ).values(
            {'deleted_at': get_now_with_delta(is_date=True).timestamp()}
        )

        await self.session.execute(query)

    async def get_list(self) -> List[GetSchemeType]:
        result = await self.session.scalars(select(self.model))
        return [self.get_scheme.model_validate(item) for item in result]

    async def get_dto_by_id(self, instance_id: ID) -> GetSchemeType | None:
        result = await self.session.get(self.model, instance_id)
        if result is not None:
            return self.get_scheme.model_validate(result)

    async def get_model_by_id(self, instance_id: ID) -> ModelType | None:
        query = select(
            self.model
        ).where(
            self.model.id == instance_id
        ).limit(1)
        return (await self.session.execute(query)).scalar_one_or_none()