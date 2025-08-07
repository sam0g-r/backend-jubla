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