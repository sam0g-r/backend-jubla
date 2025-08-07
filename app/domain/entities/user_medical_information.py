from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class UserMedicalInformation:
    id: str
    userId: str
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
    emergencyContactName: str
    emergencyContactPhone: str
    emergencyContactRelationship: str
    emergencyContactEmail: str
    createdAt: datetime = field(default_factory=datetime.now)
    updatedAt: Optional[datetime] = None
