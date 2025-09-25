from pydantic import BaseModel
from datetime import datetime


class RoleDTO(BaseModel):
    id: str
    name: str
    description: str | None = None
    createdAt: datetime
    updatedAt: datetime | None = None

    @classmethod
    def from_entity(cls, r):
        return cls(id=r.id, name=r.name, description=r.description, createdAt=r.createdAt, updatedAt=getattr(r, "updatedAt", None))
