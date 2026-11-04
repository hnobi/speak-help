from __future__ import annotations

from pydantic import BaseModel, Field


class AnalysisResult(BaseModel):
    recording_id: str
    transcript: str
    overall_score: float = Field(default=0.0, ge=0.0, le=100.0)
    native_rewrite: str | None = None
    grammar_issues: list[dict] = Field(default_factory=list)
