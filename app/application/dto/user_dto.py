from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from uuid import UUID

class CreateUserDTO(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    birthdate: datetime
    phone: str
    country: str
    state: str
    password: str

class UpdateUserDTO(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    phone: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None

class UserResponseDTO(BaseModel):
    id: UUID
    firstname: str
    lastname: str
    email: str
    birthdate: datetime
    phone: str
    country: str
    state: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_entity(cls, user):
        return cls(
            id=user.id,
            firstname=user.firstname,
            lastname=user.lastname,
            email=user.email,
            birthdate=user.birthdate,
            phone=user.phone,
            country=user.country,
            state=user.state,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at
        ) 