from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.application.use_cases.user_use_cases import UserUseCases
from app.application.dto.user_dto import CreateUserDTO, UpdateUserDTO, UserResponseDTO
from app.presentation.dependencies import get_user_use_cases
from app.shared.exceptions.user_exceptions import UserAlreadyExistsError, UserNotFoundError


router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}", response_model=UserResponseDTO)
async def get_user(
    user_id: str,
    user_use_cases: UserUseCases = Depends(get_user_use_cases)
):
    try:
        user = await user_use_cases.get_user_by_id(user_id)
        return user
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.get("/", response_model=List[UserResponseDTO])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    user_use_cases: UserUseCases = Depends(get_user_use_cases)
):
    users = await user_use_cases.list_users(skip=skip, limit=limit)
    return users

@router.put("/{user_id}", response_model=UserResponseDTO)
async def update_user(
    user_id: str,
    user_data: UpdateUserDTO,
    user_use_cases: UserUseCases = Depends(get_user_use_cases)
):
    try:
        user = await user_use_cases.update_user(user_id, user_data)
        return user
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    user_use_cases: UserUseCases = Depends(get_user_use_cases)
):
    try:
        await user_use_cases.delete_user(user_id)
        return None
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        ) 
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.application.use_cases.user_use_cases import UserUseCases
from app.application.dto.user_dto import CreateUserDTO, UpdateUserDTO, UserResponseDTO
from app.presentation.dependencies import get_user_use_cases
from app.shared.exceptions.user_exceptions import UserAlreadyExistsError, UserNotFoundError
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserResponseDTO)
async def get_current_user(
    session: SessionContainer = Depends(verify_session()),
    user_use_cases: UserUseCases = Depends(get_user_use_cases)
):
    try:
        user_id = session.get_user_id()
        user = await user_use_cases.get_user_by_id(user_id)
        return user
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.get("/{user_id}", response_model=UserResponseDTO)
async def get_user(
    user_id: str,
    user_use_cases: UserUseCases = Depends(get_user_use_cases),
    session: SessionContainer = Depends(verify_session())
):
    try:
        user = await user_use_cases.get_user_by_id(user_id)
        return user
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.get("/", response_model=List[UserResponseDTO])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    user_use_cases: UserUseCases = Depends(get_user_use_cases),
    session: SessionContainer = Depends(verify_session())
):
    users = await user_use_cases.list_users(skip=skip, limit=limit)
    return users

@router.put("/{user_id}", response_model=UserResponseDTO)
async def update_user(
    user_id: str,
    user_data: UpdateUserDTO,
    user_use_cases: UserUseCases = Depends(get_user_use_cases),
    session: SessionContainer = Depends(verify_session())
):
    try:
        user = await user_use_cases.update_user(user_id, user_data)
        return user
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    user_use_cases: UserUseCases = Depends(get_user_use_cases),
    session: SessionContainer = Depends(verify_session())
):
    try:
        await user_use_cases.delete_user(user_id)
        return None
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
