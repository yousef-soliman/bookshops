from sqlalchemy import (
    Column,
    Date,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.database.db import Base


class Author(Base):
    __tablename__ = "authors"
    __table_args__ = (UniqueConstraint("name", "birth_date"),)
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)

    books = relationship("Book", back_populates="author")
