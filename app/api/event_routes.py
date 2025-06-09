from datetime import datetime
from typing import List, Annotated

from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject

from app.models.event_models import EventCreate, EventUpdate, Event
from app.services.event_services import EventService
from app.di.container import Container


router = APIRouter()

@router.post('/events', response_model=Event)
@inject
async def handle_create_event(event: EventCreate, service: Annotated[EventService, Depends(Provide[Container.event_service])]):
    return await service.create_event(event)

@router.put('/events/{event_id}', response_model=Event)
@inject
async def handle_update_event(event_id: str, event: EventUpdate, service: Annotated[EventService, Depends(Provide[Container.event_service])]):
    return await service.update_event(event_id, event)

@router.get('/events/range', response_model=List[Event])
@inject
async def handle_get_range_events(start: datetime, end: datetime, service: Annotated[EventService, Depends(Provide[Container.event_service])]):
    return await service.get_range_events(start, end)

@router.get('/events/{event_id}', response_model=Event)
@inject
async def handle_get_one_event(event_id: str, service: Annotated[EventService, Depends(Provide[Container.event_service])]):
    return await service.get_one_event(event_id)

@router.get('/events', response_model=List[Event])
@inject
async def handle_get_all_events(service: Annotated[EventService, Depends(Provide[Container.event_service])]):
    return await service.get_all_events()

@router.delete('/events/{event_id}')
@inject
async def handle_delete_event(event_id: str, service: Annotated[EventService, Depends(Provide[Container.event_service])]):
    return await service.delete_event(event_id)
