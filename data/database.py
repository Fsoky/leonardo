from sqlalchemy import select, update, ScalarResult
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncAttrs, AsyncEngine
from sqlalchemy.exc import NoResultFound

from .models import Base, Users


class DataBase:

    def __init__(self):
        self.engine: AsyncEngine = create_async_engine("sqlite+aiosqlite:///users.db")
        self.async_session: AsyncSession = async_sessionmaker(
            self.engine,
            expire_on_commit=False
        )

    async def create(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def insert(self, **kwargs) -> None:
        async with self.async_session.begin() as session:
            session.add(Users(**kwargs))

    async def user_update(self, user_id: int, **kwargs) -> None:
        stmt = (
            update(Users).
            where(Users.user_id == user_id).
            values(**kwargs)
        )
        
        async with self.async_session.begin() as session:
            await session.execute(stmt)

    async def get(self, user_id: int | None=None, all_data: bool=False) -> ScalarResult | None:
        stmt = (
            select(Users).
            where(Users.user_id == user_id)
        ) if user_id is not None else select(Users)

        try:
            async with self.async_session.begin() as session:
                data = await session.execute(stmt)
                return data.scalars().one() if not all_data else data.scalars().all()
        except NoResultFound:
            return None