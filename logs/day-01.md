# Day 1 — 2026-05-19 (Mon)

> **Theme**: Setup the entire toolchain end-to-end. PM mindset off, FDE mindset on.
> **Hours invested**: ~5h
> **Mood**: Energized. The whole loop closed faster than I expected.

## ✅ Done today

- [x] Verified dev environment (Python 3.14, Node 25, Git, Homebrew, pnpm)
- [x] Installed `uv` and added it to zsh PATH
- [x] Set up dual-identity Git: `~/workspace/fde-journey/` uses Gmail, everywhere else stays on the work email (`includeIf` in `~/.gitconfig`)
- [x] Generated dedicated `id_ed25519_github` SSH key, added to GitHub, verified `ssh -T git@github.com`
- [x] Bootstrapped `fde-journey` uv project (Python 3.13, ruff, pytest, anthropic, openai, dotenv, rich)
- [x] Wrote `day01/hello_python.py` — toy portfolio analytics; exercises dataclasses, comprehensions, context managers
- [x] Wrote `day01/hello_llm.py` v2 — **dual-protocol** LLM client: auto-adapts between native Anthropic API and OpenAI-compatible proxies
- [x] First successful LLM call through proxy (claude-opus-4-7 via aigocode)
- [x] Pushed to GitHub: https://github.com/junsongma-hue/fde-journey *(after manual repo creation)*
- [ ] Posted public commitment on LinkedIn / 即刻 *(tonight)*

## 📊 Time breakdown

| activity | hours |
|---|---|
| environment & Git identity isolation | 1.0 |
| Python warm-up code (hello_python.py) | 1.0 |
| LLM API integration + dual-protocol refactor | 1.5 |
| writing / docs / commits | 1.0 |
| reflection & planning | 0.5 |
| **total** | **5.0** |

## 💡 Aha moment

The shift from "PM Brain" to "FDE Brain" is concrete: it's the difference between *describing a system* and *being accountable for one running*. Claude nailed it on the first call — the trap is substituting communication for technical understanding. I will print that quote and put it on my desk.

## 🚧 Stuck on

Nothing major today. The closest thing to friction was deciding which LLM provider to use given my proxy access pattern — but turning that question into a generic adapter (LLM_PROTOCOL env var) actually became the most senior-engineer-feeling commit of the day. PM tendency to "design the abstraction first" actually paid off here, instead of being a trap.

## 🌅 Top 3 for tomorrow (Day 2)

1. *Fluent Python* chapters 3-4 (dicts, sets, text encoding) — read with code in a scratch file, no passive reading
2. Git deep dive: rebase, cherry-pick, merge conflicts (Pro Git ch. 3) — practice on a throwaway repo
3. LeetCode Easy × 5 in Python, focusing on idiomatic comprehensions and `collections.Counter`

## 📷 Public outputs

- GitHub: https://github.com/junsongma-hue/fde-journey
- Latest commit: `1d6bc24 Day 1: dual-protocol LLM client (Anthropic + OpenAI-compatible)`
- LinkedIn: *(posting tonight)*
- 即刻: *(posting tonight)*
- Blog: *(none today — Day 5 plan)*

---

## Reflection (English)

Day 1 wasn't about learning a new framework or solving a hard problem. It was about removing every excuse: dual Git identity so I never accidentally commit to the wrong remote; uv so dependencies never bite me again; a dual-protocol LLM adapter so I can swap providers without rewriting my code. The whole point was to make tomorrow frictionless, so I spend zero seconds on setup and 100% on the actual work.

The most surprising thing: I expected the first LLM call to feel magical. It didn't. It felt *normal* — like calling any other API. That's the right feeling. Magic is a tutorial trap; routine is engineering.

Tomorrow the easy stuff is over. Time to actually build muscle memory.

## 反思（中文）

今天没学新框架，没解难题。今天做的是**清障**：双 Git 身份让我不会手滑提交到错误的远端；uv 让依赖管理再也不会卡我；双协议 LLM 适配让我换供应商不用重写代码。一切就为了让明天开工的摩擦力归零。

最意外的是：我以为第一次调通 LLM 会有魔法感。其实没有。就像调一个普通 API 一样。这才是对的。魔法感是教程陷阱，工程师对自己的工具应该是"日常化"的感觉。

最受用的一句话来自 Claude 自己的回答："The transition from PM to FDE isn't about learning to code — it's about shifting from describing systems to being accountable for systems running."（PM 转 FDE 不是学会写代码，是从描述系统转变为对运行中的系统负责。）

明天起，简单的活儿干完了。该练肌肉了。
