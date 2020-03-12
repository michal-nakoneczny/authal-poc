from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import RedirectResponse

from authal.error_handler import validation_exception_handler
from authal.views import service_view, status_view, user_view

app = FastAPI(title="Authal", description="Gengo AI User Management Service", version="0.0.1")


app.include_router(status_view.router)
app.include_router(user_view.router)
app.include_router(service_view.router)

app.add_exception_handler(RequestValidationError, validation_exception_handler)


@app.get("/")
async def root_view():
    return RedirectResponse(url="/docs", status_code=303)
