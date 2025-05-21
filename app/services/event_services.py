from typing import List
from bson import ObjectId
from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException

from app.models.event_models import EventCreate, EventUpdate, EventRead


class EventService:
    def __init__(self, db_client: AsyncIOMotorClient):
        self.collection = db_client['events_db']['events']

    async def initialize(self):
        await self.collection.create_index('start_time')
        await self.collection.create_index('end_time')

    async def create_event(self, event: EventCreate) -> EventRead:
        conflict = await self.collection.find_one({
            "$or": [
                {'start_time': {'%lt': event.end_time}, 'end_time': {'%gt': event.start_time}},
            ]
        })
        if conflict:
            raise HTTPException(400, detail='Событие пересекается с другим')
        result = await self.collection.insert_one(event.model_dump())
        new_event = await self.get_one_event(result.inserted_id)
        return new_event

    async def update_event(self, event_id: str, event: EventUpdate) -> EventRead:
        obj_id = ObjectId(event_id)
        await self.collection.update_one({'_id': obj_id}, {'$set': event.model_dump()})
        updated_event = await self.get_one_event(event_id)
        return updated_event

    async def get_one_event(self, event_id: str) -> EventRead:
        obj_id = ObjectId(event_id)
        event = await self.collection.find_one({'_id': obj_id})
        if not event:
            raise HTTPException(404, 'Событие не найдено')
        return EventRead(**event)

    async def get_all_events(self) -> List[EventRead]:
        cursor = self.collection.find({})
        events = await cursor.to_list(length=100)
        return [EventRead(**e) for e in events]

    async def get_range_events(self, start: datetime, end: datetime) -> List[EventRead]:
        cursor = self.collection.find({
            'start_time': {'$lte': end},
            'end_time': {'$gte': start}
        })
        events = await cursor.to_list(length=100)
        return [EventRead(**e) for e in events]

    async def delete_event(self, event_id: str):
        result = await self.collection.delete_one({'_id': ObjectId(event_id)})
        if result.deleted_count == 0:
            raise HTTPException(404, 'Событие не найдено')
        return {'msg': 'deleted'}
