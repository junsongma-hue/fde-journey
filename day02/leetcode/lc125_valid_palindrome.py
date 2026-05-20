"""
LeetCode 125 — Valid Palindrome
https://leetcode.com/problems/valid-palindrome/

Return True if s is a palindrome, considering only alphanumeric chars
and ignoring case.

Day 2 lesson: two-pointer is the canonical pattern for "compare from both
ends" problems. Master this; it'll show up 20 more times this year.

Run me with:    uv run python day02/leetcode/lc125_valid_palindrome.py
"""

from __future__ import annotations


def is_palindrome(s: str) -> bool:
    """Two pointers, in-place skip of non-alphanumeric. O(n) time, O(1) space."""
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True


def is_palindrome_pythonic(s: str) -> bool:
    """The Python one-liner. Easier to read but allocates a new string."""
    cleaned = [c.lower() for c in s if c.isalnum()]
    return cleaned == cleaned[::-1]


def main() -> None:
    cases = [
        ("A man, a plan, a canal: Panama", True),
        ("race a car", False),
        (" ", True),                 # empty after cleanup
        ("0P", False),                # the famous gotcha — '0' and 'p' both alnum
    ]
    for s, expected in cases:
        got = is_palindrome(s)
        ok = "✅" if got == expected else "❌"
        print(f"{ok}  is_palindrome({s!r}) = {got}  (want {expected})")


if __name__ == "__main__":
    main()
