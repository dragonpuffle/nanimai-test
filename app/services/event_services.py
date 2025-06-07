from typing import List

from beanie import PydanticObjectId
from bson import ObjectId
from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException

from app.models.event_models import EventCreate, EventUpdate, Event


class EventService:
    async def create_event(self, data: EventCreate) -> Event:
        conflict = await Event.find({
            "$or": [
                {
                    "start_time": {"$lte": data.start_time},
                    "end_time": {"$gt": data.start_time},
                },
                {
                    "start_time": {"$lt": data.end_time},
                    "end_time": {"$gte": data.end_time},
                },
                {
                    "start_time": {"$gte": data.start_time},
                    "end_time": {"$lte": data.end_time},
                },
                {
                    "start_time": {"$lte": data.start_time},
                    "end_time": {"$gte": data.end_time},
                }
            ]
        }).first_or_none()
        if conflict:
            raise HTTPException(400, detail='Событие пересекается с другим')
        result = Event(**data.model_dump())
        await result.insert()
        return result


    async def update_event(self, event_id: str, data: EventUpdate) -> Event:
        existing_event = await Event.get(PydanticObjectId(event_id))
        if not existing_event:
            raise HTTPException(404, detail='Event not found')

        await existing_event.set(data.model_dump(exclude_unset=True))
        return existing_event


    async def get_one_event(self, event_id: str) -> Event:
        event = await Event.get(PydanticObjectId(event_id))
        if not event:
            raise HTTPException(404, detail='Event not found')
        return event


    async def get_all_events(self) -> List[Event]:
        return await Event.find_all().to_list()


    async def get_range_events(self, start: datetime, end: datetime) -> List[Event]:
        return await Event.find({
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
        }).to_list()


    async def delete_event(self, event_id: str):
        event = await Event.get(PydanticObjectId(event_id))
        if not event:
            raise HTTPException(404, detail='Event not found')
        await event.delete()
        return {'msg': 'deleted'}
