from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends

from app.models.event_models import EventCreate, EventUpdate, EventRead
from app.services.event_services import EventService
from app.di.container import get_event_service


router = APIRouter()

@router.post('/events', response_model=EventRead)
async def handle_create_event(event: EventCreate, service: EventService = Depends(get_event_service)):
    return await service.create_event(event)

@router.put('/events/{event_id}', response_model=EventRead)
async def handle_update_event(event_id: str, event: EventUpdate, service: EventService = Depends(get_event_service)):
    return await service.update_event(event_id, event)

@router.get('/events/range', response_model=List[EventRead])
async def handle_get_range_events(start: datetime, end: datetime, service: EventService = Depends(get_event_service)):
    return await service.get_range_events(start, end)

@router.get('/events/{event_id}', response_model=EventRead)
async def handle_get_one_event(event_id: str, service: EventService = Depends(get_event_service)):
    return await service.get_one_event(event_id)

@router.get('/events', response_model=List[EventRead])
async def handle_get_all_events(service: EventService = Depends(get_event_service)):
    return await service.get_all_events()

@router.delete('/events/{event_id}')
async def handle_delete_event(event_id: str, service: EventService = Depends(get_event_service)):
    return await service.delete_event(event_id)
