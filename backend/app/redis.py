import redis.asyncio as aioredis

from app.config import settings

client: aioredis.Redis | None = None


async def init_redis() -> None:
    global client
    client = aioredis.from_url(settings.redis_url, decode_responses=True)


async def close_redis() -> None:
    global client
    if client:
        await client.close()
        client = None


async def get_redis_client() -> aioredis.Redis:
    assert client is not None, "Redis client is not initialized"
    return client
