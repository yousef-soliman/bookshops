from sqlalchemy.orm import Session
from app.author import schemas
from app.author.models import Author


def get_all_authors(db: Session) -> list[Author]:
    authors = db.query(Author).all()
    return authors


def get_author_by_id(db: Session, author_id: int) -> Author:
    author = db.query(Author).filter(Author.id == author_id).first()
    return author


def create_author(db: Session, author: schemas.AuthorCreate) -> Author:
    author = Author(name=author.name, birth_date=author.birth_date)
    db.add(author)
    db.commit()
    db.refresh(author)
    return author
