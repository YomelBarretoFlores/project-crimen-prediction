

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes import health, predict, historical
from backend.core.config import get_settings
from backend.middleware.error_handler import register_exception_handlers


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(name)-30s │ %(levelname)-8s │ %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    
    settings = get_settings()

    application = FastAPI(
        title=settings.APP_TITLE,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
    )

 
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

 
    register_exception_handlers(application)


    application.include_router(health.router)
    application.include_router(predict.router)
    application.include_router(historical.router)

    logger.info("🚀 %s v%s inicializado.", settings.APP_TITLE, settings.APP_VERSION)

    return application


app = create_app()
