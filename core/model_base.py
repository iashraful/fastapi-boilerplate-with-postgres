import typing as t

from sqlalchemy.ext.declarative import as_declarative, declared_attr


class_registry: t.Dict = {}


@as_declarative(class_registry=class_registry)
class ModelBase:
    id: t.Any
    __name__: str

    @classmethod
    def get_table_name(cls, make_plural=True):
        return f"{cls.__name__.lower()}s"

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.get_table_name()
