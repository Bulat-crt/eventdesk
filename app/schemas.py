from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime

class EventCreate(BaseModel):
    title: str
    location: str
    starts_at: datetime
    capacity: int = Field(gt=0)
    description: str | None = None


class EventResponse(BaseModel):
    id: int
    title: str
    description: str | None
    starts_at: datetime
    location: str
    capacity: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class RegistrationCreate(BaseModel):
    attendee_name: str
    attendee_email: EmailStr

class RegistrationResponse(BaseModel):
    id: int
    event_id: int
    attendee_name: str
    attendee_email: EmailStr
    registered_at: datetime

    model_config = ConfigDict(from_attributes=True)

class EventRegistrationStats(BaseModel):
    event_id: int
    registered_count: int
    capacity: int
    available_places: int