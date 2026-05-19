"""
Day 1 - First LLM call. Hello, Claude.

Goal: prove the whole loop end-to-end.
1. Read the API key from .env (never hardcode secrets).
2. Send a small prompt to Claude.
3. Print the response with a pretty terminal UI.
4. Print the token usage so I start feeling FDE-style cost awareness.

Run me with:    uv run python day01/hello_llm.py
"""

from __future__ import annotations

import os
import sys

from anthropic import Anthropic
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

console = Console()


def load_api_key() -> str:
    """Load Anthropic API key from .env or fail fast with a helpful message."""
    load_dotenv()
    key = os.getenv("ANTHROPIC_API_KEY", "")
    if not key or key.startswith("sk-ant-xxxxxxxx"):
        console.print(
            Panel.fit(
                "[bold red]No Anthropic API key found.[/]\n\n"
                "1. Copy [cyan].env.example[/] to [cyan].env[/]\n"
                "2. Get a key from https://console.anthropic.com/settings/keys\n"
                "3. Paste it as [cyan]ANTHROPIC_API_KEY=sk-ant-...[/] in .env",
                title="Setup needed",
                border_style="red",
            )
        )
        sys.exit(1)
    return key


def ask_claude(client: Anthropic, prompt: str, *, model: str = "claude-3-5-sonnet-latest") -> None:
    """Send one prompt to Claude and pretty-print the answer."""
    console.print(Panel(prompt, title="🧑 You ask", border_style="cyan"))

    with console.status("[bold green]Claude is thinking...[/]"):
        response = client.messages.create(
            model=model,
            max_tokens=600,
            system=(
                "You are a senior Forward Deployed Engineer at an AI startup. "
                "Reply briefly, in plain English, with concrete advice. "
                "Use markdown."
            ),
            messages=[{"role": "user", "content": prompt}],
        )

    answer_text = "".join(block.text for block in response.content if block.type == "text")

    console.print(Panel(Markdown(answer_text), title="🤖 Claude", border_style="magenta"))

    # Cost awareness — FDE habit from day 1.
    usage = Table(title="Token usage", show_header=True, header_style="bold yellow")
    usage.add_column("metric", justify="right")
    usage.add_column("value", justify="right")
    usage.add_row("model", model)
    usage.add_row("input tokens", str(response.usage.input_tokens))
    usage.add_row("output tokens", str(response.usage.output_tokens))
    # Sonnet pricing as of 2024-10: $3/MTok input, $15/MTok output
    cost = (response.usage.input_tokens * 3 + response.usage.output_tokens * 15) / 1_000_000
    usage.add_row("est. cost (USD)", f"${cost:.6f}")
    console.print(usage)


def main() -> None:
    api_key = load_api_key()
    client = Anthropic(api_key=api_key)

    prompt = (
        "I'm a Senior PM with 7 years of B2B internal-tools experience, "
        "now sprinting 60 days to become a Forward Deployed Engineer at an AI startup. "
        "Day 1, I just made my first LLM call. "
        "What's the single most important habit I should build this week, "
        "and what trap do most career-switchers fall into?"
    )

    ask_claude(client, prompt)


if __name__ == "__main__":
    main()
