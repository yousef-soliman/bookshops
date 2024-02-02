from sqlalchemy import (
    Column,
    Date,
    Integer,
    String,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.database.db import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    barcode = Column(String, nullable=False)
    publish_year = Column(Integer, nullable=False)

    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    author = relationship("Author", back_populates="books")

    stroning_infos = relationship("Storing", back_populates="book")
