import uuid
from pydantic import BaseModel
from datetime import datetime

# Base schema for Calendar Event
class CalendarEventBase(BaseModel):
    title: str
    description: str | None = None
    start_time: datetime
    end_time: datetime

# Schema for creating a new event
class CalendarEventCreate(CalendarEventBase):
    pass

# Schema for updating an event
class CalendarEventUpdate(CalendarEventBase):
    pass

# Schema for reading event data (from DB to API)
class CalendarEventInDB(CalendarEventBase):
    id: uuid.UUID
    user_id: uuid.UUID
    google_event_id: str | None = None
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True 