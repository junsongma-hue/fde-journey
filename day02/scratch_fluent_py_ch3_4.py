"""
Day 2 · Block 1 — Fluent Python Ch3 (dict & set) and Ch4 (str vs bytes)

This is your *active reading* notebook. The pattern:
  1. Read a few pages of the book.
  2. Come back here. Try the concept yourself in the matching `# experiment N` block.
  3. Run the script: `uv run python day02/scratch_fluent_py_ch3_4.py`
  4. If anything surprises you, write a one-liner in your reflection.

DO NOT just run this and move on. The point is to *type* each experiment
yourself first. Only peek at my version when you're stuck.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from rich import print  # nicer repr
from rich.rule import Rule


# ============================================================================
# Ch3 — Dictionaries and Sets
# ============================================================================

def experiment_0_dict_comprehension() -> None:
    """Q4 — group user actions into ordered lists per user."""
    print(Rule("Experiment Q4 — group actions by user"))

    events = [
        {"user": "alice", "action": "login"},
        {"user": "bob", "action": "click"},
        {"user": "alice", "action": "click"},
        {"user": "alice", "action": "logout"},
        {"user": "bob", "action": "login"},
    ]

    def group_actions_by_user(events: list[dict]) -> dict[str, list[str]]:
        groups = defaultdict(list)
        for event in events:
            groups[event["user"]].append(event["action"])
        return dict(groups)

    result = group_actions_by_user(events)
    print(result)
def experiment_1_dict_comprehension() -> None:
    """Build a dict from two parallel lists in ONE line."""
    print(Rule("Experiment 1 — dict comprehension"))
    tickers = ["NVDA", "AAPL", "MSFT", "GOOGL"]
    prices = [880.0, 195.0, 415.0, 165.0]

    quotes = {n: s for n, s in zip(prices,tickers)}

    # Your turn: build {ticker: price} in one line, then run me.
    #quotes = {t: p for t, p in zip(tickers, prices)}
    print(quotes)


def experiment_2_setdefault_vs_defaultdict() -> None:
    """Group items by first letter — two idioms."""
    print(Rule("Experiment 2 — setdefault vs defaultdict"))
    words = ["apple", "ant", "banana", "blueberry", "cherry"]

    by_letter_a: dict[str, list[str]]={}
    for word in words:
        by_letter_a.setdefault(word[0],[]).append(word)

    print("setdefault:", by_letter_a)

    # Idiom B: defaultdict — cleaner, but it's a different class
    by_letter_b: defaultdict[str, list[str]] = defaultdict(list)
    for w in words:
        by_letter_b[w[0]].append(w)
    print("defaultdict:", dict(by_letter_b))

    # Surprise: defaultdict doesn't behave like a dict on `.get()`!
    # Try this and see what happens:
    #print("by_letter_a[‘z’] (creates new key!):", by_letter_a['z'])
    
    print("by_letter_b['z'] (creates new key!):", by_letter_b["z"])
    print("after 'z' access:", dict(by_letter_b),dict(by_letter_a))

    
# defaultdict(<class 'list'>, {'a': ['apple', 'ant'], 'b': ['banana']})


def experiment_3_hashable() -> None:
    """What can be a dict key, what cannot, and why."""
    print(Rule("Experiment 3 — hashability"))
    valid_key = ("AAPL", "2026-Q1")          # tuple of immutables → ok
    print({valid_key: 195.0})

    try:
        invalid_key = ["AAPL", "2026-Q1"]     # list → unhashable
        print({invalid_key: 195.0})
    except TypeError as e:
        print(f"Lists can't be keys: {e}")

    # Frozen sets ARE hashable
    fs = frozenset(["NVDA", "AAPL"])
    print({fs: "tech bucket"})


def experiment_4_counter() -> None:
    """Counter — a dict subclass for counting things. FDE uses this often."""
    print(Rule("Experiment 4 — Counter"))
    log_lines = [
        "INFO ok",
        "ERROR timeout",
        "INFO ok",
        "WARN slow",
        "ERROR timeout",
        "ERROR rate-limit",
        "INFO ok",
    ]
    levels = [line.split()[0] for line in log_lines]
    counts = Counter(levels)
    print("counts:", counts)
    print("top 2:", counts.most_common(2))

    # Add another batch
    counts.update(["INFO", "INFO", "ERROR"])
    print("after update:", counts)


def experiment_5_sets_for_diff() -> None:
    """Set algebra is the fastest way to compare collections."""
    print(Rule("Experiment 5 — set algebra"))
    yesterday = {"NVDA", "AAPL", "MSFT", "GOOGL"}
    today = {"NVDA", "AAPL", "TSLA", "MSFT"}

    print("dropped:", yesterday - today)        # in yesterday, not today
    print("added:  ", today - yesterday)        # in today, not yesterday
    print("kept:   ", yesterday & today)        # in both
    print("union:  ", yesterday | today)        # in either


# ============================================================================
# Ch4 — Unicode Text vs Bytes
# ============================================================================

def experiment_6_str_vs_bytes() -> None:
    """The mental model: str is text, bytes is octets. Conversions can fail."""
    print(Rule("Experiment 6 — str vs bytes"))
    s = "财报"
    b = s.encode("utf-8")
    print(f"str  : {s!r} (len {len(s)})")
    print(f"bytes: {b!r} (len {len(b)})")  # Chinese: 6 bytes for 2 chars in utf-8

    # Round-trip
    print("decoded back:", b.decode("utf-8"))


def experiment_7_encoding_failure() -> None:
    """When the encoding doesn't fit. FDE: customer files often arrive in legacy encodings."""
    print(Rule("Experiment 7 — encoding failures"))
    s = "财报"

    # GBK can encode Chinese, but it's narrower than UTF-8
    print("gbk:", s.encode("gbk"))

    # Latin-1 cannot represent Chinese
    try:
        s.encode("latin-1")
    except UnicodeEncodeError as e:
        print(f"latin-1 fails: {e}")

    # Three error policies. Each one matters in different situations.
    print("strict (default) raises above")
    print("replace:", s.encode("latin-1", errors="replace"))
    print("ignore: ", s.encode("latin-1", errors="ignore"))


def experiment_8_decode_real_world() -> None:
    """What if a customer sends you a CSV in GBK and you naively read as UTF-8?"""
    print(Rule("Experiment 8 — wrong-encoding decode"))
    raw_gbk = "公司,营收\n苹果,1000\n微软,900".encode("gbk")
    print(f"raw bytes: {raw_gbk!r}")

    try:
        raw_gbk.decode("utf-8")
    except UnicodeDecodeError as e:
        print(f"naive utf-8 decode fails: {e}")

    print("correct:", raw_gbk.decode("gbk"))


def experiment_9_normalization() -> None:
    """The famous é trap: same character, two byte representations."""
    print(Rule("Experiment 9 — Unicode normalization"))
    import unicodedata as ud

    a = "café"                    # one combined codepoint
    b = "cafe\u0301"              # 'e' + combining acute accent

    print(f"a: {a!r} len={len(a)}")
    print(f"b: {b!r} len={len(b)}")
    print(f"a == b? {a == b}")    # False — looks the same, isn't!

    a_n = ud.normalize("NFC", a)
    b_n = ud.normalize("NFC", b)
    print(f"after NFC: {a_n == b_n}")


def experiment_10_walrus_with_dict() -> None:
    """Bonus: the walrus operator + dict — a real FDE one-liner."""
    print(Rule("Experiment 10 — walrus operator (PEP 572)"))
    data = {"NVDA": 880.0, "AAPL": 195.0, "MSFT": None}

    # Old way: .get() then check
    for ticker, price in data.items():
        if price is not None and (doubled := price * 2) > 500:
            print(f"  {ticker}: 2x = {doubled}")


# ============================================================================
# Run all experiments
# ============================================================================

def main() -> None:
    experiment_0_dict_comprehension()
    experiment_1_dict_comprehension()
    experiment_2_setdefault_vs_defaultdict()
    experiment_3_hashable()
    experiment_4_counter()
    experiment_5_sets_for_diff()
    experiment_6_str_vs_bytes()
    experiment_7_encoding_failure()
    experiment_8_decode_real_world()
    experiment_9_normalization()
    experiment_10_walrus_with_dict()


if __name__ == "__main__":
    main()
