from app.application.dto.user_role_dto import UserRoleDTO
from app.domain.entities.user_role import UserRole
from app.domain.repositories.user_role_repository import UserRoleRepository
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from app.infrastructure.database.prisma_client import prisma_client
from cuid2 import cuid_wrapper


class CreateUserRoleUseCase:
    def __init__(self, repo: UserRoleRepository):
        self.repo = repo

    async def execute(self, data: Dict[str, Any]) -> UserRoleDTO:
        # validate existence
        user_id = data.get("userId")
        role_id = data.get("roleId")
        if not user_id:
            raise Exception("userId is required")
        if not role_id:
            raise Exception("roleId is required")

        user = await prisma_client.client.user.find_unique(where={"id": user_id})
        if not user:
            raise Exception(f"User with id {user_id} not found")

        role = await prisma_client.client.role.find_unique(where={"id": role_id})
        if not role:
            raise Exception(f"Role with id {role_id} not found")

        event_id = data.get("eventId")
        if event_id:
            event = await prisma_client.client.event.find_unique(where={"id": event_id})
            if not event:
                raise Exception(f"Event with id {event_id} not found")

        generate_id = cuid_wrapper()
        user_role = UserRole(
            id=generate_id(),
            userId=user_id,
            roleId=role_id,
            eventId=event_id,
            assignedAt=datetime.now(),
        )
        created = await self.repo.create(user_role)
        return UserRoleDTO.from_entity(created)


class QueryUserRoleUseCase:
    def __init__(self, repo: UserRoleRepository):
        self.repo = repo

    async def execute(self, filters: Optional[Dict] = None, skip: int = 0, limit: int = 10) -> Tuple[List[UserRoleDTO], int]:
        results, total = await self.repo.query(filters, skip, limit)
        return [UserRoleDTO.from_entity(r) for r in results], total


class GetUserRoleUseCase:
    def __init__(self, repo: UserRoleRepository):
        self.repo = repo

    async def execute(self, id: str) -> Optional[UserRoleDTO]:
        ur = await self.repo.get_by_id(id)
        return UserRoleDTO.from_entity(ur) if ur else None


class UpdateUserRoleUseCase:
    def __init__(self, repo: UserRoleRepository):
        self.repo = repo

    async def execute(self, id: str, data: Dict[str, Any]) -> UserRoleDTO:
        existing = await self.repo.get_by_id(id)
        if not existing:
            raise Exception(f"UserRole with id {id} not found")
        # update fields
        existing.roleId = data.get("roleId", existing.roleId)
        existing.eventId = data.get("eventId", existing.eventId)
        updated = await self.repo.update(existing)
        return UserRoleDTO.from_entity(updated)


class DeleteUserRoleUseCase:
    def __init__(self, repo: UserRoleRepository):
        self.repo = repo

    async def execute(self, id: str) -> bool:
        return await self.repo.delete(id)
