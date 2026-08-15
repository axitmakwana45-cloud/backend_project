from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.db import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .url import URL

class URLClick(Base):
    __tablename__ = "url_clicks"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    url_id: Mapped[int] = mapped_column(
        ForeignKey("urls.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    ip_address: Mapped[str | None] = mapped_column(
        String(45),
        nullable=True,
    )

    user_agent: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    url: Mapped["URL"] = relationship(
        back_populates="clicks_data"
    )