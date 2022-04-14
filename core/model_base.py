from typing import Dict, Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr


class_registry: Dict = {}


@as_declarative(class_registry=class_registry)
class ModelBase:
    id: Any
    __name__: str

    @classmethod
    def get_table_name(cls, make_plural: bool = True):
        _name = f"{cls.__name__.lower()}"
        if make_plural:
            return f"{_name}s"
        return _name

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.get_table_name()
