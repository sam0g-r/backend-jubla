from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.domain.value_objects import CuidStr


class CreaetEventODM(BaseModel):
    organizationId: CuidStr
    title: str
    slug: str
    description: str
    startDate: datetime
    endDate: datetime
    countryId: CuidStr
    stateId: CuidStr
    currency: str
    isActive: bool
    maxCapacity: Optional[int]
    pastoralLetterDeadline: Optional[datetime]
    paymentDeadline: Optional[datetime]
    price: float


class UpdateEventODM(BaseModel):
    organizationId: Optional[str] = None
    title: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    startDate: Optional[datetime] = None
    endDate: Optional[datetime] = None
    countryId: Optional[str] = None
    stateId: Optional[str] = None
    currency: Optional[str] = None
    isActive: Optional[bool] = None
    maxCapacity: Optional[int] = None
    pastoralLetterDeadline: Optional[datetime] = None
    paymentDeadline: Optional[datetime] = None
    price: Optional[float] = None
