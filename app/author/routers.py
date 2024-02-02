from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from . import models, schemas

router = APIRouter(
    prefix="/authors",
    tags=["authors"],
)


@router.post("", response_model=schemas.Author)
async def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    author = models.Author(name=author.name, birth_date=author.birth_date)
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


@router.get("", response_model=list[schemas.Author])
async def get_all_authors(db: Session = Depends(get_db)):
    authors = db.query(models.Author).all()
    return authors


@router.get("/{author_id}", response_model=schemas.Author)
async def get_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    return author
