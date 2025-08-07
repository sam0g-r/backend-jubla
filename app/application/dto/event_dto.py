from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CreateEventDTO(BaseModel):
    organizationId: str
    title: str
    slug: str
    description: str
    startDate: datetime
    endDate: datetime
    countryId: str
    stateId: str
    currency: str = "USD"
    maxCapacity: Optional[int] = None
    pastoralLetterDeadline: Optional[datetime] = None
    paymentDeadline: Optional[datetime] = None
    price: float = 0.0

class UpdateEventDTO(BaseModel):
    organizationId: Optional[str] = None
    title: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    startDate: Optional[datetime] = None
    endDate: Optional[datetime] = None
    countryId: Optional[str] = None
    stateId: Optional[str] = None
    currency: Optional[str] = None
    maxCapacity: Optional[int] = None
    pastoralLetterDeadline: Optional[datetime] = None
    paymentDeadline: Optional[datetime] = None
    price: Optional[float] = None
    isActive: Optional[bool] = None

class EventResponseDTO(BaseModel):
    id: str
    organizationId: str
    title: str
    slug: str
    description: str
    startDate: datetime
    endDate: datetime
    countryId: str
    stateId: str
    currency: str
    isActive: bool
    maxCapacity: Optional[int] = None
    pastoralLetterDeadline: Optional[datetime] = None
    paymentDeadline: Optional[datetime] = None
    price: float
    createdAt: datetime
    updatedAt: Optional[datetime] = None

    class Config:
        orm_mode = True

    @classmethod
    def from_entity(cls, event):
        return cls(
            id=event.id,
            organizationId=event.organizationId,
            title=event.title,
            slug=event.slug,
            description=event.description,
            startDate=event.startDate,
            endDate=event.endDate,
            countryId=event.countryId,
            stateId=event.stateId,
            currency=event.currency,
            isActive=event.isActive,
            maxCapacity=event.maxCapacity,
            pastoralLetterDeadline=event.pastoralLetterDeadline,
            paymentDeadline=event.paymentDeadline,
            price=event.price,
            createdAt=event.createdAt,
            updatedAt=event.updatedAt
        )
