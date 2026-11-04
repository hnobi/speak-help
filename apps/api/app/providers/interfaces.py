from __future__ import annotations

from typing import Protocol


class TranscriptToken(Protocol):
    word: str
    start: float
    end: float
    confidence: float


class TranscriptResult(Protocol):
    words: list[TranscriptToken]
    transcript: str


class TranscriptionProvider(Protocol):
    def transcribe(self, audio_key: str) -> TranscriptResult: ...


class PronunciationProvider(Protocol):
    def assess(self, transcript: str, audio_key: str) -> dict: ...


class LLMProvider(Protocol):
    def complete_json(self, prompt: str, schema: dict) -> dict: ...


class TTSProvider(Protocol):
    def synthesize(self, text: str, voice: str = "en-GB") -> str: ...
