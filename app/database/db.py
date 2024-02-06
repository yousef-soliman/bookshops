from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://username:password@db/bookshop"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()


# Dependency
async def get_db() -> AsyncSession:
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        autocommit=False,
        autoflush=False,
    )
    async with async_session() as session:
        yield session
