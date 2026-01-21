from typing import Generic, List, Optional, Type, TypeVar, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

T = TypeVar("T")

class CrudBase(Generic[T]):
    def __init__(self, model: Type[T], db: AsyncSession):
        self.model = model
        self.db = db

    async def create(self, **kwargs) -> T:
        instance = self.model(**kwargs)
        self.db.add(instance)
        await self.db.flush()
        await self.db.refresh(instance)
        return instance

    async def create_bulk(self, obj_list: list[dict], return_data=False) -> Optional[List[T]]:
        instances = [self.model(**data) for data in obj_list]
        self.db.add_all(instances)
        await self.db.flush()
        if return_data:
            for instance in instances:
                await self.db.refresh(instance)
            return instances
        return None

    async def read(self, *args, **kwargs) -> Optional[T]:
        stmt = select(self.model).filter(*args).filter_by(**kwargs)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def read_by(self, columns: List[Any], *args, **kwargs) -> Optional[T]:
        stmt = select(*columns).filter(*args).filter_by(**kwargs)
        result = await self.db.execute(stmt)
        return result.first()

    async def update(self, instance: T, **kwargs) -> T:
        for key, value in kwargs.items():
            setattr(instance, key, value)
        await self.db.flush()
        await self.db.refresh(instance)
        return instance

    async def delete(self, instance: T) -> None:
        await self.db.delete(instance)
        await self.db.flush()

    async def list_all(self) -> List[T]:
        stmt = select(self.model)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def list(self, skip: int = 0, limit: int = 10) -> List[T]:
        offset = skip * limit
        stmt = select(self.model).offset(offset).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def list_by(self, columns: List[Any], skip: int = 0, limit: int = 10) -> List[T]:
        offset = skip * limit
        stmt = select(*columns).offset(offset).limit(limit)
        result = await self.db.execute(stmt)
        return result.all()
