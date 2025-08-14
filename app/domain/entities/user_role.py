from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class UserRole:
    id: str
    userId: str
    roleId: str
    eventId: Optional[str] = None
    assignedAt: datetime = field(default_factory=datetime.now)
