from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CreateEventDTO(BaseModel):
    organization_id: str
    title: str
    slug: str
    description: str
    start_date: datetime
    end_date: datetime
    country_id: str
    state_id: str
    currency: str = "USD"
    max_capacity: Optional[int] = None
    pastoral_letter_deadline: Optional[datetime] = None
    payment_deadline: Optional[datetime] = None
    price: float = 0.0

class UpdateEventDTO(BaseModel):
    organization_id: Optional[str] = None
    title: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    country_id: Optional[str] = None
    state_id: Optional[str] = None
    currency: Optional[str] = None
    max_capacity: Optional[int] = None
    pastoral_letter_deadline: Optional[datetime] = None
    payment_deadline: Optional[datetime] = None
    price: Optional[float] = None
    is_active: Optional[bool] = None

class EventResponseDTO(BaseModel):
    id: str
    organization_id: str
    title: str
    slug: str
    description: str
    start_date: datetime
    end_date: datetime
    country_id: str
    state_id: str
    currency: str
    is_active: bool
    max_capacity: Optional[int] = None
    pastoral_letter_deadline: Optional[datetime] = None
    payment_deadline: Optional[datetime] = None
    price: float
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

    @classmethod
    def from_entity(cls, event):
        return cls(
            id=event.id,
            organization_id=event.organization_id,
            title=event.title,
            slug=event.slug,
            description=event.description,
            start_date=event.start_date,
            end_date=event.end_date,
            country_id=event.country_id,
            state_id=event.state_id,
            currency=event.currency,
            is_active=event.is_active,
            max_capacity=event.max_capacity,
            pastoral_letter_deadline=event.pastoral_letter_deadline,
            payment_deadline=event.payment_deadline,
            price=event.price,
            created_at=event.created_at,
            updated_at=event.updated_at
        )
