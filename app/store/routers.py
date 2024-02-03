from datetime import date
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from sqlalchemy.orm import Session
import pandas as pd

from app.database.db import get_db
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
    df = pd.read_excel(file.file, sheet_name=None, header=None)
    sheet1 = list(df.keys())[0]
    for index, record in df[sheet1].iterrows():
        import pdb

        pdb.set_trace()
        try:
            if str(record[0]):
                store = schemas.StoreCreation(
                    barcode=str(record[0]), quantity=abs(int(record[1]))
                )
                operation_type = (
                    OperationType.add if record[1] > 0 else OperationType.remove
                )
                store = crud.create_store(db, store, operation_type)
        except:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"error in row {index}"
            )
    return {"filename": file.filename}


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
