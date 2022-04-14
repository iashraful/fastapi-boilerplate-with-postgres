from sqlalchemy import Column, Integer, String, Boolean

from core.model_base import ModelBase


class User(ModelBase):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=False)
    email_verified = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
