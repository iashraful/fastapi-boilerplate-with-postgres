from typing import List, Optional, Tuple, Type, Union

from sqlalchemy import select
from core.database import DBClient

from core.model_base import ModelBase
from core.config import settings
from .base_repo import AbstractRepository
import logging


logger = logging.getLogger(settings.PROJECT_NAME)


class BaseSQLAlchemyRepo(AbstractRepository):
    def __init__(self, model: Type[ModelBase], db: DBClient) -> None:
        super(BaseSQLAlchemyRepo, self).__init__()
        self._model = model
        self._session = db

    async def get(self, filters: Optional[Tuple] = ()) -> Union[dict, None]:
        statement = select(self._model).filter(*filters)
        result = await self._session.execute(statement)
        data = result.scalars().first()
        return data.__dict__ if data else None

    async def list(
        self, filters: Optional[Tuple] = (), limit: Optional[int] = None
    ) -> List[dict]:
        statement = select(self._model).filter(*filters)
        result = await self._session.execute(statement)
        data = result.scalars().fetchall()
        return [d.__dict__ for d in data]

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
