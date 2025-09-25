from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Tuple
from app.domain.entities.permission import Permission


class PermissionRepository(ABC):
    @abstractmethod
    async def create(self, p: Permission) -> Permission:
        pass

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[Permission]:
        pass

    @abstractmethod
    async def update(self, p: Permission) -> Permission:
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        pass

    @abstractmethod
    async def query(self, filters: Optional[Dict] = None, skip: int = 0, limit: int = 10) -> Tuple[List[Permission], int]:
        pass
