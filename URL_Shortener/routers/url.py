from fastapi import APIRouter,Depends,Request
from schemas.url import URLresponse,URLcreate,URLupdate
from schemas.analytics import URLAnalyticsResponse
from sqlalchemy.orm import Session
from core.dependencies import get_current_user
from models.user import User
from services import url_controller,rate_limiter
from database.db import get_db
from fastapi.responses import RedirectResponse


router = APIRouter(prefix="/url")
redirect_router = APIRouter()

@router.post('/create',response_model=URLresponse)
def create_url(
    url: URLcreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return url_controller.create_short_url(db, url, current_user)

@router.get(
    "/all",
    response_model=list[URLresponse],
)
def get_urls(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return url_controller.get_all_urls(
        db=db,
        current_user=current_user,
    )
@router.get(
    "/{url_id}/analytics",
    response_model=URLAnalyticsResponse,
)
def get_analytics(
    url_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return url_controller.get_url_analytics(
        db=db,
        url_id=url_id,
        current_user=current_user,
    )


@router.get(
    "/{url_id}",
    response_model=URLresponse
)
def get_url(
    url_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return url_controller.get_url_by_id(
        db=db,
        url_id=url_id,
        current_user=current_user,
    )

@router.put(
    "/{url_id}",
    response_model=URLresponse,
)
async def update_url_route(
    url_id: int,
    url_data: URLupdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await url_controller.update_url(
        db=db,
        url_id=url_id,
        url_data=url_data,
        current_user=current_user,
    )

@router.delete("/{url_id}")
async def delete_url(url_id : int,db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),):
    return await url_controller.delete_url(db,url_id,current_user)

@redirect_router.get("/{short_code}")
async def redirect_url(
    short_code: str,
    request: Request,
    db: Session = Depends(get_db),
):
    ip_address = (
        request.client.host
        if request.client
        else None
    )

    await rate_limiter.check_rate_limit(
        f"ip:{ip_address}"
    )

    user_agent = request.headers.get("user-agent")

    original_url, cache_hit = await url_controller.redirect_to_original_url(
        db=db,
        short_code=short_code,
        ip_address=ip_address,
        user_agent=user_agent,
    )

    return RedirectResponse(
        url=original_url,
        status_code=302,
    )

