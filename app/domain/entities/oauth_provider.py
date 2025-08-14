from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class OAuthProvider:
    id: str
    userId: str
    provider: str
    providerId: str
    updatedAt: datetime = field(default_factory=datetime.now)
    createdAt: datetime = field(default_factory=datetime.now)
