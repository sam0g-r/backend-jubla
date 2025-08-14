from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Event:
    id: str
    organizationId: str
    title: str
    slug: str
    description: str
    startDate: datetime
    endDate: datetime
    countryId: str
    stateId: str
    currency: str = "USD"
    isActive: bool = True
    maxCapacity: Optional[int] = None
    pastoralLetterDeadline: Optional[datetime] = None
    paymentDeadline: Optional[datetime] = None
    price: float = 0.0
    createdAt: datetime = field(default_factory=datetime.now)
    updatedAt: datetime = field(default_factory=datetime.now)

    @property
    def is_upcoming(self) -> bool:
        return self.startDate > datetime.now()

    @property
    def is_ongoing(self) -> bool:
        now = datetime.now()
        return self.startDate <= now <= self.endDate
