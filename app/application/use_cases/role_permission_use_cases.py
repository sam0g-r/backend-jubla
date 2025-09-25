from app.application.dto.role_permission_dto import RolePermissionDTO
from app.domain.entities.role_permission import RolePermission
from app.domain.repositories.role_permission_repository import RolePermissionRepository
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from app.infrastructure.database.prisma_client import prisma_client
from cuid2 import cuid_wrapper


class CreateRolePermissionUseCase:
    def __init__(self, repo: RolePermissionRepository):
        self.repo = repo

    async def execute(self, data: Dict[str, Any]) -> RolePermissionDTO:
        role_id = data.get("roleId")
        permission_id = data.get("permissionId")
        if not role_id or not permission_id:
            raise Exception("roleId and permissionId are required")

        role = await prisma_client.client.role.find_unique(where={"id": role_id})
        if not role:
            raise Exception(f"Role with id {role_id} not found")

        permission = await prisma_client.client.permission.find_unique(where={"id": permission_id})
        if not permission:
            raise Exception(f"Permission with id {permission_id} not found")
        # check uniqueness (roleId, permissionId)
        exists = await prisma_client.client.rolepermission.find_first(where={"roleId": role_id, "permissionId": permission_id})
        if exists:
            raise Exception(f"RolePermission for role {role_id} and permission {permission_id} already exists")
        generate_id = cuid_wrapper()
        rp = RolePermission(id=generate_id(), roleId=role_id, permissionId=permission_id, createdAt=datetime.now())
        created = await self.repo.create(rp)
        return RolePermissionDTO.from_entity(created)


class QueryRolePermissionUseCase:
    def __init__(self, repo: RolePermissionRepository):
        self.repo = repo

    async def execute(self, filters: Optional[Dict] = None, skip: int = 0, limit: int = 10) -> Tuple[List[RolePermissionDTO], int]:
        results, total = await self.repo.query(filters, skip, limit)
        return [RolePermissionDTO.from_entity(r) for r in results], total


class GetRolePermissionUseCase:
    def __init__(self, repo: RolePermissionRepository):
        self.repo = repo

    async def execute(self, id: str) -> Optional[RolePermissionDTO]:
        rp = await self.repo.get_by_id(id)
        return RolePermissionDTO.from_entity(rp) if rp else None


class UpdateRolePermissionUseCase:
    def __init__(self, repo: RolePermissionRepository):
        self.repo = repo

    async def execute(self, id: str, data: Dict[str, Any]) -> RolePermissionDTO:
        existing = await self.repo.get_by_id(id)
        if not existing:
            raise Exception(f"RolePermission with id {id} not found")
        existing.roleId = data.get("roleId", existing.roleId)
        existing.permissionId = data.get("permissionId", existing.permissionId)
        updated = await self.repo.update(existing)
        return RolePermissionDTO.from_entity(updated)


class DeleteRolePermissionUseCase:
    def __init__(self, repo: RolePermissionRepository):
        self.repo = repo

    async def execute(self, id: str) -> bool:
        return await self.repo.delete(id)
