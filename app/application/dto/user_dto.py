<<<<<<< Updated upstream
=======
<<<<<<< Updated upstream
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

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
    id: str
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
=======
>>>>>>> Stashed changes
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class CreateUserDTO(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    birthdate: datetime
    phone: str
<<<<<<< Updated upstream
    country_id: str
    state_id: str
    password: str
    church: Optional[str] = None
=======
    countryId: str
    stateId: str
    password: str
    church: str
>>>>>>> Stashed changes

class UpdateUserDTO(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    phone: Optional[str] = None
<<<<<<< Updated upstream
    country_id: Optional[str] = None
    state_id: Optional[str] = None
=======
    countryId: Optional[str] = None
    stateId: Optional[str] = None
>>>>>>> Stashed changes
    church: Optional[str] = None

class UserResponseDTO(BaseModel):
    id: str
    firstname: str
    lastname: str
    email: str
    birthdate: datetime
    phone: str
<<<<<<< Updated upstream
    country_id: str
    state_id: str
    church: Optional[str] = None
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
=======
    countryId: str
    stateId: str
    church: Optional[str] = None
    isActive: bool
    isVerified: bool
    createdAt: datetime
    updatedAt: Optional[datetime] = None
>>>>>>> Stashed changes

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
<<<<<<< Updated upstream
            country_id=user.country_id,
            state_id=user.state_id,
            church=user.church,
            is_active=user.is_active,
            is_verified=user.is_verified,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
=======
            countryId=user.countryId,
            stateId=user.stateId,
            church=user.church,
            isActive=user.isActive,
            isVerified=user.isVerified,
            createdAt=user.createdAt,
            updatedAt=user.updatedAt
        )
>>>>>>> Stashed changes
>>>>>>> Stashed changes
