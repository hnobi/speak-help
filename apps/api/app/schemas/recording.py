from __future__ import annotations

from pydantic import BaseModel, Field


class RecordingCreate(BaseModel):
    source: str = Field(default="audio")
    prompt_id: str | None = None
    storage_key: str = Field(min_length=1)
    duration_s: int = Field(default=0, ge=0)


class RecordingResponse(BaseModel):
    id: str
    source: str
    storage_key: str
    duration_s: int
    status: str
