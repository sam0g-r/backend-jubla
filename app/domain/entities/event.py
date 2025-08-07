<<<<<<< Updated upstream
=======
<<<<<<< Updated upstream
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Event:
    id: str
    title: str
    slug: str
    description: str
    start_date: datetime
    end_date: datetime
    max_participants: int
    current_participants: int
    price: float
    is_active: bool = True
    created_at: datetime = datetime.now()
    updated_at: Optional[datetime] = None
    
    @property
    def is_full(self) -> bool:
        return self.current_participants >= self.max_participants
    
    @property
    def available_spots(self) -> int:
        return max(0, self.max_participants - self.current_participants)
    
    @property
    def is_upcoming(self) -> bool:
        return self.start_date > datetime.now()
    
    @property
    def is_ongoing(self) -> bool:
        now = datetime.now()
        return self.start_date <= now <= self.end_date 
=======
>>>>>>> Stashed changes
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Event:
    id: str
<<<<<<< Updated upstream
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
=======
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
    updatedAt: Optional[datetime] = None

    @property
    def is_upcoming(self) -> bool:
        return self.startDate > datetime.now()
>>>>>>> Stashed changes

    @property
    def is_ongoing(self) -> bool:
        now = datetime.now()
<<<<<<< Updated upstream
        return self.start_date <= now <= self.end_date
=======
        return self.startDate <= now <= self.endDate
>>>>>>> Stashed changes
>>>>>>> Stashed changes
