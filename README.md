# fde-journey

> A public, day-by-day sprint diary from **7 years Senior PM** to **Forward Deployed Engineer**.
> 60 days. AI/LLM track. Building in public.

| | |
|---|---|
| Start date | 2026-05-19 (Day 1) |
| Target date | 2026-07-13 (Day 60) |
| Daily commitment | 6-8 hours, full weekends, all holidays |
| Track | Python + TypeScript, AI/LLM application engineering |
| Flagship project | **AlphaLens** — AI investment research copilot for retail US-stock investors |

## Why this repo exists

I'm sharing my full learning trajectory in public:

- All code, even the embarrassing first scripts
- Daily check-ins under [`logs/`](./logs)
- Weekly retrospectives, in both English and Chinese
- Three projects, each one feeding directly into the next

If you're a fellow PM-turning-engineer, hopefully this is useful.
If you're a hiring manager looking for FDE candidates — this is my interview.

## Roadmap

```
W1-W2  Foundations   →  llm-cli-buddy   (Day 5 ship)
W3-W4  Full-stack    →  stock-chat      (Day 21 ship)
W5     RAG           →  10k-rag         (Day 28 ship)
W5-W7  Flagship      →  AlphaLens       (Day 46 v1.0)
W7-W8  Apply & ship  →  interviews      (Day 60 results)
```

Detailed plan: [`docs/sprint-plan.md`](./docs/sprint-plan.md) (TBD)

## Stack

- **Language**: Python 3.13 (uv-managed) + TypeScript 5
- **LLM**: Anthropic Claude (primary), with OpenAI / DeepSeek as fallbacks
- **Backend**: FastAPI + PostgreSQL + pgvector
- **Frontend**: React 18 + Vite + shadcn/ui
- **Editor**: Cursor

## Quick start (for me, future me, and the curious)

```bash
# 1. Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Install deps (uv handles venv automatically)
uv sync

# 3. Copy env template and add your API key
cp .env.example .env
# then edit .env

# 4. Say hi to Claude
uv run python day01/hello_llm.py
```

## Daily logs

See [`logs/`](./logs) — one file per day, plus weekly recaps.

## Connect

- Twitter / X: TBD
- LinkedIn: TBD
- Email: junsong.ma@gmail.com
