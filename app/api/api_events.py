from http import HTTPStatus
from typing import Optional, List
from uuid import UUID

from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.database.connection import get_db
from app.dtos.EventDTO import EventResponse, EventCreationRequest, EventUpdateRequest
from app.services import event_service

event_router = APIRouter(tags=["events"])


@event_router.post("/create/event", status_code=HTTPStatus.CREATED, response_model=EventResponse)
async def create_event(event_request: EventCreationRequest, request: Request,
                       user_id: Optional[str] = Query(None),
                       db: Session = Depends(get_db)) -> EventResponse:
    if user_id is None:
        raise ValueError("User ID is required to create an event")

    context = request.url.path
    return await event_service.create_event(event_request=event_request,
                                            context=context, user_id=user_id,
                                            db=db)


@event_router.post("/update/event", status_code=HTTPStatus.OK, response_model=EventResponse)
async def update_event(event_request: EventUpdateRequest, request: Request,
                       user_id: Optional[str] = Query(None),
                       db: Session = Depends(get_db)) -> EventResponse:
    if user_id is None:
        raise ValueError("User ID is required to update an event")

    context = request.url.path
    return await event_service.update_event(event_request=event_request,
                                            context=context, user_id=user_id,
                                            db=db)


@event_router.get("/event/{id}", status_code=HTTPStatus.OK, response_model=EventResponse)
async def get_event_by_id(id: UUID, db: Session = Depends(get_db)) -> EventResponse:
    return await event_service.get_event_by_id(id=id, db=db)


@event_router.get("/user/{user_id}", status_code=HTTPStatus.OK, response_model=List[EventResponse])
async def get_events_by_user_id(user_id: UUID, db: Session = Depends(get_db)) -> List[EventResponse]:
    return await event_service.get_events_by_user_id(user_id=user_id, db=db)
