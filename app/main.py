from fastapi import FastAPI, Request
from starlette.responses import JSONResponse


from app.author.routers import router as author_router
from app.book.routers import router as book_router
from app.store.routers import router as store_router

app = FastAPI(debug=True)
app.include_router(author_router)
app.include_router(book_router)
app.include_router(store_router)


@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )
