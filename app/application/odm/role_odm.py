from pydantic import BaseModel


class CreateRoleODM(BaseModel):
    name: str
    description: str | None = None


class UpdateRoleODM(BaseModel):
    name: str | None = None
    description: str | None = None
