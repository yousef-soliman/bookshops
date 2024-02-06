import asyncio
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.author.models import Author
from app.book.models import Book
from app.store.models import Storing

from app.database.db import Base


SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///test.db"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


asyncio.run(init_models())


TestingSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
