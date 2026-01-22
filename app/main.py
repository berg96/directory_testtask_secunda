from fastapi import FastAPI

from .api.exception_handlers import setup_exception_handlers
from .api.router import main_router
from .config.settings import settings

app = FastAPI(title=settings.APP_TITLE, description=settings.APP_DESCRIPTION)

app.include_router(main_router)
setup_exception_handlers(app)
