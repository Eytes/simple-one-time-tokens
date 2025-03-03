from fastapi import FastAPI
from routes import links, health
from settings import settings


app = FastAPI(
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)


app.include_router(
    links.router,
    prefix=settings.api_v1_prefix + "/links",
    tags=["Links"],
)
app.include_router(
    health.router,
    tags=["health"],
)
