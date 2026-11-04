import uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    display_name: Mapped[str] = mapped_column(String(160), nullable=False)
    accent_target: Mapped[str] = mapped_column(String(32), default="en-GB", nullable=False)
    daily_goal_minutes: Mapped[int] = mapped_column(default=15, nullable=False)
    timezone: Mapped[str] = mapped_column(String(80), default="UTC", nullable=False)
