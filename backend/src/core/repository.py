from typing import TypeVar, Type, Generic
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from core.db import Base


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

    async def update(self, instance: model_type, schema: update_schema_type) -> model_type:
        data = schema.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(instance, key, value)

        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def create(self, schema: create_schema_type) -> model_type:
        instance = self.model(**schema.model_dump())
        self.session.add(instance)

        try:
            await self.session.commit()
            await self.session.refresh(instance)
            return instance
        except Exception:
            await self.session.rollback()
            raise