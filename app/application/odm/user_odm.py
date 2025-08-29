from pydantic import BaseModel
from typing import Optional
from datetime import date

from app.domain.value_objects import CuidStr


class UpdateUserODM(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    phone: Optional[str] = None
    countryId: Optional[CuidStr] = None
    stateId: Optional[CuidStr] = None
    church: Optional[str] = None
    birthdate: Optional[date] = None
    gender: Optional[str] = None
    documentId: Optional[str] = None
    profession: Optional[str] = None
    instagramProfile: Optional[str] = None
    birthCountry: Optional[CuidStr] = None
