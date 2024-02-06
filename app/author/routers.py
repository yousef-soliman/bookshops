from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.db import get_db
from . import models, schemas, crud

router = APIRouter(
    prefix="/authors",
    tags=["authors"],
)


@router.post("", response_model=schemas.Author, status_code=status.HTTP_201_CREATED)
async def create_author(
    author: schemas.AuthorCreate, db: AsyncSession = Depends(get_db)
):
    try:
        author = await crud.create_author(db, author)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="can not create author",
        )
    return author


@router.get("", response_model=list[schemas.Author])
async def get_all_authors(db: AsyncSession = Depends(get_db)):
    authors = await crud.get_all_authors(db)
    return authors


@router.get("/{author_id}", response_model=schemas.Author)
async def get_author(author_id: int, db: AsyncSession = Depends(get_db)):
    author = await crud.get_author_by_id(db, author_id)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found",
        )
    return author
