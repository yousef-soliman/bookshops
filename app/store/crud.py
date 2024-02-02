from datetime import date
from sqlalchemy.orm import Session

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
    storings = (
        db.query(Storing)
        .filter(Storing.book_id == book_id, Storing.date >= start, Storing.date <= end)
        .all()
    )
    history = [storing.__dict__ for storing in storings]
    return schemas.StoreHistory(book=book.__dict__, history=history)
