from app.domain.entities.user_medical_information import UserMedicalInformation
from app.domain.repositories.user_medical_information_repository import UserMedicalInformationRepository
from typing import Dict, Any, List, Optional, Tuple
from uuid import uuid4
from datetime import datetime

class CreateUserMedicalInformationUseCase:
    def __init__(self, repo: UserMedicalInformationRepository):
        self.repo = repo

    async def execute(self, data: Dict[str, Any]) -> UserMedicalInformation:
        info = UserMedicalInformation(
            id=str(uuid4()),
            userId=data["userId"],
            hasPatologies=data.get("hasPatologies", False),
            hasMedication=data.get("hasMedication", False),
            hasAllergies=data.get("hasAllergies", False),
            hasMedicationAllergies=data.get("hasMedicationAllergies", False),
            hasSurgeryHistory=data.get("hasSurgeryHistory", False),
            hasDaietaryRestrictions=data.get("hasDaietaryRestrictions", False),
            patologies=data.get("patologies"),
            medication=data.get("medication"),
            allergies=data.get("allergies"),
            medicationAllergies=data.get("medicationAllergies"),
            surgeryHistory=data.get("surgeryHistory"),
            dietaryRestrictions=data.get("dietaryRestrictions"),
            emergencyContactName=data["emergencyContactName"],
            emergencyContactPhone=data["emergencyContactPhone"],
            emergencyContactRelationship=data["emergencyContactRelationship"],
            emergencyContactEmail=data["emergencyContactEmail"],
            createdAt=datetime.now(),
            updatedAt=None
        )
        return await self.repo.create(info)

class QueryUserMedicalInformationUseCase:
    def __init__(self, repo: UserMedicalInformationRepository):
        self.repo = repo

    async def execute(self, filters: Optional[Dict] = None, skip: int = 0, limit: int = 10) -> Tuple[List[UserMedicalInformation], int]:
        return await self.repo.query(filters, skip, limit)
