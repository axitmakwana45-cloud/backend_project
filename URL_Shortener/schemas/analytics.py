from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ClickResponse(BaseModel):
    id: int
    ip_address: str | None
    user_agent: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class URLAnalyticsResponse(BaseModel):
    url_id: int
    short_code: str
    total_clicks: int
    clicks: list[ClickResponse]