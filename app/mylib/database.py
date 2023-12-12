from sqlalchemy import select, update
from sqlalchemy import desc
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


class UserBase(Base):
    __tablename__ = "user"
    user_id = Column(BigInteger, primary_key=True)
    monthly_time = Column(BigInteger)
    total_time = Column(BigInteger)

class User:
    def __init__(self, user_base: UserBase):
        self.user_id = user_base.user_id
        self.monthly_time = user_base.monthly_time
        self.total_time = user_base.total_time


async def init_db():
    async with async_engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def fetch_user(user_id):
    async with async_session() as session:
        result = await (session.execute(select(UserBase).filter(UserBase.user_id == user_id)))
        user_base = result.scalar_one_or_none()
        if user_base is None:
            return None
        return User(user_base)


async def fetch_monthly_top_users():
    async with async_session() as session:
        query = select(UserBase).order_by(desc(UserBase.monthly_time)).limit(10)
        result = await session.execute(query)
        top_user_base = result.scalars().all()
        top_users = [User(user_base) for user_base in top_user_base]
        return top_users


async def fetch_total_top_users():
    async with async_session() as session:
        query = select(UserBase).order_by(desc(UserBase.total_time)).limit(10)
        result = await session.execute(query)
        top_user_base = result.scalars().all()
        top_users = [User(user_base) for user_base in top_user_base]
        return top_users


async def insert_user(user_id):
    async with async_session() as session:
        new_user = UserBase(user_id=user_id, monthly_time=0, total_time=0)
        session.add(new_user)
        await session.flush()
        await session.commit()


async def update_user(_user: User):
    async with async_session() as session:
        result = await (session.execute(select(UserBase).filter(UserBase.user_id == _user.user_id)))
        user = result.first()
        user[0].monthly_time = _user.monthly_time
        user[0].total_time = _user.total_time
        session.add(user[0])
        await session.commit()
        await session.refresh(user[0])


async def reset_monthly_time():
    async with async_session() as session:
        # Userテーブルのmonthly_timeを0に更新
        query = update(UserBase).values(monthly_time=0)
        await session.execute(query)
        await session.commit()
