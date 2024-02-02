from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from . import models, schemas
from app.store.enum import OperationType
from app.book.models import Book

router = APIRouter(
    prefix="/store",
    tags=["store"],
)


@router.get("/leftover/{operation_type}", response_model=schemas.Store)
async def update_store(
    operation_type: OperationType,
    store: schemas.StoreCreation,
    db: Session = Depends(get_db),
):
    book = db.query(Book).filter(Book.barcode == store.barcode).first()
    store = models.Storing(
        book=book, quantity=store.quantity, operation_type=operation_type
    )
    db.add(store)
    db.commit()
    db.refresh(store)
    return store
