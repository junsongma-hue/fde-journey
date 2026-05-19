"""
Day 1 - Python warm-up.

Goal: stretch the language muscles before touching LLMs.
We do four tiny exercises that together cover the language features
I'll lean on every day for the next 60 days:

1. f-strings + type hints
2. dict / list comprehensions
3. context managers (with statement)
4. dataclasses (the "PM-friendly" way to model data)

Run me with:    uv run python day01/hello_python.py
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


# 1. dataclasses ------------------------------------------------------------
@dataclass
class Holding:
    """One position in my (totally hypothetical) portfolio."""

    ticker: str
    shares: int
    cost_basis: float  # USD per share

    @property
    def book_value(self) -> float:
        return self.shares * self.cost_basis

    def pnl(self, current_price: float) -> float:
        return (current_price - self.cost_basis) * self.shares


# 2. some sample data -------------------------------------------------------
PORTFOLIO: list[Holding] = [
    Holding("NVDA", shares=10, cost_basis=420.0),
    Holding("AAPL", shares=20, cost_basis=180.0),
    Holding("MSFT", shares=5, cost_basis=310.0),
]

# Pretend these came back from an API. Day 1: hardcoded is fine.
LATEST_PRICES: dict[str, float] = {
    "NVDA": 880.0,
    "AAPL": 195.0,
    "MSFT": 415.0,
}


# 3. the analytics ----------------------------------------------------------
def portfolio_summary(
    holdings: list[Holding],
    prices: dict[str, float],
) -> dict[str, float]:
    """Return a one-shot dict of portfolio metrics."""
    book = sum(h.book_value for h in holdings)
    market = sum(h.shares * prices[h.ticker] for h in holdings)
    pnl = market - book
    return {
        "book_value": round(book, 2),
        "market_value": round(market, 2),
        "unrealized_pnl": round(pnl, 2),
        "return_pct": round(pnl / book * 100, 2),
    }


def winners_and_losers(
    holdings: list[Holding],
    prices: dict[str, float],
) -> tuple[list[str], list[str]]:
    winners = [h.ticker for h in holdings if h.pnl(prices[h.ticker]) > 0]
    losers = [h.ticker for h in holdings if h.pnl(prices[h.ticker]) <= 0]
    return winners, losers


# 4. context manager: write a tiny report -----------------------------------
def write_report(summary: dict[str, float], path: Path) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with path.open("w", encoding="utf-8") as f:
        f.write(f"# Portfolio snapshot · {timestamp}\n\n")
        for key, value in summary.items():
            f.write(f"- **{key}**: {value}\n")


# 5. main -------------------------------------------------------------------
def main() -> None:
    summary = portfolio_summary(PORTFOLIO, LATEST_PRICES)
    winners, losers = winners_and_losers(PORTFOLIO, LATEST_PRICES)

    print("=" * 50)
    print("Day 1 portfolio summary")
    print("=" * 50)
    for key, value in summary.items():
        print(f"  {key:>16} = {value}")
    print(f"\n  winners: {winners}")
    print(f"  losers : {losers}")

    out = Path(__file__).parent / "portfolio_snapshot.md"
    write_report(summary, out)
    print(f"\n📝 Report written to {out.relative_to(Path.cwd())}")


if __name__ == "__main__":
    main()
