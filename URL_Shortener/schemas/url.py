from datetime import datetime
from typing import Optional

from pydantic import BaseModel,HttpUrl,ConfigDict

class URLcreate(BaseModel):

    original_url : HttpUrl
    expires_at : Optional[datetime] = None

class URLupdate(BaseModel):

    original_url : Optional[HttpUrl] = None
    is_active : Optional[bool] = None
    expires_at : Optional[datetime] = None

class URLresponse(BaseModel):

    id: int
    original_url: HttpUrl
    short_code: str
    clicks: int
    is_active: bool
    expires_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    user_id: int

    model_config = ConfigDict(from_attributes=True)

class URLAnalytics(BaseModel):
    short_code: str
    clicks: int


class URLListResponse(BaseModel):
    urls: list[URLresponse]