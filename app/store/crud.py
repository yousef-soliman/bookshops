from datetime import date
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import Date, cast, func, select

from app.book.crud import get_book_by_id, get_one_books_by_barcode
from app.book.models import Book
from app.book.schemas import Book as BookSchema
from app.store import schemas
from app.store.enum import OperationType
from app.store.models import Storing


async def create_store_record(
    db: AsyncSession,
    book: Book,
    store: schemas.StoreCreation,
    operation_type: OperationType,
) -> Storing:
    quantity = (
        store.quantity if operation_type == OperationType.add else -store.quantity
    )
    store = Storing(book=book, quantity=quantity, operation_type=operation_type)
    db.add(store)
    await db.commit()
    await db.refresh(store)
    return store


async def create_store(
    db: AsyncSession, store: schemas.StoreCreation, operation_type: OperationType
) -> Storing:
    book = await get_one_books_by_barcode(db, store.barcode)
    store = await create_store_record(db, book, store, operation_type)
    return store


async def create_store_native(
    db: AsyncSession, store: schemas.StoreCreationNative
) -> Storing:
    store = Storing(
        book_id=store.book_id,
        quantity=store.quantity,
        operation_type=store.operation_type,
    )
    db.add(store)
    await db.commit()
    await db.refresh(store)

    return store


async def get_history_for_book(
    db: AsyncSession, book_id: int, start: date, end: date
) -> schemas.StoreHistory:
    book = await get_book_by_id(db, book_id)
    cast_date = cast(Storing.date, Date)
    statement = select(Storing).where(
        Storing.book_id == book_id, cast_date >= start, cast_date <= end
    )
    storings = await db.execute(statement)
    storings = storings.scalars()

    statement = select(func.sum(Storing.quantity)).where(
        Storing.book_id == book_id, cast_date <= start
    )
    start_balance = await db.execute(statement)
    start_balance = start_balance.scalar()
    start_balance = start_balance or 0

    statement = select(func.sum(Storing.quantity)).where(
        Storing.book_id == book_id, cast_date <= end
    )
    end_balance = await db.execute(statement)
    end_balance = end_balance.scalar()
    end_balance = end_balance or 0

    history = [storing.__dict__ for storing in storings]
    return schemas.StoreHistory(
        book=book.__dict__,
        history=history,
        start_balance=start_balance,
        end_balance=end_balance,
    )
