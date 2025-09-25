from app.application.dto.permission_dto import PermissionDTO
from app.domain.entities.permission import Permission
from app.domain.repositories.permission_repository import PermissionRepository
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from app.infrastructure.database.prisma_client import prisma_client
from cuid2 import cuid_wrapper


class CreatePermissionUseCase:
    def __init__(self, repo: PermissionRepository):
        self.repo = repo

    async def execute(self, data: Dict[str, Any]) -> PermissionDTO:
        module = data.get("module")
        action = data.get("action")
        if not module or not action:
            raise Exception("module and action are required")
        # unique (module, action)
        exists = await prisma_client.client.permission.find_first(where={"module": module, "action": action})
        if exists:
            raise Exception(f"Permission for module {module} and action {action} already exists")
        generate_id = cuid_wrapper()
        p = Permission(id=generate_id(), module=module, action=action, description=data.get("description"), createdAt=datetime.now())
        created = await self.repo.create(p)
        return PermissionDTO.from_entity(created)


class QueryPermissionUseCase:
    def __init__(self, repo: PermissionRepository):
        self.repo = repo

    async def execute(self, filters: Optional[Dict] = None, skip: int = 0, limit: int = 10) -> Tuple[List[PermissionDTO], int]:
        results, total = await self.repo.query(filters, skip, limit)
        return [PermissionDTO.from_entity(r) for r in results], total


class GetPermissionUseCase:
    def __init__(self, repo: PermissionRepository):
        self.repo = repo

    async def execute(self, id: str) -> Optional[PermissionDTO]:
        p = await self.repo.get_by_id(id)
        return PermissionDTO.from_entity(p) if p else None


class UpdatePermissionUseCase:
    def __init__(self, repo: PermissionRepository):
        self.repo = repo

    async def execute(self, id: str, data: Dict[str, Any]) -> PermissionDTO:
        existing = await self.repo.get_by_id(id)
        if not existing:
            raise Exception(f"Permission with id {id} not found")
        existing.module = data.get("module", existing.module)
        existing.action = data.get("action", existing.action)
        existing.description = data.get("description", existing.description)
        updated = await self.repo.update(existing)
        return PermissionDTO.from_entity(updated)


class DeletePermissionUseCase:
    def __init__(self, repo: PermissionRepository):
        self.repo = repo

    async def execute(self, id: str) -> bool:
        return await self.repo.delete(id)
