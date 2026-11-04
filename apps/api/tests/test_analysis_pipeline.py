from app.services.analysis_pipeline import (
    build_word_usage,
    compute_fluency_metrics,
    compute_pronunciation_score,
    extract_grammar_issues,
)


def test_compute_pronunciation_score_from_word_scores():
    score = compute_pronunciation_score([0.9, 0.8, 0.7])
    assert score == 80.0


def test_build_word_usage_counts_lowercase_tokens():
    usage = build_word_usage(["English", "english", "learning", "English"])
    assert usage["english"] == 3
    assert usage["learning"] == 1


def test_extract_grammar_issues_when_text_changes():
    issue = extract_grammar_issues("I am learning english", "I am learning English")
    assert len(issue) == 1
    assert issue[0]["corrected"] == "I am learning English"


def test_compute_fluency_metrics_uses_average_scores():
    metrics = compute_fluency_metrics([0.9, 0.75, 0.8], ["I", "study", "daily"])
    assert metrics["word_count"] == 3
    assert metrics["average_word_score"] == 0.817
