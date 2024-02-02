from sqlalchemy.orm import Session

from app.book.crud import get_one_books_by_barcode
from app.book.models import Book
from app.store import schemas
from app.store.enum import OperationType
from app.store.models import Storing


def create_store_record(
    db: Session, book: Book, store: schemas.StoreCreation, operation_type: OperationType
) -> Storing:
    store = Storing(book=book, quantity=store.quantity, operation_type=operation_type)
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
