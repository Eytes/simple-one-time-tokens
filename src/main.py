import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from dependencies.tokens import cleanup_expired_tokens
from routes import health, tokens
from settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(cleanup_expired_tokens())
    logger.info("Запущена фоновая задача очистки просроченных токенов.")
    yield


app = FastAPI(
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)


app.include_router(
    tokens.router,
    prefix=settings.api_v1_prefix + "/token",
    tags=["Token"],
)
app.include_router(
    health.router,
    tags=["Health"],
)
