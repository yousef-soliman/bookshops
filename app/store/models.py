from sqlalchemy import Column, DateTime, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime

from app.store.enum import OperationType
from app.database.db import Base


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
