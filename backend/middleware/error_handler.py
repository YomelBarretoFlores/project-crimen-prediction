

import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

logger = logging.getLogger(__name__)


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:

    logger.error("Error no controlado en %s %s: %s",
                 request.method, request.url, exc, exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Error interno del servidor. Contacte al administrador.",
            "status_code": 500,
        },
    )


async def validation_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:

    logger.warning("Validación fallida en %s %s: %s",
                   request.method, request.url, exc.errors())
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Datos de entrada inválidos. Revise los rangos permitidos.",
            "errors": exc.errors(),
            "status_code": 422,
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(Exception, generic_exception_handler)
    app.add_exception_handler(ValidationError, validation_exception_handler)
