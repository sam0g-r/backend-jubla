from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from app.domain.entities.role_permission import RolePermission


class RolePermissionRepository(ABC):
    @abstractmethod
    async def create(self, rp: RolePermission) -> RolePermission:
        pass

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[RolePermission]:
        pass

    @abstractmethod
    async def update(self, rp: RolePermission) -> RolePermission:
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        pass

    @abstractmethod
    async def query(self, filters: Optional[Dict] = None, skip: int = 0, limit: int = 10):
        pass
