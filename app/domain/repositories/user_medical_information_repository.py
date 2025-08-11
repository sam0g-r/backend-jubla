from app.domain.entities.user_medical_information import UserMedicalInformation
from typing import Optional, List, Dict
from abc import ABC, abstractmethod

class UserMedicalInformationRepository(ABC):
    @abstractmethod
    async def create(self, info: UserMedicalInformation) -> UserMedicalInformation:
        pass

    @abstractmethod
    async def query(self, filters: Optional[Dict] = None, skip: int = 0, limit: int = 10):
        pass
