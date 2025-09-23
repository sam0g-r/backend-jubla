from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class RolePermission:
    id: str
    roleId: str
    permissionId: str
    createdAt: datetime = field(default_factory=datetime.now)
