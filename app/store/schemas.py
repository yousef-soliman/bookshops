from pydantic import BaseModel
from datetime import datetime
from app.book.schemas import Book

from app.store.enum import OperationType


class StoreCreation(BaseModel):
    barcode: str
    quantity: int


class Store(BaseModel):
    book: Book
    quantity: int
    date: datetime
    operation_type: OperationType

    class Config:
        orm_mode = True
