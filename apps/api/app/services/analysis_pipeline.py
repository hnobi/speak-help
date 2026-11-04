from __future__ import annotations

from collections import Counter
from statistics import mean


def compute_pronunciation_score(word_scores: list[float]) -> float:
    if not word_scores:
        return 0.0
    return round(mean(word_scores) * 100, 2)


def compute_fluency_metrics(word_scores: list[float], words: list[str]) -> dict:
    return {
        "overall_score": compute_pronunciation_score(word_scores),
        "word_count": len(words),
        "average_word_score": round(mean(word_scores), 3) if word_scores else 0.0,
    }


def build_word_usage(words: list[str]) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for word in words:
        token = word.lower().strip(".,!?;:()[]{}\n")
        if token:
            counts[token] += 1
    return dict(sorted(counts.items(), key=lambda item: (-item[1], item[0])))


def extract_grammar_issues(transcript: str, corrected_text: str) -> list[dict]:
    if transcript == corrected_text:
        return []
    return [
        {
            "category": "grammar",
            "original": transcript,
            "corrected": corrected_text,
            "explanation": "The corrected version is more natural for spoken English.",
        }
    ]


def normalise_audio_key(storage_key: str) -> str:
    return storage_key.replace("\\", "/").lstrip("/")
