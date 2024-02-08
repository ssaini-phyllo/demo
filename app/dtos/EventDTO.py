from datetime import datetime
from http import HTTPStatus
from typing import List, Optional
from uuid import UUID

from pydantic import validator, BaseModel, Field

from app.utils.utils import RequestError, ErrorCode


class EventCreationRequest(BaseModel):
    name: str = Field(..., min_length=1, description="The name of the event")
    description: str = Field(..., description="The description of the event")
    start_date: datetime = Field(..., description="The start date and time of the event")
    end_date: datetime = Field(..., description="The end date and time of the event")

    @validator('start_date')
    def validate_start_date(cls, start_date):
        if not start_date:
            raise RequestError(status_code=HTTPStatus.BAD_REQUEST, error_code=ErrorCode.INVALID_START_DATE)
        return start_date

    @validator('end_date')
    def validate_end_date(cls, end_date, values):
        if not end_date:
            raise RequestError(status_code=HTTPStatus.BAD_REQUEST, error_code=ErrorCode.INVALID_END_DATE)
        if 'start_date' in values and end_date < values['start_date']:
            raise RequestError(status_code=HTTPStatus.BAD_REQUEST, error_code=ErrorCode.INVALID_END_DATE)
        return end_date


class EventResponse(BaseModel):
    id: UUID
    name: str
    description: str
    start_date: datetime
    end_date: datetime
    created_at: datetime
    updated_at: datetime


class EventUpdateRequest(BaseModel):
    id: UUID = Field(..., description="The ID of the event to update")
    name: Optional[str] = Field(None, min_length=1, description="The new name of the event")
    description: Optional[str] = Field(None, description="The new description of the event")
    start_date: Optional[datetime] = Field(None, description="The new start date and time of the event")
    end_date: Optional[datetime] = Field(None, description="The new end date and time of the event")

    @validator('id')
    def validate_id(cls, event_id):
        if not event_id:
            raise RequestError(status_code=HTTPStatus.BAD_REQUEST, error_code=ErrorCode.INVALID_ID)
        return event_id
