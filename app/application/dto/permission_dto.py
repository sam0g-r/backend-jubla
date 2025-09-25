from pydantic import BaseModel
from datetime import datetime


class PermissionDTO(BaseModel):
    id: str
    module: str
    action: str
    description: str | None = None
    createdAt: datetime
    updatedAt: datetime | None = None

    @classmethod
    def from_entity(cls, p):
        return cls(id=p.id, module=p.module, action=p.action, description=p.description, createdAt=p.createdAt, updatedAt=getattr(p, "updatedAt", None))
