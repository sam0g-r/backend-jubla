from app.domain.entities.user_medical_information import UserMedicalInformation
from app.domain.repositories.user_medical_information_repository import UserMedicalInformationRepository
from app.infrastructure.database.prisma_client import prisma_client
from typing import Dict, List, Optional

class UserMedicalInformationRepositoryImpl(UserMedicalInformationRepository):
    def _to_entity(self, db_info) -> UserMedicalInformation:
        return UserMedicalInformation(
            id=db_info.id,
            userId=db_info.userId,
            emergencyContactName=db_info.emergencyContactName,
            emergencyContactPhone=db_info.emergencyContactPhone,
            emergencyContactRelationship=db_info.emergencyContactRelationship,
            emergencyContactEmail=db_info.emergencyContactEmail,
            hasPatologies=db_info.hasPatologies,
            hasMedication=db_info.hasMedication,
            hasAllergies=db_info.hasAllergies,
            hasMedicationAllergies=db_info.hasMedicationAllergies,
            hasSurgeryHistory=db_info.hasSurgeryHistory,
            hasDaietaryRestrictions=db_info.hasDaietaryRestrictions,
            patologies=db_info.patologies,
            medication=db_info.medication,
            allergies=db_info.allergies,
            medicationAllergies=db_info.medicationAllergies,
            surgeryHistory=db_info.surgeryHistory,
            dietaryRestrictions=db_info.dietaryRestrictions,
            createdAt=db_info.createdAt,
            updatedAt=db_info.updatedAt
        )

    async def create(self, info: UserMedicalInformation) -> UserMedicalInformation:
        async with prisma_client as client:
            db_info = await client.client.usermedicalinformation.create(data=info.__dict__)
        return self._to_entity(db_info)

    async def query(self, filters: Optional[Dict] = None, skip: int = 0, limit: int = 10):
        filters = filters or {}
        async with prisma_client as client:
            total = await client.client.usermedicalinformation.count(where=filters)
            db_infos = await client.client.usermedicalinformation.find_many(where=filters, skip=skip, take=limit, order={"createdAt": "desc"})
        return [self._to_entity(i) for i in db_infos], total
