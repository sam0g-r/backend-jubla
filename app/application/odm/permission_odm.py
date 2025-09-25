from pydantic import BaseModel


class CreatePermissionODM(BaseModel):
    module: str
    action: str
    description: str | None = None


class UpdatePermissionODM(BaseModel):
    module: str | None = None
    action: str | None = None
    description: str | None = None
