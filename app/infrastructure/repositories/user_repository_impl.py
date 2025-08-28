from typing import List, Optional
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
            countryId=db_user.countryId,
            stateId=db_user.stateId,
            phone=db_user.phone,
            password=db_user.password,
            church=db_user.church,
            isActive=db_user.isActive,
            isVerified=db_user.isVerified,
            deletedAt=db_user.deletedAt,
            createdAt=db_user.createdAt,
            updatedAt=db_user.updatedAt,
        )

    async def create(self, user: User) -> User:
        """Crear un nuevo usuario en la base de datos"""
        db_user = await prisma_client.client.user.create(
            data={
                "email": user.email,
                "firstname": user.firstname,
                "lastname": user.lastname,
                "birthdate": user.birthdate,
                "countryId": user.countryId,
                "stateId": user.stateId,
                "phone": user.phone,
                "password": user.password,
                "church": user.church,
            }
        )
        return self._to_entity(db_user)

    async def get_by_id(self, userId: str) -> Optional[User]:
        """Obtener usuario por ID"""
        db_user = await prisma_client.client.user.find_unique(where={"id": userId})
        if db_user:
            return self._to_entity(db_user)
        return None

    async def get_by_email(self, email: str) -> Optional[User]:
        """Obtener usuario por email"""
        db_user = await prisma_client.client.user.find_unique(where={"email": email})
        if db_user:
            return self._to_entity(db_user)
        return None

    async def update(self, user: User) -> User:
        """Actualizar usuario"""
        db_user = await prisma_client.client.user.update(
            where={"id": user.id},
            data={
                "firstname": user.firstname,
                "lastname": user.lastname,
                "phone": user.phone,
                "countryId": user.countryId,
                "stateId": user.stateId,
                "church": user.church,
                "isActive": user.isActive,
                "isVerified": user.isVerified,
            },
        )
        return self._to_entity(db_user)

    async def delete(self, userId: str) -> bool:
        """Eliminar usuario"""
        try:
            await prisma_client.client.user.delete(where={"id": userId})
            return True
        except Exception:
            return False

    async def list_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Listar todos los usuarios con paginación"""
        db_users = await prisma_client.client.user.find_many(
            skip=skip, take=limit, order=[{"createdAt": "desc"}]
        )
        return [self._to_entity(db_user) for db_user in db_users]

    async def exists_by_email(self, email: str) -> bool:
        """Verificar si existe un usuario con el email dado"""
        user = await prisma_client.client.user.find_unique(where={"email": email})
        return user is not None
