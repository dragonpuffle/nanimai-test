from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.event_routes import router
from app.di.container import container


@asynccontextmanager
async def lifespan(app: FastAPI):
    event_service = container.event_service()
    await event_service.initialize()
    yield

app = FastAPI(lifespan=lifespan)

app.container = container
app.include_router(router)
