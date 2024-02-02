from sqlalchemy.orm import Session
from app.author.models import Author
from app.book import schemas
from app.book.models import Book


def get_all_books(db: Session) -> list[Book]:
    books = db.query(Book).all()
    return books


def get_one_books_by_barcode(db: Session, barcode: str) -> Book:
    book = db.query(Book).filter(Book.barcode == barcode).first()
    return book


def get_all_books_by_barcode(db: Session, barcode: str) -> list[Book]:
    books = db.query(Book).filter(Book.barcode == barcode).all()
    return books


def get_book_by_id(db: Session, book_id: int) -> Book:
    books = db.query(Book).filter(Book.id == book_id).first()
    return books


def create_book(db: Session, book: schemas.BookCreate) -> Book:
    author = db.query(Author).filter_by(id=book.author).first()
    book = Book(
        title=book.title,
        publish_year=book.publish_year,
        barcode=book.barcode,
        author=author,
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book
