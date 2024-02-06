import re
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, UploadFile, status
from app.book.crud import get_all_books_in_barcode_list
from app.store import crud, schemas
import pandas as pd

from app.store.enum import OperationType


class FileHandler:
    file_ext: str | None = None

    def __init__(self, file: UploadFile) -> None:
        self.file = file

    def get_rows(self) -> list:
        raise NotImplemented("NotImplemented")


class XlxsFileHandler(FileHandler):
    file_ext = "xlsx"

    def get_rows(self) -> list:
        df = pd.read_excel(self.file.file, sheet_name=None, header=None, dtype=str)
        sheet1 = list(df.keys())[0]
        result = []
        for index, record in df[sheet1].iterrows():
            result.append(record)
        return result


class TextFileHandler(FileHandler):
    file_ext = "text"

    def extract_pattern(self, line: str):
        match = re.match(r"([A-Za-z]+)(-?\d+)", line)

        if match:
            return match.groups()
        else:
            return None

    def get_rows(self) -> list:
        lines = self.file.file.readlines()
        result = [self.extract_pattern(line.decode()) for line in lines]
        return result


def get_file_handler(filename: str):
    if filename.endswith(".xlsx"):
        return XlxsFileHandler
    if filename.endswith(".txt"):
        return TextFileHandler
    return FileHandler


class ImportBulkLeftOver:
    def __init__(self, file: UploadFile) -> None:
        self.file = file

    async def get_books_by_barcode(
        self, db: AsyncSession, barcodes: list[str]
    ) -> dict[str, int]:
        books = await get_all_books_in_barcode_list(db, barcodes)
        return {str(book.barcode): int(book.id) for book in books}

    async def get_store_infos(
        self, db: AsyncSession
    ) -> list[schemas.StoreCreationNative]:
        handler_class = get_file_handler(self.file.filename or "")
        handler = handler_class(file=self.file)
        rows = handler.get_rows()
        res = []
        barcodes = [row[0] for row in rows]
        books_by_barcode = await self.get_books_by_barcode(db, barcodes)
        for row in rows:
            barcode = row[0]
            quantity = int(row[1])
            book_id = books_by_barcode.get(barcode)
            operation_type = OperationType.add if quantity > 0 else OperationType.remove
            if not book_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"book not found",
                )
            res.append(
                schemas.StoreCreationNative(
                    quantity=quantity, book_id=book_id, operation_type=operation_type
                )
            )
        return res

    async def import_row(self, db: AsyncSession, store: schemas.StoreCreationNative):
        await crud.create_store_native(db, store)

    async def import_data(self, db: AsyncSession):
        store_info = await self.get_store_infos(db)
        for index, store in enumerate(store_info):
            try:
                await self.import_row(db, store)
            except:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"error in row {index+1}",
                )
