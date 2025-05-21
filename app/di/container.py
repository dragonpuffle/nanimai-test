import os

from dotenv import load_dotenv
from dependency_injector import containers, providers
from motor.motor_asyncio import AsyncIOMotorClient

from app.services.event_services import EventService


load_dotenv()


class Container(containers.DeclarativeContainer):
    mongo_client = providers.Singleton(AsyncIOMotorClient,
                                       os.getenv('MONGO_URI', "mongodb://localhost:27017"))
    event_service = providers.Factory(EventService, db_client=mongo_client)

container = Container()

def get_event_service():
    return container.event_service()
