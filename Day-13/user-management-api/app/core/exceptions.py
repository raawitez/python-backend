from fastapi import Request
from fastapi.responses import JSONResponse
from loguru import logger

async def global_exception_handler(request: Request, exc: Exception):
    logger.error(
        f"Unhandled exception on {request.method} {request.url.path} "
        f"- {type(exc).__name__}: {exc}"
    )

    return JSONResponse(
        status_code=500,
        content={
        "error_code": "SERVER_ERROR",
        "message": "An unexpected error occurred. Please try again.",
        "details": []
        }
    )