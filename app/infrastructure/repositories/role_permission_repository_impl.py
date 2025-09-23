from app.domain.entities.role_permission import RolePermission
from app.domain.repositories.role_permission_repository import RolePermissionRepository
from app.infrastructure.database.prisma_client import prisma_client
from typing import Dict, List, Optional


class RolePermissionRepositoryImpl(RolePermissionRepository):
    def _to_entity(self, db_obj) -> RolePermission:
        return RolePermission(
            id=db_obj.id,
            roleId=db_obj.roleId,
            permissionId=db_obj.permissionId,
            createdAt=db_obj.createdAt,
        )

    async def create(self, rp: RolePermission) -> RolePermission:
        db = await prisma_client.client.rolepermission.create(data=rp.__dict__)
        return self._to_entity(db)

    async def get_by_id(self, id: str) -> Optional[RolePermission]:
        db = await prisma_client.client.rolepermission.find_unique(where={"id": id})
        return self._to_entity(db) if db else None

    async def update(self, rp: RolePermission) -> RolePermission:
        data = rp.__dict__.copy()
        id = data.pop("id")
        db = await prisma_client.client.rolepermission.update(where={"id": id}, data=data)
        return self._to_entity(db)

    async def delete(self, id: str) -> bool:
        await prisma_client.client.rolepermission.delete(where={"id": id})
        return True

    async def query(self, filters: Optional[Dict] = None, skip: int = 0, limit: int = 10):
        filters = filters or {}
        total = await prisma_client.client.rolepermission.count(where=filters)
        db_items = await prisma_client.client.rolepermission.find_many(where=filters, skip=skip, take=limit, order={"createdAt": "desc"})
        return [self._to_entity(i) for i in db_items], total
