from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Event:
    id: str
    organization_id: str
    title: str
    slug: str
    description: str
    start_date: datetime
    end_date: datetime
    country_id: str
    state_id: str
    currency: str = "USD"
    is_active: bool = True
    max_capacity: Optional[int] = None
    pastoral_letter_deadline: Optional[datetime] = None
    payment_deadline: Optional[datetime] = None
    price: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    @property
    def is_upcoming(self) -> bool:
        return self.start_date > datetime.now()

    @property
    def is_ongoing(self) -> bool:
        now = datetime.now()
        return self.start_date <= now <= self.end_date
