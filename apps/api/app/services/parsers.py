import re


def parse_transcript_to_words(transcript: str) -> list[str]:
    tokens = re.findall(r"[A-Za-z']+", transcript)
    return [token.lower() for token in tokens]
