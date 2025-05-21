from datetime import datetime
from typing import Optional

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

class EventUpdate(EventBase):
    title: Optional[str]
    description: Optional[str]
    start_time: Optional[datetime]
    end_time: Optional[datetime]

class EventRead(EventBase):
    id: str = Field(alias='_id')