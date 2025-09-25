from app.application.dto.role_dto import RoleDTO
from app.domain.entities.role import Role
from app.domain.repositories.role_repository import RoleRepository
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from app.infrastructure.database.prisma_client import prisma_client
from cuid2 import cuid_wrapper


class CreateRoleUseCase:
    def __init__(self, repo: RoleRepository):
        self.repo = repo

    async def execute(self, data: Dict[str, Any]) -> RoleDTO:
        name = data.get("name")
        if not name:
            raise Exception("name is required")
        # unique name
        exists = await prisma_client.client.role.find_unique(where={"name": name})
        if exists:
            raise Exception(f"Role with name {name} already exists")
        generate_id = cuid_wrapper()
        r = Role(id=generate_id(), name=name, description=data.get("description"), createdAt=datetime.now())
        created = await self.repo.create(r)
        return RoleDTO.from_entity(created)


class QueryRoleUseCase:
    def __init__(self, repo: RoleRepository):
        self.repo = repo

    async def execute(self, filters: Optional[Dict] = None, skip: int = 0, limit: int = 10) -> Tuple[List[RoleDTO], int]:
        results, total = await self.repo.query(filters, skip, limit)
        return [RoleDTO.from_entity(r) for r in results], total


class GetRoleUseCase:
    def __init__(self, repo: RoleRepository):
        self.repo = repo

    async def execute(self, id: str) -> Optional[RoleDTO]:
        r = await self.repo.get_by_id(id)
        return RoleDTO.from_entity(r) if r else None


class UpdateRoleUseCase:
    def __init__(self, repo: RoleRepository):
        self.repo = repo

    async def execute(self, id: str, data: Dict[str, Any]) -> RoleDTO:
        existing = await self.repo.get_by_id(id)
        if not existing:
            raise Exception(f"Role with id {id} not found")
        existing.name = data.get("name", existing.name)
        existing.description = data.get("description", existing.description)
        updated = await self.repo.update(existing)
        return RoleDTO.from_entity(updated)


class DeleteRoleUseCase:
    def __init__(self, repo: RoleRepository):
        self.repo = repo

    async def execute(self, id: str) -> bool:
        return await self.repo.delete(id)
