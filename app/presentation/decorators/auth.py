from fastapi import Depends, HTTPException
from supertokens_python.recipe.session.framework.fastapi import verify_session
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.domain.repositories.user_repository import UserRepository


def get_user_repo() -> UserRepository:
    return UserRepositoryImpl()


def get_current_session(session: dict = Depends(verify_session())):
    # verify_session returns a SessionContainer but FastAPI dependency wiring returns it directly
    return session


def require_roles(*required_roles: str):
    """Ensure that the current session user has at least one of the required roles."""
    async def _dependency(
        session = Depends(verify_session()),
        user_repo: UserRepository = Depends(get_user_repo),
    ):
        # Try from token payload first
        roles = _roles_from_token(session)
        if roles and set(required_roles) & set(roles):
            return session  # devolver la session para seguir usándola en el endpoint

        # Fallback: check from DB
        user_id = session.get_user_id()
        if not user_id:
            raise HTTPException(status_code=401, detail="Unauthenticated")

        user = await user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        user_roles = [ur.role.name for ur in getattr(user, "roles", [])]
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
