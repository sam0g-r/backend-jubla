from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserRoleDTO(BaseModel):
    id: str
    userId: str
    roleId: str
    eventId: Optional[str] = None
    assignedAt: datetime

    @classmethod
    def from_entity(cls, user_role):
        return cls(
            id=user_role.id,
            userId=user_role.userId,
            roleId=user_role.roleId,
            eventId=user_role.eventId,
            assignedAt=user_role.assignedAt,
        )
