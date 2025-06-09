from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.api import event_routes
from app.api.event_routes import router
from app.di.container import container, init_beanie_container


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_beanie_container()
    container.wire(modules=[event_routes])
    yield

app = FastAPI(lifespan=lifespan)

app.container = container
app.include_router(router)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
