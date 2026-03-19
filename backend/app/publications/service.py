import asyncio
import json
from datetime import datetime

import redis.asyncio as aioredis

from app.config import settings
from app.publications.repository import PublicationRepository


class PublicationService:
    def __init__(self, repo: PublicationRepository, cache: aioredis.Redis):
        self._repo = repo
        self._cache = cache

    @staticmethod
    def _key(pub_id: int) -> str:
        return f"publication:{pub_id}"

    @staticmethod
    def _serialize(pub: dict) -> str:
        data = {}
        for k, v in pub.items():
            data[k] = v.isoformat() if isinstance(v, datetime) else v
        return json.dumps(data)

    @staticmethod
    def _deserialize(raw: str) -> dict:
        data = json.loads(raw)
        data["created_at"] = datetime.fromisoformat(data["created_at"])
        data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        return data

    async def create(self, user_id: int, title: str, text: str) -> dict:
        pub = await self._repo.create(user_id, title, text)
        await self._cache.setex(
            self._key(pub["id"]),
            settings.publication_cache_ttl,
            self._serialize(pub),
        )
        pub["source"] = "cache"
        return pub

    async def get_by_user(self, user_id: int) -> list[dict]:
        all_ids = await self._repo.get_ids_by_user(user_id)
        if not all_ids:
            return []

        keys = [self._key(pid) for pid in all_ids]
        cached_values = await self._cache.mget(keys)

        result: list[dict] = []
        uncached_ids: list[int] = []

        for pub_id, cached in zip(all_ids, cached_values):
            if cached:
                pub = self._deserialize(cached)
                pub["source"] = "cache"
                result.append(pub)
            else:
                uncached_ids.append(pub_id)

        if uncached_ids:
            await asyncio.sleep(2)
            db_pubs = await self._repo.get_by_ids(uncached_ids)
            for pub in db_pubs:
                pub["source"] = "database"
                result.append(pub)

        result.sort(key=lambda x: x["created_at"], reverse=True)
        return result

    async def get_by_user_paginated(self, user_id: int, limit: int = 10, offset: int = 0) -> list[dict]:
        rows = await self._repo.get_by_user_paginated(user_id, limit, offset)
        all_ids = [r["id"] for r in rows]
        if not all_ids:
            return []

        keys = [self._key(pid) for pid in all_ids]
        cached_values = await self._cache.mget(keys)

        result: list[dict | None] = [None] * len(all_ids)
        uncached_ids: list[int] = []

        for i, (pub_id, cached) in enumerate(zip(all_ids, cached_values)):
            if cached:
                pub = self._deserialize(cached)
                pub["source"] = "cache"
                result[i] = pub
            else:
                uncached_ids.append(pub_id)

        if uncached_ids:
            await asyncio.sleep(2)
            db_pubs = await self._repo.get_by_ids(uncached_ids)
            id_to_pub = {p["id"]: p for p in db_pubs}
            for i, pub_id in enumerate(all_ids):
                if result[i] is None:
                    pub = id_to_pub[pub_id]
                    pub["source"] = "database"
                    result[i] = pub

        return [r for r in result if r is not None]

    async def count_by_user(self, user_id: int) -> int:
        return await self._repo.count_by_user(user_id)

    async def update(self, pub_id: int, title: str | None, text: str | None) -> dict | None:
        pub = await self._repo.update(pub_id, title, text)
        if not pub:
            return None

        ttl = await self._cache.ttl(self._key(pub_id))
        if ttl > 0:
            await self._cache.setex(self._key(pub_id), ttl, self._serialize(pub))
            pub["source"] = "cache"
        else:
            pub["source"] = "database"
        return pub

    async def delete(self, pub_id: int) -> bool:
        deleted = await self._repo.delete(pub_id)
        if deleted:
            await self._cache.delete(self._key(pub_id))
        return deleted

    async def clear_cache_by_user(self, user_id: int) -> None:
        pub_ids = await self._repo.get_ids_by_user(user_id)
        if pub_ids:
            await self._cache.delete(*[self._key(pid) for pid in pub_ids])

    async def get_owner_id(self, pub_id: int) -> int | None:
        return await self._repo.get_owner_id(pub_id)

    async def get_by_id(self, pub_id: int) -> dict | None:
        raw = await self._cache.get(self._key(pub_id))
        if raw:
            if isinstance(raw, (bytes, bytearray)):
                raw = raw.decode()
            pub = self._deserialize(raw)
            pub["source"] = "cache"
            return pub
        await asyncio.sleep(2)
        pub = await self._repo.get_by_id(pub_id)
        if not pub:
            return None
        pub["source"] = "database"
        return pub
