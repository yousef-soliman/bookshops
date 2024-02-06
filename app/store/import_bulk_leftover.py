import re
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, UploadFile, status
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

    def get_store_infos(self) -> list[schemas.StoreCreation]:
        handler_class = get_file_handler(self.file.filename or "")
        handler = handler_class(file=self.file)
        rows = handler.get_rows()
        res = []
        for row in rows:
            res.append(schemas.StoreCreation(barcode=row[0], quantity=int(row[1])))
        return res

    async def import_row(self, db: AsyncSession, store: schemas.StoreCreation):
        if store.barcode:
            operation_type = (
                OperationType.add if store.quantity > 0 else OperationType.remove
            )
            store = await crud.create_store(db, store, operation_type)

    async def import_data(self, db: AsyncSession):
        store_info = self.get_store_infos()
        for index, store in enumerate(store_info):
            try:
                await self.import_row(db, store)
            except:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"error in row {index+1}",
                )
