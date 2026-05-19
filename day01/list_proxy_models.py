"""
Day 1 - Probe what models the proxy actually exposes.

Cursor's "Add Model" button greys out when its preflight to /v1/models
returns nothing it recognizes. This script bypasses the SDK and just hits
the OpenAI-compatible /v1/models endpoint directly so we can see the
ground truth.

Run me with:    uv run python day01/list_proxy_models.py
"""

from __future__ import annotations

import os
import sys

import httpx
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

console = Console()


def main() -> None:
    load_dotenv()
    base_url = os.getenv("LLM_BASE_URL", "").rstrip("/")
    api_key = os.getenv("LLM_API_KEY", "")

    if not base_url or not api_key:
        console.print("[red]Missing LLM_BASE_URL or LLM_API_KEY in .env[/]")
        sys.exit(1)

    url = f"{base_url}/models"
    console.print(f"[dim]GET {url}[/dim]\n")

    try:
        resp = httpx.get(
            url,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=15.0,
        )
    except Exception as e:
        console.print(f"[red]Network error: {e}[/]")
        sys.exit(1)

    console.print(f"[dim]HTTP {resp.status_code}[/dim]\n")
    if resp.status_code != 200:
        console.print(f"[red]{resp.text[:500]}[/]")
        sys.exit(1)

    data = resp.json()
    items = data.get("data", []) if isinstance(data, dict) else data

    if not items:
        console.print("[yellow]Endpoint returned an empty list. "
                      "This is why Cursor says 'No models available'.[/]")
        console.print(f"\nRaw response (truncated):\n{resp.text[:800]}")
        return

    table = Table(title=f"{len(items)} models exposed by {base_url}")
    table.add_column("model id", style="cyan")
    table.add_column("owned_by")
    for m in items[:80]:
        table.add_row(m.get("id", "?"), m.get("owned_by", "-"))
    console.print(table)

    if len(items) > 80:
        console.print(f"[dim]...and {len(items) - 80} more[/dim]")


if __name__ == "__main__":
    main()
