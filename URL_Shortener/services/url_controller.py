import random
import string
from fastapi import HTTPException, status
from sqlalchemy import update
from sqlalchemy.orm import Session
from models.url import URL
from models.user import User
from models.url_click import URLClick
from schemas.url import URLcreate,URLupdate
from datetime import datetime, timezone
from services.redis_server import get_cached_url,cache_url,delete_cached_url


def short_url(length : int = 6):

    a = string.ascii_letters + string.digits

    return "".join( random.choices(a,k=length))

def unique_short_url(db : Session):

    while True:

        code = short_url()

        existing = (
            db.query(URL)
            .filter(URL.short_code == code)
            .first()
        )

        if not existing:
            return code

def create_short_url(db : Session,url_data : URLcreate,current_user : User):

    code = unique_short_url(db)

    url = URL(
        original_url=str(url_data.original_url),
        short_code=code,
        expires_at=url_data.expires_at,
        user_id=current_user.id,
    )

    db.add(url)
    db.commit()
    db.refresh(url)

    return url

def get_all_urls(
    db: Session,
    current_user: User,
):
    return (
        db.query(URL)
        .filter(URL.user_id == current_user.id)
        .order_by(URL.created_at.desc())
        .all()
    )

def get_url_by_id(
    db: Session,
    url_id: int,
    current_user: User,
):
    url = (
        db.query(URL)
        .filter(
            URL.id == url_id,
            URL.user_id == current_user.id
        )
        .first()
    )

    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="URL not found"
        )

    return url


async def update_url(
    db: Session,
    url_id: int,
    url_data: URLupdate,
    current_user: User,
):
    url = (
        db.query(URL)
        .filter(
            URL.id == url_id,
            URL.user_id == current_user.id
        )
        .first()
    )

    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="URL not found"
        )

    update_data = url_data.model_dump(exclude_unset=True)
        
    for key, value in update_data.items():
        setattr(url, key, str(value))
    db.add(url)
    db.commit()
    db.refresh(url)

    try:
        await delete_cached_url(url.short_code)
    except Exception:
        pass

    return url

async def delete_url(db : Session,url_id : int,current_user : User):

    url = (
            db.query(URL)
            .filter(
                URL.id == url_id,
                URL.user_id == current_user.id
            )
            .first()
        )

    if not url:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="URL not found"
            )

    short_code = url.short_code

    db.delete(url)
    db.commit()

    try:
        await delete_cached_url(short_code)
    except Exception:
        pass

    return {
        "message": "URL deleted successfully"
    }


async def redirect_to_original_url(
    db: Session,
    short_code: str,
    ip_address: str | None,
    user_agent: str | None,
):
    # ==========================================
    # 1. REDIS LOOKUP
    # ==========================================

    try:
        cached_url = await get_cached_url(short_code)
    except Exception:
        # Redis failure should not break redirect
        cached_url = None

    # ==========================================
    # 2. REDIS HIT
    # ==========================================

    if cached_url is not None:

        # Check active
        if not cached_url["is_active"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="URL is disabled",
            )

        # Check expiration
        if cached_url["expires_at"] is not None:

            expires_at = datetime.fromisoformat(
                cached_url["expires_at"]
            )

            if expires_at < datetime.now(timezone.utc):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="URL has expired",
                )

        url_id = int(cached_url["url_id"])

        # --------------------------------------
        # Analytics record
        # --------------------------------------

        click = URLClick(
            url_id=url_id,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        db.add(click)

        # --------------------------------------
        # Atomic click increment
        # --------------------------------------

        db.execute(
            update(URL)
            .where(URL.id == url_id)
            .values(
                clicks=URL.clicks + 1
            )
        )

        db.commit()

        return cached_url["original_url"], True

    # ==========================================
    # 3. REDIS MISS → POSTGRESQL
    # ==========================================

    url = (
        db.query(URL)
        .filter(
            URL.short_code == short_code
        )
        .first()
    )

    if url is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short URL not found",
        )

    # ==========================================
    # 4. CHECK ACTIVE
    # ==========================================

    if not url.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="URL is disabled",
        )

    # ==========================================
    # 5. CHECK EXPIRATION
    # ==========================================

    if (
        url.expires_at is not None
        and url.expires_at < datetime.now(timezone.utc)
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="URL has expired",
        )

    # ==========================================
    # 6. ANALYTICS
    # ==========================================

    click = URLClick(
        url_id=url.id,
        ip_address=ip_address,
        user_agent=user_agent,
    )

    db.add(click)

    # ==========================================
    # 7. ATOMIC CLICK INCREMENT
    # ==========================================

    db.execute(
        update(URL)
        .where(URL.id == url.id)
        .values(
            clicks=URL.clicks + 1
        )
    )

    db.commit()

    # ==========================================
    # 8. CACHE IN REDIS
    # ==========================================

    cache_data = {
        "url_id": url.id,
        "original_url": str(url.original_url),
        "is_active": url.is_active,
        "expires_at": (
            url.expires_at.isoformat()
            if url.expires_at is not None
            else None
        ),
    }

    try:
        await cache_url(
            short_code=short_code,
            data=cache_data,
        )
    except Exception:
        # Redis failure should not affect redirect
        pass

    # ==========================================
    # 9. RETURN
    # ==========================================

    return str(url.original_url), False


def get_url_analytics(
    db: Session,
    url_id: int,
    current_user: User,
):
    url = (
        db.query(URL)
        .filter(
            URL.id == url_id,
            URL.user_id == current_user.id,
        )
        .first()
    )

    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="URL not found",
        )

    clicks = (
        db.query(URLClick)
        .filter(URLClick.url_id == url.id)
        .order_by(URLClick.created_at.desc())
        .all()
    )

    return {
        "url_id": url.id,
        "short_code": url.short_code,
        "total_clicks": url.clicks,
        "clicks": clicks,
    }