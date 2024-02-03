from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import Date, cast, func

from app.book.crud import get_book_by_id, get_one_books_by_barcode
from app.book.models import Book
from app.book.schemas import Book as BookSchema
from app.store import schemas
from app.store.enum import OperationType
from app.store.models import Storing


def create_store_record(
    db: Session, book: Book, store: schemas.StoreCreation, operation_type: OperationType
) -> Storing:
    quantity = (
        store.quantity if operation_type == OperationType.add else -store.quantity
    )
    store = Storing(book=book, quantity=quantity, operation_type=operation_type)
    db.add(store)
    db.commit()
    db.refresh(store)
    return store


def create_store(
    db: Session, store: schemas.StoreCreation, operation_type: OperationType
) -> Storing:
    book = get_one_books_by_barcode(db, store.barcode)
    store = create_store_record(db, book, store, operation_type)
    return store


def get_history_for_book(
    db: Session, book_id: int, start: date, end: date
) -> schemas.StoreHistory:
    book = get_book_by_id(db, book_id)
    cast_date = cast(Storing.date, Date)
    storings = (
        db.query(Storing)
        .filter(Storing.book_id == book_id, cast_date >= start, cast_date <= end)
        .all()
    )
    start_balance = (
        db.query(func.sum(Storing.quantity))
        .filter(Storing.book_id == book_id, cast_date <= start)
        .scalar()
    )
    start_balance = start_balance or 0
    # import pdb

    # pdb.set_trace()
    end_balance = (
        db.query(func.sum(Storing.quantity))
        .filter(Storing.book_id == book_id, cast_date <= end)
        .scalar()
    )
    end_balance = end_balance or 0
    history = [storing.__dict__ for storing in storings]
    return schemas.StoreHistory(
        book=book.__dict__,
        history=history,
        start_balance=start_balance,
        end_balance=end_balance,
    )
