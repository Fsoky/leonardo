from sqlalchemy import (
    Column,
    Integer,
    String,
    Text
)
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, unique=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    city = Column(String, nullable=False)
    sex = Column(Integer, nullable=False)
    look_for = Column(Integer, nullable=False)
    bio = Column(Text, nullable=False)
    photo = Column(String, nullable=False)