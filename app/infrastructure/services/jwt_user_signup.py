from passlib.context import CryptContext
from app.domain.services.user_singup import UserSignUp
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.domain.entities.user import User
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class JwtUserSignUp(UserSignUp):
    """Service to register users directly in the local database and hash passwords.

    The caller sometimes provides an already-hashed password (the use cases hash it).
    To avoid double-hashing we detect bcrypt hashes (they start with $2) and skip hashing.
    """
    def __init__(self, user_repo: Optional[UserRepositoryImpl] = None):
        self.user_repo = user_repo or UserRepositoryImpl()

    async def register(self, email: str, password: str):
        # check existence
        exists = await self.user_repo.exists_by_email(email)
        if exists:
            raise Exception("User already exists")
        # In the JWT flow we don't create a separate auth record here because
        # the application use case is responsible for creating the full User
        # in the database (see UserUseCases.create_user). This method only
        # validates the email isn't already taken and returns.
        return None
