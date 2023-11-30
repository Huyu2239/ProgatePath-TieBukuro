from sqlalchemy import select
from sqlalchemy.schema import Column
from sqlalchemy.types import BigInteger
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from .constant import DB_URL


async_engine = create_async_engine(DB_URL)
async_session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
)
Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    user_id = Column(BigInteger, primary_key=True)
    total_time = Column(BigInteger)


async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def fetch_user(user_id):
    async with async_session() as session:
        result = await (session.execute(select(User).filter(User.user_id == user_id)))
        return result.scalar_one_or_none()


async def insert_user(user_id):
    async with async_session() as session:
        new_user = User(user_id=user_id, total_time=0)
        session.add(new_user)
        await session.flush()
        await session.commit()


async def update_user(_user):
    async with async_session() as session:
        result = await (session.execute(select(User).filter(User.user_id == _user.user_id)))
        user = result.first()
        user[0].total_time = _user.total_time
        session.add(user[0])
        await session.commit()
        await session.refresh(user[0])
