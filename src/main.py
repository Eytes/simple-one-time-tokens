from fastapi import FastAPI

from routes import health, tokens
from settings import settings

app = FastAPI(
    docs_url="/api/docs",
    redoc_url="/api/redoc",
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
