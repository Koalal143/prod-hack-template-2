from typing import TypeVar, Type, Generic
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from src.core.db.engine import Base


model_type = TypeVar("model_type", bound=Base)
create_schema_type = TypeVar("create_schema_type", bound=BaseModel)
update_schema_type = TypeVar("update_schema_type", bound=BaseModel)


class BaseRepository(Generic[model_type]):
    model: Type[model_type]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, object_id: int) -> model_type | None:
        return await self.session.get(self.model, object_id)

    async def delete(self, instance: model_type):
        await self.session.delete(instance)
        await self.session.commit()

    async def update(
        self, instance: model_type, data: update_schema_type | dict
    ) -> model_type:
        if isinstance(data, BaseModel):
            data = data.model_dump(exclude_unset=True)

        for key, value in data.items():
            setattr(instance, key, value)

        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def create(self, data: create_schema_type | dict) -> model_type:
        if isinstance(data, BaseModel):
            instance = self.model(**data.model_dump())
        else:
            instance = self.model(**data)

        self.session.add(instance)

        try:
            await self.session.commit()
            await self.session.refresh(instance)
            return instance
        except Exception:
            await self.session.rollback()
            raise
