from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import select
from app.author import schemas
from app.author.models import Author


async def get_all_authors(db: AsyncSession) -> list[Author]:
    statement = select(Author)
    authors = await db.execute(statement)
    return authors.scalars()


async def get_author_by_id(db: AsyncSession, author_id: int) -> Author:
    statement = select(Author).where(Author.id == author_id)
    author = await db.execute(statement)
    return author.scalars().first()


async def create_author(db: AsyncSession, author: schemas.AuthorCreate) -> Author:
    author = Author(name=author.name, birth_date=author.birth_date)
    db.add(author)
    await db.commit()
    await db.refresh(author)
    return author
