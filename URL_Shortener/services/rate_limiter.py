from fastapi import HTTPException, status

from core.redis import redis_client


RATE_LIMIT = 30
WINDOW_SECONDS = 60


async def check_rate_limit(identifier: str) -> None:
    key = f"rate_limit:{identifier}"

    try:
        count = await redis_client.incr(key)

        if count == 1:
            await redis_client.expire(
                key,
                WINDOW_SECONDS,
            )

        if count > RATE_LIMIT:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Try again later.",
            )

    except HTTPException:
        raise

    except Exception:
        
        return