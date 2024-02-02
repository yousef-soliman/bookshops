from typing import Union

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from starlette.routing import request_response

from app.db import get_db, init_db
from . import models, schemas

# init_db()

app = FastAPI(debug=True)


@app.post("/authors", response_model=schemas.Author)
async def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    author = models.Author(name=author.name, birth_date=author.birth_date)
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


@app.get("/authors", response_model=list[schemas.Author])
async def get_all_authors(db: Session = Depends(get_db)):
    authors = db.query(models.Author).all()
    return authors


@app.get("/authors/{author_id}", response_model=schemas.Author)
async def get_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    return author


@app.post("/books", response_model=schemas.Book)
async def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    author = db.query(models.Author).filter_by(id=book.author).first()
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


@app.get("/books", response_model=list[schemas.Book])
async def get_all_books(db: Session = Depends(get_db)):
    books = db.query(models.Book).all()
    return books


@app.get("/books/{book_id}", response_model=schemas.Book)
async def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    return book
