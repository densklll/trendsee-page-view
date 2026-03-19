import asyncpg
from fastapi import APIRouter, Depends, HTTPException, Path, status

from app.auth import create_token
from app.dependencies import get_current_user, get_db, get_publication_service
from app.publications.service import PublicationService
from app.users.repository import UserRepository
from app.users.schemas import (
    TokenResponse,
    UserCreate,
    UserCreateResponse,
    UserResponse,
    UserUpdate,
)

router = APIRouter(prefix="/users", tags=["users"])


def get_user_repo(db: asyncpg.Pool = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


@router.post("", response_model=UserCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    body: UserCreate,
    repo: UserRepository = Depends(get_user_repo),
):
    user = await repo.create(body.name)
    token = create_token(user["id"])
    return UserCreateResponse(user=UserResponse(**user), token=token)


@router.get("/{user_id}/token", response_model=TokenResponse)
async def get_token(
    user_id: int = Path(..., ge=1),
    repo: UserRepository = Depends(get_user_repo),
):
    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return TokenResponse(token=create_token(user_id))


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    body: UserUpdate,
    user_id: int = Path(..., ge=1),
    current_user_id: int = Depends(get_current_user),
    repo: UserRepository = Depends(get_user_repo),
):
    if user_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot modify another user")
    user = await repo.update_name(user_id, body.name)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserResponse(**user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int = Path(..., ge=1),
    current_user_id: int = Depends(get_current_user),
    repo: UserRepository = Depends(get_user_repo),
    pub_service: PublicationService = Depends(get_publication_service),
):
    if user_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot delete another user")

    await pub_service.clear_cache_by_user(user_id)

    deleted = await repo.delete(user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
