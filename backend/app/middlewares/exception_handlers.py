"""
Global exception handlers mapping AppException subclasses (and unhandled
exceptions) to a consistent JSON error envelope.
"""
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.exceptions import AppException
from app.core.logging_config import get_logger

logger = get_logger("exceptions")


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        logger.warning("app_exception", error_code=exc.error_code, message=exc.message, path=request.url.path)
        return JSONResponse(
            status_code=exc.status_code,
            content={"error_code": exc.error_code, "message": exc.message, "details": exc.details},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        # Pydantic v2 validators that raise a plain ValueError attach the
        # exception object itself into error["ctx"]["error"], which the stdlib
        # json encoder can't serialize by default. Sanitize ctx.error to a
        # string before encoding so validation failures never 500.
        raw_errors = exc.errors()
        for error in raw_errors:
            ctx = error.get("ctx")
            if isinstance(ctx, dict) and "error" in ctx and not isinstance(ctx["error"], (str, int, float, bool, type(None))):
                ctx["error"] = str(ctx["error"])
        safe_errors = jsonable_encoder(raw_errors)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"error_code": "VALIDATION_ERROR", "message": "Request validation failed", "details": safe_errors},
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.error("unhandled_exception", error=str(exc), path=request.url.path, exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error_code": "INTERNAL_SERVER_ERROR", "message": "An unexpected error occurred", "details": None},
        )
