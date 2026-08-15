from sqlalchemy.orm import Mapped, mapped_column,relationship
from database.db import Base
from datetime import datetime,UTC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.url import URL

class User(Base):

    __tablename__ = "users"

    id : Mapped[int] = mapped_column(primary_key=True)

    username : Mapped[str] = mapped_column(
        unique=True,
        nullable=False
    )

    email : Mapped[str] = mapped_column(
        unique=True,
        nullable=False,
        index = True
    )

    password : Mapped[str] = mapped_column(
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
       default=lambda: datetime.now(UTC)
    )

    urls: Mapped[list["URL"]] = relationship(
    back_populates="user"
)