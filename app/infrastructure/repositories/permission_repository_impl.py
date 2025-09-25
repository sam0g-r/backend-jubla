from app.domain.entities.permission import Permission
from app.domain.repositories.permission_repository import PermissionRepository
from app.infrastructure.database.prisma_client import prisma_client
from typing import Dict, List, Optional


class PermissionRepositoryImpl(PermissionRepository):
    def _to_entity(self, db_obj) -> Permission:
        return Permission(
            id=db_obj.id,
            module=db_obj.module,
            action=db_obj.action,
            description=db_obj.description,
            createdAt=db_obj.createdAt,
            updatedAt=getattr(db_obj, "updatedAt", None),
        )

    async def create(self, p: Permission) -> Permission:
        data = {k: v for k, v in p.__dict__.items() if v is not None}
        db = await prisma_client.client.permission.create(data=data)
        return self._to_entity(db)

    async def get_by_id(self, id: str) -> Optional[Permission]:
        db = await prisma_client.client.permission.find_unique(where={"id": id})
        return self._to_entity(db) if db else None

    async def update(self, p: Permission) -> Permission:
        data = p.__dict__.copy()
        id = data.pop("id")
        data = {k: v for k, v in data.items() if v is not None}
        db = await prisma_client.client.permission.update(where={"id": id}, data=data)
        return self._to_entity(db)

    async def delete(self, id: str) -> bool:
        await prisma_client.client.permission.delete(where={"id": id})
        return True

    async def query(self, filters: Optional[Dict] = None, skip: int = 0, limit: int = 10):
        filters = filters or {}
        total = await prisma_client.client.permission.count(where=filters)
        db_items = await prisma_client.client.permission.find_many(where=filters, skip=skip, take=limit, order={"createdAt": "desc"})
        return [self._to_entity(i) for i in db_items], total
