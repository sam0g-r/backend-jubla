from app.presentation.decorators.auth import require_roles
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from app.application.dto.permission_dto import PermissionDTO
from app.application.odm.permission_odm import CreatePermissionODM, UpdatePermissionODM
from app.infrastructure.repositories.permission_repository_impl import PermissionRepositoryImpl
from app.application.use_cases.permission_use_cases import (
    CreatePermissionUseCase,
    QueryPermissionUseCase,
    GetPermissionUseCase,
    UpdatePermissionUseCase,
    DeletePermissionUseCase,
)

router = APIRouter(prefix="/permissions", tags=["permissions"])


@router.post("/create", response_model=PermissionDTO, status_code=status.HTTP_201_CREATED)
async def create_permission(data: CreatePermissionODM, _=Depends(require_roles('CoreEngineer'))):
    repo = PermissionRepositoryImpl()
    use_case = CreatePermissionUseCase(repo)
    try:
        created = await use_case.execute(data.dict())
        return created
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/get", response_model=List[PermissionDTO])
async def list_permissions(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1), module: Optional[str] = None, action: Optional[str] = None, _=Depends(require_roles('CoreEngineer'))):
    filters = {}
    if module:
        filters["module"] = module
    if action:
        filters["action"] = action
    repo = PermissionRepositoryImpl()
    use_case = QueryPermissionUseCase(repo)
    results, total = await use_case.execute(filters, skip, limit)
    return results


@router.get("/{id}", response_model=PermissionDTO)
async def get_permission(id: str, _=Depends(require_roles('CoreEngineer'))):
    repo = PermissionRepositoryImpl()
    use_case = GetPermissionUseCase(repo)
    result = await use_case.execute(id)
    if not result:
        raise HTTPException(status_code=404, detail="Permission not found")
    return result


@router.put("/update/{id}", response_model=PermissionDTO)
async def update_permission(id: str, data: UpdatePermissionODM, _=Depends(require_roles('CoreEngineer'))):
    repo = PermissionRepositoryImpl()
    use_case = UpdatePermissionUseCase(repo)
    try:
        updated = await use_case.execute(id, data.dict(exclude_unset=True))
        return updated
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_permission(id: str, _=Depends(require_roles('CoreEngineer'))):
    repo = PermissionRepositoryImpl()
    use_case = DeletePermissionUseCase(repo)
    success = await use_case.execute(id)
    if not success:
        raise HTTPException(status_code=404, detail="Permission not found")
    return None
