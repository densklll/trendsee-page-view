import asyncpg


class PublicationRepository:
    def __init__(self, pool: asyncpg.Pool):
        self._pool = pool

    async def create(self, user_id: int, title: str, text: str) -> dict:
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(
                "INSERT INTO publications (user_id, title, text) VALUES ($1, $2, $3) "
                "RETURNING id, user_id, title, text, cover_asset, created_at, updated_at",
                user_id,
                title,
                text,
            )
        return dict(row)

    async def get_by_id(self, pub_id: int) -> dict | None:
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT id, user_id, title, text, cover_asset, created_at, updated_at "
                "FROM publications WHERE id = $1",
                pub_id,
            )
        return dict(row) if row else None

    async def get_ids_by_user(self, user_id: int) -> list[int]:
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT id FROM publications WHERE user_id = $1 ORDER BY created_at DESC",
                user_id,
            )
        return [r["id"] for r in rows]

    async def get_by_user_paginated(self, user_id: int, limit: int = 10, offset: int = 0) -> list[dict]:
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT id, user_id, title, text, cover_asset, created_at, updated_at "
                "FROM publications WHERE user_id = $1 ORDER BY created_at DESC LIMIT $2 OFFSET $3",
                user_id, limit, offset,
            )
        return [dict(r) for r in rows]

    async def count_by_user(self, user_id: int) -> int:
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow("SELECT COUNT(*) as cnt FROM publications WHERE user_id = $1", user_id)
        return row["cnt"]

    async def get_by_ids(self, ids: list[int]) -> list[dict]:
        if not ids:
            return []
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT id, user_id, title, text, cover_asset, created_at, updated_at "
                "FROM publications WHERE id = ANY($1)",
                ids,
            )
        return [dict(r) for r in rows]

    async def update(self, pub_id: int, title: str | None, text: str | None) -> dict | None:
        parts: list[str] = []
        values: list = []
        idx = 1

        if title is not None:
            parts.append(f"title = ${idx}")
            values.append(title)
            idx += 1

        if text is not None:
            parts.append(f"text = ${idx}")
            values.append(text)
            idx += 1

        if not parts:
            return await self.get_by_id(pub_id)

        parts.append("updated_at = NOW()")
        values.append(pub_id)

        query = (
            f"UPDATE publications SET {', '.join(parts)} "
            f"WHERE id = ${idx} "
            "RETURNING id, user_id, title, text, cover_asset, created_at, updated_at"
        )

        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(query, *values)
        return dict(row) if row else None

    async def delete(self, pub_id: int) -> bool:
        async with self._pool.acquire() as conn:
            result = await conn.execute("DELETE FROM publications WHERE id = $1", pub_id)
        return result == "DELETE 1"

    async def get_owner_id(self, pub_id: int) -> int | None:
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT user_id FROM publications WHERE id = $1", pub_id
            )
        return row["user_id"] if row else None
