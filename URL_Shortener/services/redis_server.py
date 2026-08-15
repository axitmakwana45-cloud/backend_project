import json
from typing import Any

from core.redis import redis_client


URL_CACHE_TTL = 60 * 60  


def get_url_cache_key(short_code: str) -> str:
    return f"url:{short_code}"


async def get_cached_url(short_code: str) -> dict[str, Any] | None:
    key = get_url_cache_key(short_code)

    cached_data = await redis_client.get(key)

    if cached_data is None:
        return None

    return json.loads(cached_data)


async def cache_url(
    short_code: str,
    data: dict[str, Any],
    ttl: int = URL_CACHE_TTL,
) -> None:
    key = get_url_cache_key(short_code)

    await redis_client.set(
        key,
        json.dumps(data),
        ex=ttl,
    )


async def delete_cached_url(short_code: str) -> None:
    key = get_url_cache_key(short_code)

    await redis_client.delete(key)