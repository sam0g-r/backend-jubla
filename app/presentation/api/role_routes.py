from app.presentation.decorators.auth import require_roles
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from app.application.dto.role_dto import RoleDTO
from app.application.odm.role_odm import CreateRoleODM, UpdateRoleODM
from app.infrastructure.repositories.role_repository_impl import RoleRepositoryImpl
from app.application.use_cases.role_use_cases import (
    CreateRoleUseCase,
    QueryRoleUseCase,
    GetRoleUseCase,
    UpdateRoleUseCase,
    DeleteRoleUseCase,
)

router = APIRouter(prefix="/roles", tags=["roles"])


@router.post("/create", response_model=RoleDTO, status_code=status.HTTP_201_CREATED)
async def create_role(data: CreateRoleODM, _=Depends(require_roles('CoreEngineer'))):
    repo = RoleRepositoryImpl()
    use_case = CreateRoleUseCase(repo)
    try:
        created = await use_case.execute(data.dict())
        return created
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/get", response_model=List[RoleDTO])
async def list_roles(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1), name: Optional[str] = None, _=Depends(require_roles('CoreEngineer'))):
    filters = {}
    if name:
        filters["name"] = name
    repo = RoleRepositoryImpl()
    use_case = QueryRoleUseCase(repo)
    results, total = await use_case.execute(filters, skip, limit)
    return results


@router.get("/{id}", response_model=RoleDTO)
async def get_role(id: str, _=Depends(require_roles('CoreEngineer'))):
    repo = RoleRepositoryImpl()
    use_case = GetRoleUseCase(repo)
    result = await use_case.execute(id)
    if not result:
        raise HTTPException(status_code=404, detail="Role not found")
    return result


@router.put("/update/{id}", response_model=RoleDTO)
async def update_role(id: str, data: UpdateRoleODM, _=Depends(require_roles('CoreEngineer'))):
    repo = RoleRepositoryImpl()
    use_case = UpdateRoleUseCase(repo)
    try:
        updated = await use_case.execute(id, data.dict(exclude_unset=True))
        return updated
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(id: str, _=Depends(require_roles('CoreEngineer'))):
    repo = RoleRepositoryImpl()
    use_case = DeleteRoleUseCase(repo)
    success = await use_case.execute(id)
    if not success:
        raise HTTPException(status_code=404, detail="Role not found")
    return None
