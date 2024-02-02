from pydantic import BaseModel
from app.author.schemas import Author


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
