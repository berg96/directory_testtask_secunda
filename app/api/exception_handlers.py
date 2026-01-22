from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.domain.exceptions import NotFoundError


def setup_exception_handlers(app):
    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "detail": exc.message,
            },
        )
