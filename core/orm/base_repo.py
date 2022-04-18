import abc
from typing import Optional


class AbstractRepository(abc.ABC):
    """
    It's time to make good on our promise to use the dependency inversion principle as a
    way of decoupling our core logic from infrastructural concerns.

    We'll introduce the Repository pattern, a simplifying abstraction over data storage,
    allowing us to decouple our model layer from the data layer. We'll present a concrete
    example of how this simplifying abstraction makes our system more testable by hiding
    the complexities of the database.
    Source: https://www.cosmicpython.com/book/chapter_02_repository.html
    """

    @abc.abstractmethod
    def get(self, query: dict):
        pass

    @abc.abstractmethod
    def list(self, query: dict, limit: Optional[int] = None):
        pass

    @abc.abstractmethod
    def create(self, data: dict):
        pass

    @abc.abstractmethod
    def update(self, query: dict, data: dict):
        pass

    @abc.abstractmethod
    def delete(self, query: dict):
        pass
