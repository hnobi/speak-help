from collections import Counter


def summarise_word_stats(words: list[str]) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for word in words:
        key = word.strip().lower()
        if key:
            counts[key] += 1
    return dict(sorted(counts.items(), key=lambda item: (-item[1], item[0])))
