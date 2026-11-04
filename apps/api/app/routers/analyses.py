from fastapi import APIRouter

from app.providers.fakes import FakeProviders
from app.schemas.analysis import AnalysisResult

router = APIRouter(prefix="/analyses", tags=["analyses"])


@router.get("/{recording_id}", response_model=AnalysisResult)
async def get_analysis(recording_id: str) -> AnalysisResult:
    transcript = FakeProviders().transcription.transcribe(recording_id)["transcript"]
    return AnalysisResult(
        recording_id=recording_id,
        transcript=transcript,
        overall_score=89.0,
        native_rewrite="I learn English every day.",
        grammar_issues=[],
    )
