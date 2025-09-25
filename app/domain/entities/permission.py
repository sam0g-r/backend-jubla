from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Permission:
    id: str
    module: str
    action: str
    description: str | None = None
    createdAt: datetime = field(default_factory=datetime.now)
    updatedAt: datetime | None = None
