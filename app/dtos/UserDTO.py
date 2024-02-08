from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, EmailStr


class UserCreationRequest(BaseModel):
    name: str = Field(..., example="John Doe")
    email: EmailStr = Field(..., example="john.doe@example.com")
    mobile: str = Field(..., example="1234567890")


class UserResponse(BaseModel):
    id: UUID = Field(default_factory=uuid4, example="123e4567-e89b-12d3-a456-426614174000")
    name: str = Field(..., example="John Doe")
    email: EmailStr = Field(..., example="john.doe@example.com")
    mobile: str = Field(..., example="1234567890")
    created_at: datetime = Field(default_factory=datetime.now, example="2022-01-01T00:00:00Z")
    updated_at: datetime = Field(default_factory=datetime.now, example="2022-01-01T00:00:00Z")
