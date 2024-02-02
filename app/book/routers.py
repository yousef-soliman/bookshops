from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from . import models, schemas
from app.author.models import Author

router = APIRouter(
    prefix="/books",
    tags=["book"],
)


@router.post("/", response_model=schemas.Book)
async def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    author = db.query(Author).filter_by(id=book.author).first()
    book = models.Book(
        title=book.title,
        publish_year=book.publish_year,
        barcode=book.barcode,
        author=author,
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@router.get("/", response_model=list[schemas.Book])
async def get_all_books(barcode: str | None = None, db: Session = Depends(get_db)):
    book_model = db.query(models.Book)
    book_qury = book_model
    if barcode:
        book_qury = book_qury.filter(models.Book.barcode == barcode)
    books = book_qury.all()
    return books


@router.get("/{book_id}", response_model=schemas.Book)
async def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    return book
