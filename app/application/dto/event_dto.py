from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CreateEventDTO(BaseModel):
    title: str
    slug: str
    description: str
    start_date: datetime
    end_date: datetime
    max_participants: int
    price: float

class UpdateEventDTO(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    max_participants: Optional[int] = None
    price: Optional[float] = None
    is_active: Optional[bool] = None

class EventResponseDTO(BaseModel):
    id: str
    title: str
    slug: str
    description: str
    start_date: datetime
    end_date: datetime
    max_participants: int
    current_participants: int
    price: float
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_entity(cls, event):
        return cls(
            id=event.id,
            title=event.title,
            slug=event.slug,
            description=event.description,
            start_date=event.start_date,
            end_date=event.end_date,
            max_participants=event.max_participants,
            current_participants=event.current_participants,
            price=event.price,
            is_active=event.is_active,
            created_at=event.created_at,
            updated_at=event.updated_at
        )
