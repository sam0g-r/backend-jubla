from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from app.application.use_cases.user_use_cases import UserUseCases
from app.application.dto.user_dto import CreateUserDTO, UpdateUserDTO, UserResponseDTO
from app.presentation.dependencies import get_user_use_cases
from app.shared.exceptions.user_exceptions import UserAlreadyExistsError, UserNotFoundError

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: CreateUserDTO,
    user_use_cases: UserUseCases = Depends(get_user_use_cases)
):
    try:
        user = await user_use_cases.create_user(user_data)
        return user
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )

@router.get("/{user_id}", response_model=UserResponseDTO)
async def get_user(
    user_id: UUID,
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
    user_id: UUID,
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
    user_id: UUID,
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