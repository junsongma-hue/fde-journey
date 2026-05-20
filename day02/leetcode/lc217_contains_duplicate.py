"""
LeetCode 217 — Contains Duplicate
https://leetcode.com/problems/contains-duplicate/

Return True if any value appears at least twice.

Day 2 lesson: when the question is about "any duplicate?", the answer is
almost always a `set` one-liner.

Run me with:    uv run python day02/leetcode/lc217_contains_duplicate.py
"""

from __future__ import annotations


def contains_duplicate(nums: list[int]) -> bool:
    """One-liner. Time O(n), space O(n)."""
    return len(set(nums)) != len(nums)


def contains_duplicate_explicit(nums: list[int]) -> bool:
    """Explicit version — same complexity, but shows the `seen set` pattern
    that you'll reuse for harder problems (e.g. LongestSubstringWithoutRepeating)."""
    seen: set[int] = set()
    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    return False


def main() -> None:
    cases = [
        ([1, 2, 3, 1], True),
        ([1, 2, 3, 4], False),
        ([1, 1, 1, 3, 3, 4, 3, 2, 4, 2], True),
        ([], False),
    ]
    for nums, expected in cases:
        got = contains_duplicate(nums)
        ok = "✅" if got == expected else "❌"
        print(f"{ok}  contains_duplicate({nums}) = {got}  (want {expected})")


if __name__ == "__main__":
    main()
