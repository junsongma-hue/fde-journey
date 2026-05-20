"""
LeetCode 1 — Two Sum
https://leetcode.com/problems/two-sum/

Given nums and target, return indices i, j such that nums[i] + nums[j] == target.

Day 2 lesson: the dict trick that turns O(n^2) brute force into O(n).

Run me with:    uv run python day02/leetcode/lc01_two_sum.py
"""

from __future__ import annotations


def two_sum(nums: list[int], target: int) -> list[int]:
    """One-pass hash map. Time O(n), space O(n)."""
    seen: dict[int, int] = {}      # value → its index
    for i, x in enumerate(nums):
        complement = target - x
        if complement in seen:
            return [seen[complement], i]
        seen[x] = i
    return []


def two_sum_brute_force(nums: list[int], target: int) -> list[int]:
    """The version you'd write first. O(n^2). Don't ship this."""
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []


# ---------------------------------------------------------------------------
# Self-tests — your own habit, not LeetCode's. FDE writes tests.
# ---------------------------------------------------------------------------
def main() -> None:
    cases = [
        ([2, 7, 11, 15], 9, [0, 1]),
        ([3, 2, 4], 6, [1, 2]),
        ([3, 3], 6, [0, 1]),
        ([1, 5, 8, 12], 100, []),     # no solution
    ]
    for nums, target, expected in cases:
        got = two_sum(nums, target)
        ok = "✅" if got == expected else "❌"
        print(f"{ok}  two_sum({nums}, {target}) = {got}  (want {expected})")


if __name__ == "__main__":
    main()
