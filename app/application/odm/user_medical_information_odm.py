from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

from app.domain.value_objects import CuidStr

class UserMedicalInformationODM(BaseModel):
    userId: CuidStr
    emergencyContactName: str
    emergencyContactPhone: str
    emergencyContactRelationship: str
    emergencyContactEmail: EmailStr
    hasPatologies: bool = False
    hasMedication: bool = False
    hasAllergies: bool = False
    hasMedicationAllergies: bool = False
    hasSurgeryHistory: bool = False
    hasDaietaryRestrictions: bool = False
    patologies: Optional[str] = None
    medication: Optional[str] = None
    allergies: Optional[str] = None
    medicationAllergies: Optional[str] = None
    surgeryHistory: Optional[str] = None
    dietaryRestrictions: Optional[str] = None
