from app.services.fsrs import fsrs_review_state
from app.services.parsers import parse_transcript_to_words
from app.services.word_stats import summarise_word_stats


def test_fsrs_review_state_increases_interval_after_good_rating():
    state = fsrs_review_state(5, 2.5, 4)
    assert state["next_interval"] == 12


def test_parse_transcript_to_words_handles_punctuation():
    words = parse_transcript_to_words("I learn English, and I speak daily.")
    assert words == ["i", "learn", "english", "and", "i", "speak", "daily"]


def test_summarise_word_stats_counts_word_frequency():
    stats = summarise_word_stats(["English", "english", "study", "study", "study"])
    assert stats["english"] == 2
    assert stats["study"] == 3
