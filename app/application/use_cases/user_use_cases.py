from typing import Optional, List
from uuid import UUID
from datetime import datetime
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.application.dto.user_dto import CreateUserDTO, UpdateUserDTO, UserResponseDTO
from app.infrastructure.database.prisma_client import with_prisma
from app.shared.exceptions.user_exceptions import InvalidCredentialsError, UserAlreadyExistsError, UserNotFoundError
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserUseCases:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    async def create_user(self, user_data: CreateUserDTO) -> UserResponseDTO:
        # Verificar si el usuario ya existe
        existing_user = await self.user_repository.get_by_email(user_data.email)
        if existing_user:
            raise UserAlreadyExistsError(f"User with email {user_data.email} already exists")
        
        # Hash de la contraseña
        hashed_password = pwd_context.hash(user_data.password)
        
        # Crear entidad de usuario
        user = User(
            id=UUID.uuid4(),
            firstname=user_data.firstname,
            lastname=user_data.lastname,
            email=user_data.email,
            birthdate=user_data.birthdate,
            phone=user_data.phone,
            country=user_data.country,
            state=user_data.state,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Guardar en repositorio
        created_user = await self.user_repository.create(user)
        return UserResponseDTO.from_entity(created_user)
    
    async def get_user_by_id(self, user_id: UUID) -> Optional[UserResponseDTO]:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User with id {user_id} not found")
        return UserResponseDTO.from_entity(user)
    
    @with_prisma
    async def get_user_by_email(self, email: str) -> Optional[UserResponseDTO]:
        user = await self.user_repository.get_by_email(email)
        if not user:
            raise UserNotFoundError(f"User with email {email} not found")
        return UserResponseDTO.from_entity(user)
    
    async def update_user(self, user_id: UUID, user_data: UpdateUserDTO) -> UserResponseDTO:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User with id {user_id} not found")
        
        # Actualizar campos
        if user_data.firstname is not None:
            user.firstname = user_data.firstname
        if user_data.lastname is not None:
            user.lastname = user_data.lastname
        if user_data.phone is not None:
            user.phone = user_data.phone
        if user_data.country is not None:
            user.country = user_data.country
        if user_data.state is not None:
            user.state = user_data.state
        
        user.updated_at = datetime.utcnow()
        
        updated_user = await self.user_repository.update(user)
        return UserResponseDTO.from_entity(updated_user)
    
    async def delete_user(self, user_id: UUID) -> bool:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User with id {user_id} not found")
        
        return await self.user_repository.delete(user_id)
    
    async def list_users(self, skip: int = 0, limit: int = 100) -> List[UserResponseDTO]:
        users = await self.user_repository.list_all(skip=skip, limit=limit)
        return [UserResponseDTO.from_entity(user) for user in users]
    
    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    async def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password) 
    
    async def authenticate_user(self, email: str, password: str):
        user = await self.user_repository.get_by_email(email)
        if not user or not await self.verify_password(password, user.hashed_password):
            raise InvalidCredentialsError("Invalid credentials")
        return user
