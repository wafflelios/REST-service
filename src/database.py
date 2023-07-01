from typing import AsyncGenerator

from sqlalchemy import Column, Integer, String, Date, NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeMeta, declarative_base, sessionmaker

from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
Base: DeclarativeMeta = declarative_base()

engine = create_async_engine(DATABASE_URL, poolclass=NullPool)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# Строение таблицы пользователей
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    login = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, unique=True, nullable=False)
    salary = Column(Integer, nullable=False)
    date_of_next_increase = Column(Date, default=None)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
