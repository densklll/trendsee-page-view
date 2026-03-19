import asyncpg
from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from app.dependencies import get_current_user, get_publication_service
from app.publications.schemas import PaginatedPublicationsResponse, PublicationCreate, PublicationResponse, PublicationUpdate
from app.publications.service import PublicationService

router = APIRouter(prefix="/publications", tags=["publications"])


@router.post("", response_model=PublicationResponse, status_code=status.HTTP_201_CREATED)
async def create_publication(
    body: PublicationCreate,
    user_id: int = Depends(get_current_user),
    service: PublicationService = Depends(get_publication_service),
):
    try:
        pub = await service.create(user_id, body.title, body.text)
    except asyncpg.ForeignKeyViolationError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return PublicationResponse(**pub)


@router.get("/user/{user_id}", response_model=list[PublicationResponse])
async def get_user_publications(
    user_id: int = Path(..., ge=1),
    service: PublicationService = Depends(get_publication_service),
):
    pubs = await service.get_by_user(user_id)
    return [PublicationResponse(**p) for p in pubs]


@router.get("/user/{user_id}/feed", response_model=PaginatedPublicationsResponse)
async def get_user_publications_feed(
    user_id: int = Path(..., ge=1),
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0),
    service: PublicationService = Depends(get_publication_service),
):
    items = await service.get_by_user_paginated(user_id, limit=limit, offset=offset)
    total = await service.count_by_user(user_id)
    return PaginatedPublicationsResponse(items=[PublicationResponse(**p) for p in items], total=total, limit=limit, offset=offset)


@router.get("/{pub_id}", response_model=PublicationResponse)
async def get_publication(
    pub_id: int = Path(..., ge=1),
    service: PublicationService = Depends(get_publication_service),
):
    pub = await service.get_by_id(pub_id)
    if not pub:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Publication not found"
        )
    return PublicationResponse(**pub)


@router.patch("/{pub_id}", response_model=PublicationResponse)
async def update_publication(
    body: PublicationUpdate,
    pub_id: int = Path(..., ge=1),
    user_id: int = Depends(get_current_user),
    service: PublicationService = Depends(get_publication_service),
):
    owner = await service.get_owner_id(pub_id)
    if owner is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Publication not found")
    if owner != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your publication")
    pub = await service.update(pub_id, body.title, body.text)
    if pub is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Publication not found")
    return PublicationResponse(**pub)


@router.delete("/{pub_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_publication(
    pub_id: int = Path(..., ge=1),
    user_id: int = Depends(get_current_user),
    service: PublicationService = Depends(get_publication_service),
):
    owner = await service.get_owner_id(pub_id)
    if owner is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Publication not found")
    if owner != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your publication")
    await service.delete(pub_id)
