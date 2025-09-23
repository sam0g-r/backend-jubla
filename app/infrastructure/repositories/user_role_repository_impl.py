from app.domain.entities.user_role import UserRole
from app.domain.repositories.user_role_repository import UserRoleRepository
from app.infrastructure.database.prisma_client import prisma_client
from typing import Dict, List, Optional


class UserRoleRepositoryImpl(UserRoleRepository):
    def _to_entity(self, db_obj) -> UserRole:
        return UserRole(
            id=db_obj.id,
            userId=db_obj.userId,
            roleId=db_obj.roleId,
            eventId=getattr(db_obj, "eventId", None),
            assignedAt=db_obj.assignedAt,
        )

    async def create(self, user_role: UserRole) -> UserRole:
        db = await prisma_client.client.userrole.create(data=user_role.__dict__)
        return self._to_entity(db)

    async def get_by_id(self, id: str) -> Optional[UserRole]:
        db = await prisma_client.client.userrole.find_unique(where={"id": id})
        return self._to_entity(db) if db else None

    async def update(self, user_role: UserRole) -> UserRole:
        data = user_role.__dict__.copy()
        id = data.pop("id")
        db = await prisma_client.client.userrole.update(where={"id": id}, data=data)
        return self._to_entity(db)

    async def delete(self, id: str) -> bool:
        await prisma_client.client.userrole.delete(where={"id": id})
        return True

    async def query(self, filters: Optional[Dict] = None, skip: int = 0, limit: int = 10):
        filters = filters or {}
        total = await prisma_client.client.userrole.count(where=filters)
        db_items = await prisma_client.client.userrole.find_many(where=filters, skip=skip, take=limit, order={"assignedAt": "desc"})
        return [self._to_entity(i) for i in db_items], total
