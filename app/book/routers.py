from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.db import get_db
from . import models, schemas, crud
from app.author.models import Author

router = APIRouter(
    prefix="/books",
    tags=["book"],
)


@router.post("/", response_model=schemas.Book, status_code=status.HTTP_201_CREATED)
async def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    try:
        book = crud.create_book(db, book)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="can not create book",
        )
    return book


@router.get("/", response_model=list[schemas.Book])
async def get_all_books(barcode: str | None = None, db: Session = Depends(get_db)):
    if barcode:
        books = crud.get_all_books_by_barcode(db, barcode)
    else:
        books = crud.get_all_books(db)
    return books


@router.get("/{book_id}", response_model=schemas.Book)
async def get_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )
    return book
