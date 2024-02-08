import uuid

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette.concurrency import run_in_threadpool

from app.database.models.models import Event
from app.dtos.EventDTO import EventUpdateRequest, EventCreationRequest
from app.repository.event_repository import EventRepository


async def create_event(event_request: EventCreationRequest, context, user_id, db: Session):
    event_repo = EventRepository(db)
    event = Event(**event_request.dict())
    event.id = uuid.uuid4()
    event.user_id = user_id
    return await run_in_threadpool(event_repo.create_event, event)


async def update_event(event_request: EventUpdateRequest, context, user_id, db: Session):
    event_repo = EventRepository(db)
    # Fetch the existing event from the database
    event = await run_in_threadpool(event_repo.get_event_by_id, event_request.id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Check if the current user is the owner of the event
    if str(event.user_id) != user_id:
        raise HTTPException(status_code=403,
                            detail="Permission denied: Cannot update another user's event")

    # Proceed with updating the event if the user check passes
    # Map the request fields to the event model, excluding 'id' and fields not set in the request
    for field, value in event_request.dict(exclude={'id'}, exclude_unset=True).items():
        setattr(event, field, value)

    # Use run_in_threadpool to execute the synchronous update operation in a separate thread
    updated_event = await run_in_threadpool(event_repo.update_event, event)
    return updated_event


async def get_event_by_id(id, db: Session):
    event_repo = EventRepository(db)
    return await run_in_threadpool(event_repo.get_event_by_id, id)


async def get_events_by_user_id(user_id, db: Session):
    event_repo = EventRepository(db)
    return await run_in_threadpool(event_repo.get_events_by_user_id, user_id)
