import asyncpg


class UserRepository:
    def __init__(self, pool: asyncpg.Pool):
        self._pool = pool

    async def create(self, name: str) -> dict:
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(
                "INSERT INTO users (name) VALUES ($1) "
                "RETURNING id, name, created_at, updated_at",
                name,
            )
        return dict(row)

    async def get_by_id(self, user_id: int) -> dict | None:
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT id, name, created_at, updated_at FROM users WHERE id = $1",
                user_id,
            )
        return dict(row) if row else None

    async def update_name(self, user_id: int, name: str) -> dict | None:
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(
                "UPDATE users SET name = $1, updated_at = NOW() WHERE id = $2 "
                "RETURNING id, name, created_at, updated_at",
                name,
                user_id,
            )
        return dict(row) if row else None

    async def delete(self, user_id: int) -> bool:
        async with self._pool.acquire() as conn:
            result = await conn.execute("DELETE FROM users WHERE id = $1", user_id)
        return result == "DELETE 1"
