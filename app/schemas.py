from pydantic import BaseModel
from datetime import date, datetime

from app.enum import OperationType


class AuthorBase(BaseModel):
    name: str
    birth_date: date


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: str
    publish_year: int
    barcode: str


class BookCreate(BookBase):
    author: int
    pass


class Book(BookBase):
    id: int
    author: Author

    class Config:
        orm_mode = True


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
