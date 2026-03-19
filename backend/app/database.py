import asyncpg

from app.config import settings

pool: asyncpg.Pool | None = None


async def _ensure_schema(conn: asyncpg.Connection) -> None:
    """Идемпотентные патчи для БД, созданных до изменений схемы.
    initdb.d не перезапускается на непустом volume, поэтому новые колонки
    добавляются здесь при каждом старте приложения."""
    row = await conn.fetchrow(
        "SELECT 1 FROM information_schema.tables "
        "WHERE table_schema = 'public' AND table_name = 'publications'"
    )
    if row is None:
        return
    await conn.execute(
        "ALTER TABLE publications ADD COLUMN IF NOT EXISTS cover_asset VARCHAR(255)"
    )


async def init_db() -> None:
    global pool
    pool = await asyncpg.create_pool(dsn=settings.database_url)
    async with pool.acquire() as conn:
        await _ensure_schema(conn)


async def close_db() -> None:
    global pool
    if pool:
        await pool.close()
        pool = None


async def get_pool() -> asyncpg.Pool:
    assert pool is not None, "Database pool is not initialized"
    return pool
