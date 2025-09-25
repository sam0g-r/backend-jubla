from app.application.dto.user_role_dto import UserRoleDTO
from app.presentation.decorators.auth import require_roles
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from app.domain.entities.user_role import UserRole
from app.application.odm.user_role_odm import CreateUserRoleODM, UpdateUserRoleODM
from app.infrastructure.repositories.user_role_repository_impl import UserRoleRepositoryImpl
from app.application.use_cases.user_role_use_cases import (
    CreateUserRoleUseCase,
    QueryUserRoleUseCase,
    GetUserRoleUseCase,
    UpdateUserRoleUseCase,
    DeleteUserRoleUseCase,
)

router = APIRouter(prefix="/user-roles", tags=["user-roles"])


@router.post("/create", response_model=UserRoleDTO, status_code=status.HTTP_201_CREATED)
async def create_user_role(
    data: CreateUserRoleODM,
    _=Depends(require_roles('CoreEngineer')),
):
    repo = UserRoleRepositoryImpl()
    use_case = CreateUserRoleUseCase(repo)
    try:
        payload = data.dict()
        # assume authenticated user provided elsewhere; payload must include userId
        created = await use_case.execute(payload)
        return created
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/get", response_model=List[UserRoleDTO])
async def list_user_roles(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    userId: Optional[str] = None,
    _=Depends(require_roles('CoreEngineer')),
):
    filters = {}
    if userId:
        filters["userId"] = userId
    repo = UserRoleRepositoryImpl()
    use_case = QueryUserRoleUseCase(repo)
    results, total = await use_case.execute(filters, skip, limit)
    return results

@router.get("/{id}", response_model=UserRoleDTO)
async def get_user_role(id: str, _=Depends(require_roles('CoreEngineer'))):
    repo = UserRoleRepositoryImpl()
    use_case = GetUserRoleUseCase(repo)
    result = await use_case.execute(id)
    if not result:
        raise HTTPException(status_code=404, detail="UserRole not found")
    return result


@router.put("/update/{id}", response_model=UserRoleDTO)
async def update_user_role(id: str, data: UpdateUserRoleODM, _=Depends(require_roles('CoreEngineer'))):
    repo = UserRoleRepositoryImpl()
    use_case = UpdateUserRoleUseCase(repo)
    try:
        updated = await use_case.execute(id, data.dict(exclude_unset=True))
        return updated
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_role(id: str, _=Depends(require_roles('CoreEngineer'))):
    repo = UserRoleRepositoryImpl()
    use_case = DeleteUserRoleUseCase(repo)
    success = await use_case.execute(id)
    if not success:
        raise HTTPException(status_code=404, detail="UserRole not found")
    return None
