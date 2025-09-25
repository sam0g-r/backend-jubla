from app.domain.repositories.role_repository import RoleRepository
from app.domain.repositories.user_role_repository import UserRoleRepository
from app.infrastructure.repositories.role_repository_impl import RoleRepositoryImpl
from app.infrastructure.repositories.user_role_repository_impl import UserRoleRepositoryImpl
from fastapi import Depends, HTTPException
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.emailpassword.asyncio import get_user
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.domain.repositories.user_repository import UserRepository


def get_user_repo() -> UserRepository:
    return UserRepositoryImpl()

def get_user_role_repo() -> UserRoleRepository:
    return UserRoleRepositoryImpl()

def get_role_repo() -> RoleRepository:
    return RoleRepositoryImpl()

def get_current_session(session: dict = Depends(verify_session())):
    # verify_session returns a SessionContainer but FastAPI dependency wiring returns it directly
    return session


def require_roles(*required_roles: str):
    """Ensure that the current session user has at least one of the required roles."""
    async def _dependency(
        session = Depends(verify_session()),
        user_repo: UserRepository = Depends(get_user_repo),
        user_role_repo: UserRoleRepository = Depends(get_user_role_repo),
        role_repo: RoleRepository = Depends(get_role_repo)
    ):
        roles = _roles_from_token(session)
        if roles and set(required_roles) & set(roles):
            return session

        supertokens_user = await get_user(session.get_user_id())
        if supertokens_user is None:
            raise HTTPException(status_code=401, detail="Unauthenticated")

        user = await user_repo.get_by_email(supertokens_user.emails[0])
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        user_roles_ids, _ = await user_role_repo.query({'userId': user.id})
        role_ids = [ur.roleId for ur in user_roles_ids]

        roles = await role_repo.get_by_ids(role_ids)
        user_roles = tuple(role.name for role in roles)

        if set(required_roles) & set(user_roles):
            return session

        raise HTTPException(status_code=403, detail="Insufficient role")

    return _dependency


def _roles_from_token(session) -> list[str] | None:
    try:
        payload = session.get_access_token_payload()
        roles = payload.get("roles") or payload.get("role")
        if roles:
            return [roles] if isinstance(roles, str) else list(roles)
    except Exception:
        pass
    return None
