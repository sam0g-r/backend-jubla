from typing import List, Optional
from datetime import datetime
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.database.prisma_client import prisma_client

class UserRepositoryImpl(UserRepository):
    """
    Implementación del repositorio de usuarios usando Prisma.
    """

    def _to_entity(self, db_user) -> User:
        return User(
            id=db_user.id,
            email=db_user.email,
            firstname=db_user.firstname,
            lastname=db_user.lastname,
            birthdate=db_user.birthdate,
            country_id=db_user.country_id,
            state_id=db_user.state_id,
            phone=db_user.phone,
            password=db_user.password,
            church=db_user.church,
            is_active=db_user.is_active,
            is_verified=db_user.is_verified,
            deleted_at=db_user.deleted_at,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
        )

    async def create(self, user: User) -> User:
        """Crear un nuevo usuario en la base de datos"""
        async with prisma_client as client:
            db_user = await client.user.create(
                data={
                    "email": user.email,
                    "firstname": user.firstname,
                    "lastname": user.lastname,
                    "birthdate": user.birthdate,
                    "country_id": user.country_id,
                    "state_id": user.state_id,
                    "phone": user.phone,
                    "password": user.password,
                    "church": user.church,
                }
            )
            return self._to_entity(db_user)

    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Obtener usuario por ID"""
        async with prisma_client as client:
            db_user = await client.user.find_unique(where={"id": user_id})
            if db_user:
                return self._to_entity(db_user)
            return None

    async def get_by_email(self, email: str) -> Optional[User]:
        """Obtener usuario por email"""
        async with prisma_client as client:
            db_user = await client.user.find_unique(where={"email": email})
            if db_user:
                return self._to_entity(db_user)
            return None

    async def update(self, user: User) -> User:
        """Actualizar usuario"""
        async with prisma_client as client:
            db_user = await client.user.update(
                where={"id": user.id},
                data={
                    "firstname": user.firstname,
                    "lastname": user.lastname,
                    "phone": user.phone,
                    "country_id": user.country_id,
                    "state_id": user.state_id,
                    "church": user.church,
                    "is_active": user.is_active,
                    "is_verified": user.is_verified,
                },
            )
            return self._to_entity(db_user)

    async def delete(self, user_id: str) -> bool:
        """Eliminar usuario"""
        async with prisma_client as client:
            try:
                await client.user.delete(where={"id": user_id})
                return True
            except Exception:
                return False

    async def list_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Listar todos los usuarios con paginación"""
        async with prisma_client as client:
            db_users = await client.user.find_many(
                skip=skip, take=limit, order=[{"created_at": "desc"}]
            )
            return [self._to_entity(db_user) for db_user in db_users]

    async def exists_by_email(self, email: str) -> bool:
        """Verificar si existe un usuario con el email dado"""
        async with prisma_client as client:
            user = await client.user.find_unique(where={"email": email})
            return user is not None
