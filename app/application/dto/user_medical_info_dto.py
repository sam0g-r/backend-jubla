from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserMedicalInformationDTO(BaseModel):
    id: str
    userId: str
    emergencyContactName: str
    emergencyContactPhone: str
    emergencyContactRelationship: str
    emergencyContactEmail: str
    createdAt: datetime
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
    updatedAt: Optional[datetime] = None

    @classmethod
    def from_entity(cls, user_medical_info):
        return cls(
            id=user_medical_info.id,
            userId=user_medical_info.userId,
            emergencyContactName=user_medical_info.emergencyContactName,
            emergencyContactPhone=user_medical_info.emergencyContactPhone,
            emergencyContactRelationship=user_medical_info.emergencyContactRelationship,
            emergencyContactEmail=user_medical_info.emergencyContactEmail,
            createdAt=user_medical_info.createdAt,
            hasPatologies=user_medical_info.hasPatologies,
            hasMedication=user_medical_info.hasMedication,
            hasAllergies=user_medical_info.hasAllergies,
            hasMedicationAllergies=user_medical_info.hasMedicationAllergies,
            hasSurgeryHistory=user_medical_info.hasSurgeryHistory,
            hasDaietaryRestrictions=user_medical_info.hasDaietaryRestrictions,
            patologies=user_medical_info.patologies,
            medication=user_medical_info.medication,
            allergies=user_medical_info.allergies,
            medicationAllergies=user_medical_info.medicationAllergies,
            surgeryHistory=user_medical_info.surgeryHistory,
            dietaryRestrictions=user_medical_info.dietaryRestrictions,
            updatedAt=user_medical_info.updatedAt
        )