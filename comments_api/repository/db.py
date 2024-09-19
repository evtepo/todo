from abc import ABC, abstractmethod
from typing import TypeVar

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.comment import Comment


Model = TypeVar("Model", Comment, ...)


class BaseRepository(ABC):
    @abstractmethod
    async def get(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def create(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def update(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, *args, **kwargs):
        raise NotImplementedError


class PostgresRepository(BaseRepository):
    async def get(self, limit: int, offset: int, session: AsyncSession, model: Model, **filters):
        query = select(model).filter_by(**filters).limit(limit).offset(offset)
        res = await session.execute(query)

        return res.scalars().all()

    async def create(self, session: AsyncSession, model: Model, data: dict):
        instance = model(**data)
        session.add(instance)
        await session.commit()
        await session.refresh(instance)

        return instance

    async def update(self, session: AsyncSession, model: Model, data: dict, **filters):
        query = update(model).values(**data).filter_by(**filters)
        await session.execute(query)
        await session.commit()

        updated_instance = await session.get_one(model, data.get("id"))

        return updated_instance


    async def delete(self, session: AsyncSession, model: Model, **filters):
        query = delete(model).filter_by(**filters)
        await session.execute(query)
        await session.commit()


repository: BaseRepository | None = PostgresRepository()


async def get_repository():
    return repository
