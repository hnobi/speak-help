from fastapi import APIRouter, HTTPException

from app.providers.fakes import FakeProviders
from app.schemas.recording import RecordingCreate, RecordingResponse

router = APIRouter(prefix="/recordings", tags=["recordings"])


@router.post("", response_model=RecordingResponse)
async def create_recording(payload: RecordingCreate) -> RecordingResponse:
    if not payload.storage_key:
        raise HTTPException(status_code=400, detail="storage_key is required")
    return RecordingResponse(
        id="rec_123",
        source=payload.source,
        storage_key=payload.storage_key,
        duration_s=payload.duration_s,
        status="uploaded",
    )


@router.post("/{recording_id}/process")
async def process_recording(recording_id: str) -> dict:
    provider = FakeProviders().transcription
    transcript = provider.transcribe(recording_id)
    return {"recording_id": recording_id, "status": "processing", "transcript": transcript["transcript"]}
