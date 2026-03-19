import asyncpg
import redis.asyncio as aioredis
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import ExpiredSignatureError, InvalidTokenError

from app.auth import decode_token
from app.database import get_pool
from app.publications.repository import PublicationRepository
from app.publications.service import PublicationService
from app.redis import get_redis_client

security = HTTPBearer()


async def get_db() -> asyncpg.Pool:
    return await get_pool()


async def get_cache() -> aioredis.Redis:
    return await get_redis_client()


def get_publication_service(
    db: asyncpg.Pool = Depends(get_db),
    cache: aioredis.Redis = Depends(get_cache),
) -> PublicationService:
    return PublicationService(PublicationRepository(db), cache)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: asyncpg.Pool = Depends(get_db),
) -> int:
    try:
        user_id = decode_token(credentials.credentials)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
        )
    except (InvalidTokenError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    async with db.acquire() as conn:
        row = await conn.fetchrow("SELECT id FROM users WHERE id = $1", user_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
            )

    return user_id
