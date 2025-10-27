from typing import TypeVar, Type
from sqlalchemy.ext.asyncio import AsyncSession
from core.db import Base


model_type = TypeVar("model_type", bound=Base)


class BaseRepository:
    model: Type[model_type]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, object_id: int) -> model_type | None:
        return await self.session.get(self.model, object_id)

    async def delete(self, instance: model_type):
        await self.session.delete(instance)
        await self.session.commit()

    async def update(self, instance: model_type, **attrs: dict) -> model_type:
        for key, value in attrs:
            setattr(instance, key, value)

        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def create(self, **attrs: dict) -> model_type:
        instance = self.model(**attrs)

        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance