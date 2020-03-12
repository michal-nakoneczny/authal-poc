from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


# DEMO: this shows how to add custom error handler to modify default behaviour
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        # by default FastAPI responds with 422 on request validation errors, we want good ol' 400
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(
            {
                "detail": exc.errors(),
                # DEMO: transform errors
                "demo_errors": [
                    {".".join(error["loc"]): {error["msg"]}} for error in exc.errors()
                ],
            }
        ),
    )
