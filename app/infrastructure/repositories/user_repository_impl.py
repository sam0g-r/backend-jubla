from typing import List, Optional
from datetime import datetime
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.database.prisma_client import prisma_client

class UserRepositoryImpl(UserRepository):
    """
    Implementación del repositorio de usuarios usando Prisma.
    """
    
    async def create(self, user: User) -> User:
        """Crear un nuevo usuario en la base de datos"""
        async with prisma_client as client:
            db_user = await client.client.user.create({
                'id': str(user.id),
                'email': user.email,
                'firstname': user.firstname,
                'lastname': user.lastname,
                'birthdate': user.birthdate,
                'phone': user.phone,
                'created_at': user.created_at or datetime.now(),
                'updated_at': user.updated_at or datetime.now()
            })
            
            return User(
                id=str(db_user.id),
                email=db_user.email,
                firstname=db_user.firstname,
                lastname=db_user.lastname,
                birthdate=db_user.birthdate,
                phone=db_user.phone,
                created_at=db_user.created_at,
                updated_at=db_user.updated_at
            )
    
    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Obtener usuario por ID"""
        async with prisma_client as client:
            db_user = await client.client.user.find_unique(
                where={'id': str(user_id)}
            )
            
            if not db_user:
                return None
                
            return User(
                id=str(db_user.id),
                email=db_user.email,
                firstname=db_user.firstname,
                lastname=db_user.lastname,
                birthdate=db_user.birthdate,
                phone=db_user.phone,
                created_at=db_user.created_at,
                updated_at=db_user.updated_at
            )
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Obtener usuario por email"""
        async with prisma_client as client:
            db_user = await client.client.user.find_unique(
                where={'email': email}
            )
            
            if not db_user:
                return None
                
            return User(
                id=str(db_user.id),
                email=db_user.email,
                firstname=db_user.firstname,
                lastname=db_user.lastname,
                birthdate=db_user.birthdate,
                phone=db_user.phone,
                created_at=db_user.created_at,
                updated_at=db_user.updated_at
            )
    
    async def update(self, user: User) -> User:
        """Actualizar usuario"""
        async with prisma_client as client:
            db_user = await client.client.user.update(
                where={'id': str(user.id)},
                data={
                    'email': user.email,
                    'firstname': user.firstname,
                    'lastname': user.lastname,
                    'birthdate': user.birthdate,
                    'phone': user.phone,
                    'updated_at': datetime.now()
                }
            )
            
            return User(
                id=str(db_user.id),
                email=db_user.email,
                firstname=db_user.firstname,
                lastname=db_user.lastname,
                birthdate=db_user.birthdate,
                phone=db_user.phone,
                created_at=db_user.created_at,
                updated_at=db_user.updated_at
            )
    
    async def delete(self, user_id: str) -> bool:
        """Eliminar usuario"""
        async with prisma_client as client:
            try:
                await client.client.user.delete(
                    where={'id': str(user_id)}
                )
                return True
            except Exception:
                return False
    
    async def list_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Listar todos los usuarios con paginación"""
        async with prisma_client as client:
            db_users = await client.client.user.find_many(
                skip=skip,
                take=limit,
                order=[{'created_at': 'desc'}]
            )
            
            return [
                User(
                    id=str(db_user.id),
                    email=db_user.email,
                    firstname=db_user.firstname,
                    lastname=db_user.lastname,
                    birthdate=db_user.birthdate,
                    phone=db_user.phone,
                    created_at=db_user.created_at,
                    updated_at=db_user.updated_at
                )
                for db_user in db_users
            ]
    
    async def exists_by_email(self, email: str) -> bool:
        """Verificar si existe un usuario con el email dado"""
        async with prisma_client as client:
            user = await client.client.user.find_unique(
                where={'email': email}
            )
            return user is not None 