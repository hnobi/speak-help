from fastapi import APIRouter, HTTPException

from app.schemas.vocab import VocabCreate, VocabResponse

router = APIRouter(prefix="/vocab", tags=["vocabulary"])


@router.post("", response_model=VocabResponse)
async def create_vocab(payload: VocabCreate) -> VocabResponse:
    if not payload.word.strip():
        raise HTTPException(status_code=400, detail="word is required")
    return VocabResponse(
        id="vocab_123",
        word=payload.word,
        lemma=payload.word.lower(),
        pos=payload.pos,
        definition=payload.definition or "A newly added word for practice.",
        status="learning",
    )
