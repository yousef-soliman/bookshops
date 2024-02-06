from app.author.crud import get_author_by_id
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import select
from app.author.models import Author
from app.book import schemas
from app.book.models import Book


async def get_all_books(db: AsyncSession) -> list[Book]:
    statement = select(Book)
    books = await db.execute(statement)
    return books.scalars()


async def get_one_books_by_barcode(db: AsyncSession, barcode: str) -> Book:
    statement = select(Book).where(Book.barcode == barcode)
    book = await db.execute(statement)
    return book.scalars().first()


async def get_all_books_by_barcode(db: AsyncSession, barcode: str) -> list[Book]:
    statement = select(Book).where(Book.barcode == barcode)
    books = await db.execute(statement)
    return books.scalars()


async def get_all_books_in_barcode_list(
    db: AsyncSession, barcodes: list[str]
) -> list[Book]:
    statement = select(Book).where(Book.barcode.in_(barcodes))
    books = await db.execute(statement)
    return books.scalars()


async def get_book_by_id(db: AsyncSession, book_id: int) -> Book:
    statement = select(Book).where(Book.id == book_id)
    book = await db.execute(statement)
    return book.scalars().first()


async def create_book(db: AsyncSession, book: schemas.BookCreate) -> Book:
    author = await get_author_by_id(db, book.author)
    book = Book(
        title=book.title,
        publish_year=book.publish_year,
        barcode=book.barcode,
        author=author,
    )
    db.add(book)
    await db.commit()
    await db.refresh(book)
    return book
