from app.domain.repositories.role_repository import RoleRepository
from app.domain.repositories.user_role_repository import UserRoleRepository
from app.infrastructure.repositories.role_repository_impl import RoleRepositoryImpl
from app.infrastructure.repositories.user_role_repository_impl import UserRoleRepositoryImpl
from fastapi import Depends, HTTPException, Request
from app.presentation.auth.jwt_utils import verify_access_token
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.domain.repositories.user_repository import UserRepository
from typing import Optional, Iterable, List, Union


def get_user_repo() -> UserRepository:
    return UserRepositoryImpl()

def get_user_role_repo() -> UserRoleRepository:
    return UserRoleRepositoryImpl()

def get_role_repo() -> RoleRepository:
    return RoleRepositoryImpl()


def _get_token_from_header(request: Request) -> Optional[str]:
    auth: str | None = request.headers.get('authorization')
    if not auth:
        return None
    parts = auth.split()
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        return None
    return parts[1]


async def get_current_session(request: Request):
    token = _get_token_from_header(request)
    if not token:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    try:
        payload = verify_access_token(token)
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")


def _normalize_roles(raw: Union[str, Iterable[str], None]) -> List[str]:
    """Normalize role input into a flat list of role strings.

    Accepts:
      - 'A, B' (string with commas)
      - ['A, B', 'C']
      - ('A','B') or ['A','B']
      - None -> []
    """
    if not raw:
        return []
    out: List[str] = []
    if isinstance(raw, str):
        out.extend([r.strip() for r in raw.split(',') if r.strip()])
        return out
    # Iterable (list/tuple/set) of strings
    try:
        for el in raw:  # type: ignore
            if isinstance(el, str):
                out.extend([r.strip() for r in el.split(',') if r.strip()])
    except TypeError:
        # not iterable
        return []
    return out


def require_roles(*required_roles: str):
    """Ensure that the current session user has at least one of the required roles."""
    async def _dependency(
        session_payload = Depends(get_current_session),
        user_repo: UserRepository = Depends(get_user_repo),
        user_role_repo: UserRoleRepository = Depends(get_user_role_repo),
        role_repo: RoleRepository = Depends(get_role_repo)
    ):
        # Normalize required roles passed to the decorator
        normalized_required = _normalize_roles(required_roles)

        # Try to get roles from token payload first
        roles = None
        if isinstance(session_payload, dict):
            roles = session_payload.get('roles') or session_payload.get('role')
            # token might include a list or a comma-separated string
        normalized_roles = _normalize_roles(roles)

        if normalized_roles and set(normalized_required) & set(normalized_roles):
            return session_payload

        # Fall back to DB lookup by email or user_id in token
        user_email = None
        user_id = None
        if isinstance(session_payload, dict):
            user_email = session_payload.get('email')
            user_id = session_payload.get('sub') or session_payload.get('user_id')

        user = None
        if user_email:
            user = await user_repo.get_by_email(user_email)
        elif user_id:
            user = await user_repo.get_by_id(user_id)

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        user_roles_ids, _ = await user_role_repo.query({'userId': user.id})
        role_ids = [ur.roleId for ur in user_roles_ids]

        roles_objs = await role_repo.get_by_ids(role_ids)
        user_roles = tuple(role.name for role in roles_objs)

        # Normalize DB roles too (should already be single names but safe to normalize)
        normalized_user_roles = _normalize_roles(user_roles)

        # Debug prints (optional)
        # print(set(normalized_required))
        # print(set(normalized_user_roles))
        if set(normalized_required) & set(normalized_user_roles):
            return session_payload

        raise HTTPException(status_code=403, detail="Insufficient role")

    return _dependency
