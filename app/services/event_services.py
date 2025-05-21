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

    @staticmethod
    def parse_event(data: dict) -> EventRead:
        data = data.copy()
        if "_id" in data and isinstance(data["_id"], ObjectId):
            data["_id"] = str(data["_id"])
        return EventRead.model_validate(data)

    def parse_events(self, datas: List[dict]) -> List[EventRead]:
        return [self.parse_event(data) for data in datas]

    async def create_event(self, event: EventCreate) -> EventRead:
        conflict = await self.collection.find_one({
            "$or": [
                {
                    "start_time": {"$lte": event.start_time},
                    "end_time": {"$gt": event.start_time},
                },
                {
                    "start_time": {"$lt": event.end_time},
                    "end_time": {"$gte": event.end_time},
                },
                {
                    "start_time": {"$gte": event.start_time},
                    "end_time": {"$lte": event.end_time},
                },
                {
                    "start_time": {"$lte": event.start_time},
                    "end_time": {"$gte": event.end_time},
                }
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
        return self.parse_event(dict(event))

    async def get_all_events(self) -> List[EventRead]:
        cursor = self.collection.find({})
        events = await cursor.to_list(length=100)
        return self.parse_events(events)

    async def get_range_events(self, start: datetime, end: datetime) -> List[EventRead]:
        cursor = self.collection.find({
            "$or": [
                {
                    "start_time": {"$lte": start},
                    "end_time": {"$gt": start},
                },
                {
                    "start_time": {"$lt": end},
                    "end_time": {"$gte": end},
                },
                {
                    "start_time": {"$gte": start},
                    "end_time": {"$lte": end},
                },
                {
                    "start_time": {"$lte": start},
                    "end_time": {"$gte": end},
                }
            ]
        })
        events = await cursor.to_list(length=100)
        return self.parse_events(events)


    async def delete_event(self, event_id: str):
        result = await self.collection.delete_one({'_id': ObjectId(event_id)})
        if result.deleted_count == 0:
            raise HTTPException(404, 'Событие не найдено')
        return {'msg': 'deleted'}
