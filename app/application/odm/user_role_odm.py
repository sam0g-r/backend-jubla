from pydantic import BaseModel
from typing import Optional
from app.domain.value_objects import CuidStr


class CreateUserRoleODM(BaseModel):
    userId: CuidStr
    roleId: CuidStr
    eventId: Optional[CuidStr] = None


class UpdateUserRoleODM(BaseModel):
    roleId: Optional[CuidStr] = None
    eventId: Optional[CuidStr] = None
