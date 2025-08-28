from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.file import File

class FileRepository(ABC):
    @abstractmethod
    async def create(self, file: File) -> File:
        pass

    @abstractmethod
    async def get_by_id(self, file_id: str) -> Optional[File]:
        pass

    @abstractmethod
    async def list_by_user(self, userId: str) -> List[File]:
        pass

    @abstractmethod
    async def update(self, file_id: str, updates: dict) -> File:
        pass
