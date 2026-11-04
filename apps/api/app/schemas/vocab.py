from __future__ import annotations

from pydantic import BaseModel, Field


class VocabCreate(BaseModel):
    word: str = Field(min_length=1)
    pos: str = "noun"
    definition: str | None = None


class VocabResponse(BaseModel):
    id: str
    word: str
    lemma: str
    pos: str
    definition: str | None = None
    status: str = "learning"
