import uuid
from datetime import datetime, timezone

from sqlalchemy import ForeignKey, JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    recording_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("recordings.id"), nullable=False, index=True)
    transcript: Mapped[str] = mapped_column(Text, nullable=False)
    words_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    pronunciation_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    fluency_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    grammar_issues_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    native_rewrite: Mapped[str | None] = mapped_column(Text, nullable=True)
    overall_score: Mapped[float] = mapped_column(default=0.0, nullable=False)
    provider: Mapped[str] = mapped_column(String(64), default="mock", nullable=False)
    locale: Mapped[str] = mapped_column(String(16), default="en-GB", nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc), nullable=False)

    recording = relationship("Recording", backref="analyses")
