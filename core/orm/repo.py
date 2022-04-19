from typing import Optional, Tuple, Type

from sqlalchemy import select
from core.database import DBClient

from core.model_base import ModelBase
from .base_repo import AbstractRepository


class BaseSQLAlchemyRepo(AbstractRepository):
    def __init__(self, model: Type[ModelBase], db: DBClient) -> None:
        super(BaseSQLAlchemyRepo, self).__init__()
        self._model = model
        self._session = db

    async def get(self, filters: Optional[Tuple]) -> dict:
        try:
            statement = select(self._model).filter(*filters)
            result = await self._session.execute(statement)
            return result.scalars().first().__dict__
        except Exception as err:
            print(err)

    async def list(self, query: dict, limit: Optional[int] = None):
        raise NotImplementedError

    async def create(self, data: dict) -> dict:
        instance = self._model(**data)
        self._session.add(instance)
        await self._session.commit()
        await self._session.refresh(instance)
        return instance.__dict__

    async def update(self, query: dict, data: dict):
        raise NotImplementedError

    async def delete(self, query: dict):
        raise NotImplementedError
