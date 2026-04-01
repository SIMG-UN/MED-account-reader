from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .exceptions import NotFoundError
from .users.router import router as users_router
from .contacts.router import router as contacts_router
from .expenses.router import router as expenses_router
from .expense_splits.router import router as expense_splits_router
from .payments.router import router as payments_router
from .chats.router import router as chats_router
from .messages.router import router as messages_router

app = FastAPI(title="MED Account Reader", version="0.1.0")


@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": exc.detail})


app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(contacts_router, prefix="/contacts", tags=["contacts"])
app.include_router(expenses_router, prefix="/expenses", tags=["expenses"])
app.include_router(expense_splits_router, prefix="/expense-splits", tags=["expense_splits"])
app.include_router(payments_router, prefix="/payments", tags=["payments"])
app.include_router(chats_router, prefix="/chats", tags=["chats"])
app.include_router(messages_router, prefix="/messages", tags=["messages"])
