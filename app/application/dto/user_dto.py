from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class CreateUserDTO(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    birthdate: datetime
    phone: str
    country_id: str
    state_id: str
    password: str
    church: Optional[str] = None

class UpdateUserDTO(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    phone: Optional[str] = None
    country_id: Optional[str] = None
    state_id: Optional[str] = None
    church: Optional[str] = None

class UserResponseDTO(BaseModel):
    id: str
    firstname: str
    lastname: str
    email: str
    birthdate: datetime
    phone: str
    country_id: str
    state_id: str
    church: Optional[str] = None
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

    @classmethod
    def from_entity(cls, user):
        return cls(
            id=user.id,
            firstname=user.firstname,
            lastname=user.lastname,
            email=user.email,
            birthdate=user.birthdate,
            phone=user.phone,
            country_id=user.country_id,
            state_id=user.state_id,
            church=user.church,
            is_active=user.is_active,
            is_verified=user.is_verified,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
