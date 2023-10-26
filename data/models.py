from sqlalchemy import BigInteger, Text
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    name: Mapped[str] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    city: Mapped[str] = mapped_column(nullable=False)
    sex: Mapped[int] =  mapped_column(nullable=False)
    look_for: Mapped[str] = mapped_column(nullable=False)
    bio: Mapped[str] = mapped_column(Text, nullable=False)
    photo: Mapped[str] = mapped_column(Text, nullable=False)