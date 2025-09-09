from pydantic import BaseModel
from datetime import datetime


class RolePermissionDTO(BaseModel):
    id: str
    roleId: str
    permissionId: str
    createdAt: datetime

    @classmethod
    def from_entity(cls, rp):
        return cls(id=rp.id, roleId=rp.roleId, permissionId=rp.permissionId, createdAt=rp.createdAt)
