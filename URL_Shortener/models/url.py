from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import (
    String,
    Text,
    Integer,
    Boolean,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.db import Base

if TYPE_CHECKING:
    from .user import User
    from .url_click import URLClick


class URL(Base):
    __tablename__ = "urls"

    # Primary Key
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    # Original Long URL
    original_url: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    # Generated Short Code
    short_code: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        nullable=False,
        index=True
    )

    # Number of Redirects
    clicks: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    # URL Status
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    # Optional Expiration
    expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True
    )

    # Created Timestamp
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    # Updated Timestamp
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

    # Foreign Key
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    # Relationship
    user: Mapped["User"] = relationship(
        back_populates="urls"
    )

    clicks_data: Mapped[list["URLClick"]] = relationship(
        back_populates="url",
        cascade="all, delete-orphan",
    )