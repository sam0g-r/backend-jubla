from pydantic import BaseModel
from app.domain.value_objects import CuidStr


class CreateRolePermissionODM(BaseModel):
    roleId: CuidStr
    permissionId: CuidStr


class UpdateRolePermissionODM(BaseModel):
    roleId: CuidStr | None = None
    permissionId: CuidStr | None = None
