from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from . import models, schemas, crud
from app.store.enum import OperationType
from app.book.models import Book

router = APIRouter(
    prefix="/store",
    tags=["store"],
)


@router.post("/leftover/{operation_type}", response_model=schemas.Store)
async def update_store(
    operation_type: OperationType,
    store: schemas.StoreCreation,
    db: Session = Depends(get_db),
):
    store = crud.create_store(db, store, operation_type)
    return store


@router.post("/history", response_model=schemas.StoreHistory)
async def get_history_for_book(
    book_id: int,
    start: date,
    end: date,
    db: Session = Depends(get_db),
):
    store = crud.get_history_for_book(db, book_id, start, end)
    return store
