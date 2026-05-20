"""
LeetCode 242 — Valid Anagram
https://leetcode.com/problems/valid-anagram/

Return True if t is an anagram of s.

Day 2 lesson: `collections.Counter` is the most idiomatic way to compare
character (or token) frequencies. Most candidates write a manual dict — don't.

Run me with:    uv run python day02/leetcode/lc242_valid_anagram.py
"""

from __future__ import annotations

from collections import Counter


def is_anagram(s: str, t: str) -> bool:
    """Counter equality — pure idiomatic Python."""
    return Counter(s) == Counter(t)


def is_anagram_sorted(s: str, t: str) -> bool:
    """Alternative: sort both, compare. O(n log n) but a one-liner."""
    return sorted(s) == sorted(t)


def main() -> None:
    cases = [
        ("anagram", "nagaram", True),
        ("rat", "car", False),
        ("", "", True),
        ("abc", "abcd", False),
    ]
    for s, t, expected in cases:
        got = is_anagram(s, t)
        ok = "✅" if got == expected else "❌"
        print(f"{ok}  is_anagram({s!r}, {t!r}) = {got}  (want {expected})")


if __name__ == "__main__":
    main()
