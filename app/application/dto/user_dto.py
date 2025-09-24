from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class CreateUserDTO(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    birthdate: datetime
    gender: Optional[str] = None
    documentId: Optional[str] = None
    profession: Optional[str] = None
    instagramProfile: Optional[str] = None
    birthCountry: str
    phone: str
    countryId: str
    stateId: str
    password: str
    church: str

class UpdateUserDTO(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    phone: Optional[str] = None
    countryId: Optional[str] = None
    stateId: Optional[str] = None
    church: Optional[str] = None
    gender: Optional[str] = None
    documentId: Optional[str] = None
    profession: Optional[str] = None
    instagramProfile: Optional[str] = None
    birthCountry: Optional[str] = None

class UserResponseDTO(BaseModel):
    id: str
    firstname: str
    lastname: str
    email: str
    birthdate: datetime
    gender: Optional[str] = None
    documentId: Optional[str] = None
    profession: Optional[str] = None
    instagramProfile: Optional[str] = None
    birthCountry: str
    phone: str
    countryId: str
    stateId: str
    church: Optional[str] = None
    isActive: bool
    isVerified: bool
    createdAt: datetime
    updatedAt: Optional[datetime] = None

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
            gender=getattr(user, 'gender', None),
            documentId=getattr(user, 'documentId', None),
            profession=getattr(user, 'profession', None),
            instagramProfile=getattr(user, 'instagramProfile', None),
            birthCountry=user.birthCountry,
            phone=user.phone,
            countryId=user.countryId,
            stateId=user.stateId,
            church=user.church,
            isActive=user.isActive,
            isVerified=user.isVerified,
            createdAt=user.createdAt,
            updatedAt=user.updatedAt
        )