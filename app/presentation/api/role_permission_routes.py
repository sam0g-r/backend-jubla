from app.presentation.decorators.auth import require_roles
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from app.domain.entities.role_permission import RolePermission
from app.application.odm.role_permission_odm import CreateRolePermissionODM, UpdateRolePermissionODM
from app.infrastructure.repositories.role_permission_repository_impl import RolePermissionRepositoryImpl
from app.application.use_cases.role_permission_use_cases import (
    CreateRolePermissionUseCase,
    QueryRolePermissionUseCase,
    GetRolePermissionUseCase,
    UpdateRolePermissionUseCase,
    DeleteRolePermissionUseCase,
)

router = APIRouter(prefix="/role-permissions", tags=["role-permissions"])


@router.post("/create", response_model=RolePermission, status_code=status.HTTP_201_CREATED)
async def create_role_permission(data: CreateRolePermissionODM, _=Depends(require_roles('CoreEngineer'))):
    repo = RolePermissionRepositoryImpl()
    use_case = CreateRolePermissionUseCase(repo)
    try:
        created = await use_case.execute(data.dict())
        return created
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/get", response_model=List[RolePermission])
async def list_role_permissions(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1), roleId: Optional[str] = None, _=Depends(require_roles('CoreEngineer'))):
    filters = {}
    if roleId:
        filters["roleId"] = roleId
    repo = RolePermissionRepositoryImpl()
    use_case = QueryRolePermissionUseCase(repo)
    results, total = await use_case.execute(filters, skip, limit)
    return results


@router.get("/{id}", response_model=RolePermission)
async def get_role_permission(id: str, _=Depends(require_roles('CoreEngineer'))):
    repo = RolePermissionRepositoryImpl()
    use_case = GetRolePermissionUseCase(repo)
    result = await use_case.execute(id)
    if not result:
        raise HTTPException(status_code=404, detail="RolePermission not found")
    return result


@router.put("/update/{id}", response_model=RolePermission)
async def update_role_permission(id: str, data: UpdateRolePermissionODM, _=Depends(require_roles('CoreEngineer'))):
    repo = RolePermissionRepositoryImpl()
    use_case = UpdateRolePermissionUseCase(repo)
    try:
        updated = await use_case.execute(id, data.dict(exclude_unset=True))
        return updated
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role_permission(id: str, _=Depends(require_roles('CoreEngineer'))):
    repo = RolePermissionRepositoryImpl()
    use_case = DeleteRolePermissionUseCase(repo)
    success = await use_case.execute(id)
    if not success:
        raise HTTPException(status_code=404, detail="RolePermission not found")
    return None
