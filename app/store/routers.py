from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.store.crud import create_store
from . import models, schemas
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
    store = create_store(db, store, operation_type)
    return store
