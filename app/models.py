from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from datetime import datetime

from app.enum import OperationType
from .db import Base


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)

    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    barcode = Column(String, nullable=False)
    publish_year = Column(Integer, nullable=False)

    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    author = relationship("Author", back_populates="books")

    stroning_infos = relationship("Storing", back_populates="book")


OperationTypeEnum = Enum(OperationType)


class Storing(Base):
    __tablename__ = "storing"

    id = Column(Integer, primary_key=True)
    operation_type = Column(
        OperationTypeEnum,
        default=OperationType.add,
        nullable=False,
    )
    quantity = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.now())

    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    book = relationship("Book", back_populates="stroning_infos")
