import uuid
from datetime import datetime, timezone

from sqlalchemy import ForeignKey, JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class VocabWord(Base):
    __tablename__ = "vocab_words"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    word: Mapped[str] = mapped_column(String(128), nullable=False)
    lemma: Mapped[str] = mapped_column(String(128), nullable=False)
    pos: Mapped[str] = mapped_column(String(32), default="noun", nullable=False)
    ipa: Mapped[str | None] = mapped_column(String(128), nullable=True)
    audio_key: Mapped[str | None] = mapped_column(String(255), nullable=True)
    definition: Mapped[str | None] = mapped_column(Text, nullable=True)
    examples_json: Mapped[dict] = mapped_column(JSON, default=list, nullable=False)
    collocations_json: Mapped[dict] = mapped_column(JSON, default=list, nullable=False)
    register: Mapped[str] = mapped_column(String(32), default="neutral", nullable=False)
    user_sentence: Mapped[str | None] = mapped_column(Text, nullable=True)
    user_sentence_feedback: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="learning", nullable=False)
    tags: Mapped[dict] = mapped_column(JSON, default=list, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc), nullable=False)

    user = relationship("User", backref="vocab_words")
