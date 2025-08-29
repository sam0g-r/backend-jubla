from app.presentation.decorators.auth import require_roles
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.application.use_cases.user_use_cases import UserUseCases
from app.application.dto.user_dto import UserResponseDTO
from app.application.odm.user_odm import UpdateUserODM
from app.presentation.dependencies import get_user_use_cases
from app.shared.exceptions.user_exceptions import UserNotFoundError
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer


router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserResponseDTO)
async def get_current_user(
    user_use_cases: UserUseCases = Depends(get_user_use_cases),
    _=Depends(require_roles('OnBoarding, Financing, Admin, Participant, ParticipantManager, CoreEngineer')),
    session: SessionContainer = Depends(verify_session())
):
    try:
        userId = session.get_userId()
        user = await user_use_cases.get_user_by_id(userId)
        return user
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.get("/get/{userId}", response_model=UserResponseDTO)
async def get_user(
    userId: str,
    user_use_cases: UserUseCases = Depends(get_user_use_cases),
    _=Depends(require_roles('OnBoarding, Admin, ParticipantManager, CoreEngineer')),
):
    try:
        user = await user_use_cases.get_user_by_id(userId)
        return user
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.get("/get-all", response_model=List[UserResponseDTO])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    user_use_cases: UserUseCases = Depends(get_user_use_cases),
    _=Depends(require_roles('OnBoarding, Admin, ParticipantManager, CoreEngineer')),
):
    users = await user_use_cases.list_users(skip=skip, limit=limit)
    return users

@router.put("/update/{userId}", response_model=UserResponseDTO)
async def update_user(
    userId: str,
    user_data: UpdateUserODM,
    user_use_cases: UserUseCases = Depends(get_user_use_cases),
    _=Depends(require_roles('Admin, Participant, ParticipantManager, CoreEngineer')),
):
    try:
        user = await user_use_cases.update_user(userId, user_data.dict())
        return user
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.delete("/delete/{userId}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    userId: str,
    user_use_cases: UserUseCases = Depends(get_user_use_cases),
    _=Depends(require_roles('ParticipantManager, CoreEngineer')),
):
    try:
        await user_use_cases.delete_user(userId)
        return None
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
