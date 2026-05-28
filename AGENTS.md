# AGENTS.md — Working agreement for AI coding agents on this repo

> This file is a contract between the human owner (Joffrey) and any AI
> coding agent (OpenCode, Claude Code, Cursor, etc.) working in this repo.
>
> It borrows philosophy from [obra/superpowers](https://github.com/obra/superpowers)
> but adapts it for a **PM-turning-FDE** who is still learning core
> engineering muscles. Pure Superpowers will be installed at W3 (Day 15+),
> when the flagship project AlphaLens kicks off and the workflow load
> matches the methodology.

---

## Who the human is

- **Joffrey 马俊淞**, 7 years senior PM at a top Chinese tech company
- Self-directed retail US-stock investor (themselves the user of AlphaLens)
- Day 2 of a 60-day public sprint to become a Forward Deployed Engineer
- Currently learning Python and modern AI engineering simultaneously
- **Strengths**: business sense, customer empathy, project execution,
  written communication, financial domain knowledge
- **Gaps to close**: hands-on coding fluency, system design, modern AI
  tooling (Harness engineering, RAG, multi-agent), production deployment

## What this repo is for

A public learning + portfolio repo. Every commit is part of the FDE
interview narrative. Code quality matters more than feature count.
Daily logs in `logs/` are first-class citizens.

---

## How AI agents should work here

These five rules borrow directly from Superpowers but stay light enough
not to break the learning flow.

### 1. Brainstorm before code (`brainstorming`)

**When the human asks for something**, do not immediately produce code.
Instead, ask **at most 2 clarifying questions** when intent is ambiguous.
Then proceed.

**Bad**:
> User: "make a counter function"
> Agent: writes 50 lines of code with bells and whistles

**Good**:
> User: "make a counter function"
> Agent: "Counting what — items in a list, or events over time? And do you
> want top-N results? I'll go with `Counter(items)` if neither matters."

### 2. Plan before multi-step work (`writing-plans`)

For any task that takes more than ~3 distinct actions, **write a todo
list first** using the `todowrite` tool. Show it to the human before
executing. Each item should be 2–5 minutes of work.

### 3. Tests live next to the code (`test-driven-development` lite)

Every Python function shipped here should have at least one self-test.
For learning code (`day0X/` directories), the pattern is:

```python
def main() -> None:
    cases = [...]
    for input, expected in cases:
        got = my_function(input)
        ok = "✅" if got == expected else "❌"
        print(f"{ok}  {input} → {got}")

if __name__ == "__main__":
    main()
```

We do not yet require `pytest` discipline (that's W3+). But every file
should be runnable with `uv run python <file>` and visibly verify itself.

### 4. Debug systematically, not by guessing (`systematic-debugging`)

When the human reports a bug or unexpected behavior:

1. **Reproduce** — actually run the code, observe the output
2. **Diff expectation vs reality** — what they thought would happen vs
   what did
3. **Form a hypothesis**, change one thing, verify
4. **Explain the root cause** in one sentence, not just "it's fixed"

**Forbidden**: making 5 changes at once and saying "try this".

### 5. Verify before claiming done (`verification-before-completion`)

Never say "done" without running the code. If the agent edited a Python
file, the agent runs it. If the agent edited Markdown, the agent reads
it back. If the agent committed, the agent verifies the commit author.

The human caught the agent on Day 1 saying "I changed your .env" without
running the validation script. That's exactly the FDE muscle this rule
builds.

---

## Style preferences

- **Python**: 3.13, uv-managed, ruff-formatted, type-hinted, modern
  syntax (`list[str]` over `List[str]`, `dict | None` over `Optional[dict]`)
- **Async**: prefer `async/await` over callbacks when the human is ready
  for it (currently W1 = no async; W3+ = embrace it)
- **HTTP**: `httpx` over `requests`
- **Models**: Pydantic v2 over dataclasses for any user-facing schema
- **CLI**: `click` for tools, `rich` for output
- **LLM**: Anthropic Claude via the user's aigocode proxy (see `.env`).
  Code must adapt to OpenAI-compatible protocol because that's what the
  proxy speaks.

---

## Repository structure

```
fde-journey/
├── AGENTS.md            ← this file
├── README.md            ← public-facing project intro
├── pyproject.toml       ← uv project manifest
├── .env.example         ← template; real .env is gitignored
├── day01/, day02/, ...  ← daily code drops
├── logs/                ← daily check-ins (Markdown)
├── docs/                ← long-form notes (book summaries, post-mortems)
└── alphalens/           ← (W3+) the flagship project
```

Daily code lives in `dayNN/`. The flagship project gets its own
top-level directory once W3 starts.

---

## Identity & secrets

- This repo's git identity is enforced by `~/.gitconfig` includeIf:
  commits are authored by `junsong.ma@gmail.com`, **never** by
  `majunsong@xiaomi.com`. Agents must verify after committing.
- API keys live in `.env` (gitignored). Never echo a real key in chat
  or commit. The `.env.example` shows placeholder structure.
- The repo is public on GitHub. Any text written into `logs/`, `docs/`,
  or code is assumed visible to recruiters/hiring managers.

---

## What NOT to do

- Don't write code without first checking that the human is in a
  learning moment vs a delivery moment. In learning moments, **explain
  before producing**. In delivery moments, **produce, then explain**.
- Don't introduce a new dependency without asking — `uv add anthropic`
  needs a one-line justification.
- Don't refactor large blocks of the human's own learning code (`dayNN/`)
  without permission. That code is a record of their journey.
- Don't claim "done" or "fixed" without running it.

---

## Roadmap context (so the agent picks defaults wisely)

| Week | Focus | Stack the agent should default to |
|---|---|---|
| W1 (now) | Foundations: Python, Git, LLM API call basics | uv, anthropic SDK via openai-compat proxy, no async |
| W2 | Harness book Ch3-5: Skills, SubAgents, Hooks | Same as W1 + filesystem/glob skills |
| W3 | AlphaLens kickoff: FastAPI + React | + httpx, FastAPI, Pydantic v2, React + Vite, shadcn/ui |
| W4 | RAG: SEC EDGAR + pgvector | + sec-api, pymupdf, pgvector, OpenAI embeddings |
| W5 | Multi-Agent: bull/bear/editor debate | + LangGraph or hand-rolled agent loop |
| W6 | Productionize: SSO, audit, monitoring | + Clerk/Auth0, Langfuse, Sentry |
| W7 | Apply for jobs | (not coding-heavy) |
| W8 | Interview iteration | (depends on feedback) |

If unsure what stack to use for a task, look at the current week and pick
the simplest tool from that row.

---

## When this file gets upgraded to real Superpowers

At **Day 15** (W3 Monday), the human plans to install
`obra/superpowers` properly into OpenCode and migrate from this hand-
rolled AGENTS.md to the full skills marketplace. At that point:

- This file shrinks to a project-specific overlay
- The seven core Superpowers skills (brainstorming, writing-plans, TDD,
  subagent-driven, code-review, systematic-debugging, finishing-branch)
  become mandatory workflows, not lite borrowings
- AlphaLens development uses subagent-driven-development from day one

Until then: keep it light, keep it learning-friendly.

---

*This document is part of the public learning record. Updates and
violations of these rules are themselves committed and explained.*
