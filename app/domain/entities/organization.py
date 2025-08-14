from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from app.domain.entities.event import Event


@dataclass
class OrganizationToUser:
    A: str
    B: str


@dataclass
class Organization:
    id: str
    name: str
    description: Optional[str] = None
    logoUrl: Optional[str] = None
    createdAt: datetime = field(default_factory=datetime.now)
    updatedAt: datetime = field(default_factory=datetime.now)
    events: List[Event] = field(default_factory=list)
    organizationToUser: List[OrganizationToUser] = field(default_factory=list)