from __future__ import annotations


def next_review_interval(last_interval: int, ease: float, rating: int) -> int:
    if rating < 3:
        return 1
    if rating == 3:
        return max(1, int(last_interval * 0.8))
    return max(1, int(last_interval * ease))


def fsrs_review_state(last_interval: int, ease: float, rating: int) -> dict:
    interval = next_review_interval(last_interval, ease, rating)
    return {"last_interval": last_interval, "ease": ease, "rating": rating, "next_interval": interval}
