from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class UserMedicalInformation:
    id: str
    user_id: str
    has_patologies: bool = False
    has_medication: bool = False
    has_allergies: bool = False
    has_medication_allergies: bool = False
    has_surgery_history: bool = False
    has_daietary_restrictions: bool = False
    patologies: Optional[str] = None
    medication: Optional[str] = None
    allergies: Optional[str] = None
    medication_allergies: Optional[str] = None
    surgery_history: Optional[str] = None
    dietary_restrictions: Optional[str] = None
    emergency_contact_name: str
    emergency_contact_phone: str
    emergency_contact_relationship: str
    emergency_contact_email: str
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
