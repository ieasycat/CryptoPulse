from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

import uvicorn

from core.models import db_helper
from core.config import settings
from api.views import router as cryptopulse_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shitdown
    await db_helper.dispose()


main_app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)
main_app.include_router(
    cryptopulse_router, prefix=settings.api.prefix, tags=settings.api.tags
)


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
