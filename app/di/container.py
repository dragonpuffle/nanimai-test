import os

from beanie import init_beanie
from dotenv import load_dotenv
from dependency_injector import containers, providers
from motor.motor_asyncio import AsyncIOMotorClient

from app.services.event_services import EventService
from app.models.event_models import Event


load_dotenv()


class Container(containers.DeclarativeContainer):
    mongo_client = providers.Singleton(AsyncIOMotorClient,
                                       os.getenv('MONGO_URI', "mongodb://localhost:27017"))
    event_service = providers.Singleton(EventService)

container = Container()


async def init_beanie_container():
    client = container.mongo_client()
    await init_beanie(database=client['events_db'], document_models=[Event])

def get_event_service():
    return container.event_service()
