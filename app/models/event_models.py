from datetime import datetime
from typing import Optional

from beanie import Document
from pydantic import BaseModel, Field, field_validator


class EventBase(BaseModel):
    title: str
    description: str
    start_time: datetime
    end_time: datetime

    @field_validator('end_time')
    @classmethod
    def validate_end_time(cls, end_time, values):
        start_time = values.data.get('start_time')
        if end_time < start_time:
            raise ValueError('End time must be after start time')
        return end_time

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

class EventRead(EventBase):
    id: str = Field(alias='_id')


class Event(Document, EventBase):
    class Settings:
        name = 'events'

        indexes = ['start_time', 'end_time']

