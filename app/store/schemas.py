from pydantic import BaseModel
from datetime import datetime
from app.book.schemas import Book, BookBase

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


class History(BaseModel):
    quantity: int
    date: datetime

    class Config:
        orm_mode = True


class StoreHistory(BaseModel):
    book: BookBase
    history: list[History]
    start_balance: int
    end_balance: int


class StoreCreationNative(BaseModel):
    book_id: int
    quantity: int
    operation_type: OperationType
