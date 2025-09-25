from app.domain.entities.role import Role
from app.domain.repositories.role_repository import RoleRepository
from app.infrastructure.database.prisma_client import prisma_client
from typing import Dict, List, Optional


class RoleRepositoryImpl(RoleRepository):
    def _to_entity(self, db_obj) -> Role:
        return Role(
            id=db_obj.id,
            name=db_obj.name,
            description=db_obj.description,
            createdAt=db_obj.createdAt,
            updatedAt=getattr(db_obj, "updatedAt", None),
        )

    async def create(self, r: Role) -> Role:
        # Remove None values and let DB defaults (createdAt/updatedAt) be applied
        data = {k: v for k, v in r.__dict__.items() if v is not None}
        db = await prisma_client.client.role.create(data=data)
        return self._to_entity(db)

    async def get_by_id(self, id: str) -> Optional[Role]:
        db = await prisma_client.client.role.find_unique(where={"id": id})
        return self._to_entity(db) if db else None

    async def get_by_ids(self, ids: List[str]) -> List[Role]:
        if not ids:
            return []
        db_items = await prisma_client.client.role.find_many(where={"id": {"in": ids}})
        return [self._to_entity(i) for i in db_items]

    async def update(self, r: Role) -> Role:
        data = r.__dict__.copy()
        id = data.pop("id")
        # Remove None values so we don't send nulls for DB-managed fields
        data = {k: v for k, v in data.items() if v is not None}
        db = await prisma_client.client.role.update(where={"id": id}, data=data)
        return self._to_entity(db)

    async def delete(self, id: str) -> bool:
        await prisma_client.client.role.delete(where={"id": id})
        return True

    async def query(self, filters: Optional[Dict] = None, skip: int = 0, limit: int = 10):
        filters = filters or {}
        total = await prisma_client.client.role.count(where=filters)
        db_items = await prisma_client.client.role.find_many(where=filters, skip=skip, take=limit, order={"createdAt": "desc"})
        return [self._to_entity(i) for i in db_items], total
