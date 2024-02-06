from datetime import date
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.store.import_bulk_leftover import ImportBulkLeftOver
from . import models, schemas, crud
from app.store.enum import OperationType
from app.book.models import Book

router = APIRouter(
    prefix="/store",
    tags=["store"],
)


@router.post("/leftover/bulk")
async def bulk_leftover(
    file: UploadFile,
    db: Session = Depends(get_db),
):
    await ImportBulkLeftOver(file=file).import_data(db)
    return {"filename": file.filename}


@router.post(
    "/leftover/{operation_type}",
    response_model=schemas.Store,
    status_code=status.HTTP_201_CREATED,
)
async def update_store(
    operation_type: OperationType,
    store: schemas.StoreCreation,
    db: Session = Depends(get_db),
):
    store = await crud.create_store(db, store, operation_type)
    return store


@router.post("/history", response_model=schemas.StoreHistory)
async def get_history_for_book(
    book_id: int,
    start: date,
    end: date,
    db: Session = Depends(get_db),
):
    store = await crud.get_history_for_book(db, book_id, start, end)
    return store
