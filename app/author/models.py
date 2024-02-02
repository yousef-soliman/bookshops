from sqlalchemy import (
    Column,
    Date,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.database.db import Base


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)

    books = relationship("Book", back_populates="author")
