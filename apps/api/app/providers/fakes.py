from __future__ import annotations

from app.providers.interfaces import LLMProvider, PronunciationProvider, TTSProvider, TranscriptionProvider


class FakeTranscriptionProvider:
    def transcribe(self, audio_key: str):
        return {
            "transcript": "I am learning English every day.",
            "words": [
                {"word": "I", "start": 0.0, "end": 0.35, "confidence": 0.99},
                {"word": "am", "start": 0.35, "end": 0.6, "confidence": 0.97},
                {"word": "learning", "start": 0.6, "end": 1.2, "confidence": 0.95},
                {"word": "English", "start": 1.2, "end": 1.8, "confidence": 0.96},
                {"word": "every", "start": 1.8, "end": 2.2, "confidence": 0.94},
                {"word": "day", "start": 2.2, "end": 2.6, "confidence": 0.96},
            ],
        }


class FakePronunciationProvider:
    def assess(self, transcript: str, audio_key: str) -> dict:
        return {
            "overall_score": 89.0,
            "word_scores": [0.92, 0.9, 0.87, 0.91, 0.88, 0.94],
            "fluency": {"wpm": 122, "filler_count": 1, "pause_ms": [250, 180]},
        }


class FakeLLMProvider:
    def complete_json(self, prompt: str, schema: dict) -> dict:
        return {
            "grammar_issues": [],
            "native_rewrite": "I learn English every day.",
            "word_usage": {"learn": 1, "english": 1, "day": 1},
        }


class FakeTTSProvider:
    def synthesize(self, text: str, voice: str = "en-GB") -> str:
        return f"https://example.com/audio/{voice}/{abs(hash(text))}.mp3"


class FakeProviders:
    transcription: TranscriptionProvider = FakeTranscriptionProvider()
    pronunciation: PronunciationProvider = FakePronunciationProvider()
    llm: LLMProvider = FakeLLMProvider()
    tts: TTSProvider = FakeTTSProvider()
