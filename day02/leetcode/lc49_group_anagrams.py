"""
LeetCode 49 — Group Anagrams
https://leetcode.com/problems/group-anagrams/

Group strings that are anagrams of each other.

Day 2 lesson: `defaultdict(list)` is the bucketing pattern. The trick here
is choosing the right *key* — sorted-string is the canonical form of an
anagram class.

Run me with:    uv run python day02/leetcode/lc49_group_anagrams.py
"""

from __future__ import annotations

from collections import defaultdict


def group_anagrams(strs: list[str]) -> list[list[str]]:
    """Bucket by canonical key (sorted letters)."""
    buckets: defaultdict[str, list[str]] = defaultdict(list)
    for s in strs:
        key = "".join(sorted(s))
        buckets[key].append(s)
    return list(buckets.values())


def main() -> None:
    cases: list[tuple[list[str], int]] = [
        (["eat", "tea", "tan", "ate", "nat", "bat"], 3),
        ([""], 1),
        (["a"], 1),
        (["abc", "bca", "cab", "xyz", "zyx"], 2),
    ]
    for strs, expected_groups in cases:
        got = group_anagrams(strs)
        ok = "✅" if len(got) == expected_groups else "❌"
        print(f"{ok}  group_anagrams({strs}) = {got}  ({len(got)} groups, want {expected_groups})")


if __name__ == "__main__":
    main()
