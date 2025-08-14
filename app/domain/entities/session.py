from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Session:
    id: str
    userId: str
    token: str
    expiresAt: datetime
    createdAt: datetime = field(default_factory=datetime.now)
