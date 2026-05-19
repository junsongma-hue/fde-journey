"""
Day 1 - First LLM call. Hello, Claude (via proxy or direct).

This script auto-adapts to two common protocols:

  • LLM_PROTOCOL=anthropic  → uses the official Anthropic SDK
                              (works with anthropic.com directly OR an
                               Anthropic-format proxy that exposes /v1/messages)

  • LLM_PROTOCOL=openai     → uses the OpenAI SDK pointed at any
                              OpenAI-compatible endpoint (oneapi, newapi,
                              openrouter, deepseek, custom proxies, etc.)

Goal: prove the whole loop end-to-end and start building cost awareness.

Run me with:    uv run python day01/hello_llm.py
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass

from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

console = Console()


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
@dataclass
class LLMConfig:
    protocol: str  # "anthropic" or "openai"
    api_key: str
    base_url: str  # may be empty string for direct Anthropic
    model: str


def load_config() -> LLMConfig:
    """Read .env and validate. Fail fast with a friendly message."""
    load_dotenv()

    protocol = os.getenv("LLM_PROTOCOL", "").strip().lower()
    api_key = os.getenv("LLM_API_KEY", "").strip()
    base_url = os.getenv("LLM_BASE_URL", "").strip()
    model = os.getenv("LLM_MODEL", "").strip()

    problems: list[str] = []
    if protocol not in ("anthropic", "openai"):
        problems.append(f"LLM_PROTOCOL must be 'anthropic' or 'openai' (got '{protocol}')")
    if not api_key or "your-" in api_key or api_key.startswith("sk-ant-xxx"):
        problems.append("LLM_API_KEY is empty or still a placeholder")
    if protocol == "openai" and not base_url:
        problems.append("LLM_BASE_URL is required when LLM_PROTOCOL=openai")
    if not model:
        problems.append("LLM_MODEL is empty (e.g. claude-3-5-sonnet-20241022)")

    if problems:
        bullet = "\n".join(f"  • {p}" for p in problems)
        console.print(
            Panel.fit(
                f"[bold red]Config issues:[/]\n{bullet}\n\n"
                "Fix [cyan].env[/] (start from [cyan].env.example[/]) and try again.",
                title="Setup needed",
                border_style="red",
            )
        )
        sys.exit(1)

    return LLMConfig(protocol=protocol, api_key=api_key, base_url=base_url, model=model)


# ---------------------------------------------------------------------------
# Two protocol adapters — same input, same output shape
# ---------------------------------------------------------------------------
@dataclass
class LLMResult:
    text: str
    input_tokens: int
    output_tokens: int


def call_anthropic(cfg: LLMConfig, system: str, user: str) -> LLMResult:
    """Call Anthropic native API (direct or via Anthropic-format proxy)."""
    from anthropic import Anthropic

    kwargs: dict = {"api_key": cfg.api_key}
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url

    client = Anthropic(**kwargs)
    response = client.messages.create(
        model=cfg.model,
        max_tokens=600,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    text = "".join(b.text for b in response.content if b.type == "text")
    return LLMResult(
        text=text,
        input_tokens=response.usage.input_tokens,
        output_tokens=response.usage.output_tokens,
    )


def call_openai_compatible(cfg: LLMConfig, system: str, user: str) -> LLMResult:
    """Call any OpenAI-format endpoint (oneapi/newapi/openrouter/deepseek/...)."""
    from openai import OpenAI

    client = OpenAI(api_key=cfg.api_key, base_url=cfg.base_url)
    response = client.chat.completions.create(
        model=cfg.model,
        max_tokens=600,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    text = response.choices[0].message.content or ""
    usage = response.usage
    return LLMResult(
        text=text,
        input_tokens=usage.prompt_tokens if usage else 0,
        output_tokens=usage.completion_tokens if usage else 0,
    )


def ask_llm(cfg: LLMConfig, prompt: str) -> None:
    system = (
        "You are a senior Forward Deployed Engineer at an AI startup. "
        "Reply briefly, in plain English, with concrete advice. Use markdown."
    )

    console.print(Panel(prompt, title="🧑 You ask", border_style="cyan"))
    console.print(
        f"[dim]protocol={cfg.protocol}  model={cfg.model}  "
        f"base_url={cfg.base_url or '(default Anthropic)'}[/dim]"
    )

    with console.status("[bold green]LLM is thinking...[/]"):
        if cfg.protocol == "anthropic":
            result = call_anthropic(cfg, system, prompt)
        else:
            result = call_openai_compatible(cfg, system, prompt)

    console.print(Panel(Markdown(result.text), title="🤖 LLM", border_style="magenta"))

    # Cost awareness — Sonnet pricing as a rough yardstick.
    table = Table(title="Token usage", show_header=True, header_style="bold yellow")
    table.add_column("metric", justify="right")
    table.add_column("value", justify="right")
    table.add_row("model", cfg.model)
    table.add_row("input tokens", str(result.input_tokens))
    table.add_row("output tokens", str(result.output_tokens))
    est = (result.input_tokens * 3 + result.output_tokens * 15) / 1_000_000
    table.add_row("est. cost @ Sonnet rate (USD)", f"${est:.6f}")
    console.print(table)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    cfg = load_config()
    prompt = (
        "I'm a Senior PM with 7 years of B2B internal-tools experience, "
        "now sprinting 60 days to become a Forward Deployed Engineer at an AI startup. "
        "Day 1, I just made my first LLM call through a proxy. "
        "What's the single most important habit I should build this week, "
        "and what trap do most career-switchers fall into?"
    )
    ask_llm(cfg, prompt)


if __name__ == "__main__":
    main()
