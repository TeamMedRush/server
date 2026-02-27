from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import get_settings
from app.middleware.cors import setup_cors
from app.routers import health


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # startup
    yield
    # shutdown


def create_app() -> FastAPI:
    settings = get_settings()

    application = FastAPI(
        title=settings.APP_NAME,
        version='0.1.0',
        description='MedRush backend API',
        lifespan=lifespan,
        docs_url='/docs',
        redoc_url='/redoc',
    )

    setup_cors(application)

    application.include_router(health.router, prefix=settings.API_PREFIX)

    return application


app = create_app()
