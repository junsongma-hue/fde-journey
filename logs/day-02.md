# Day 2 — 2026-05-20 (Tue)

> **Theme**: Python core fluency + Git mastery. Less setup, more code.
> **Hours target**: 6h
> **Mood**: _to be filled_

## 🌅 Carry-over from Day 1 — Decision Log

Owner explicitly decided on Day 2 morning to **skip both** carry-over items.
Recording the decision and its rationale for transparency.

- [ ] **Rotate the leaked API key** — DEFERRED
  - Risk: a key that has passed through a third-party LLM service is, by
    industry standard, considered leaked. Real-world risk = low ($30 cap),
    but the missed reflex is the bigger issue.
  - Owner's call: skip. Will revisit when convenient.
- [ ] **Public commitment post** — DEFERRED
  - Risk: without an external audience, the cost of quitting on Day 12
    drops sharply. Plan handbook心法 #4 explicitly leans on this lever.
  - Owner's call: skip. Will revisit at end of W1 if motivation wavers.

To be reviewed at **Sunday W1 retrospective (Day 7)**.

## 📋 Day 2 plan

### Block 1 · 9:00-11:00 (2h) — *Fluent Python* Ch3-4

Read with code in a scratch file, not passively.

- [ ] Ch3 Dictionaries and Sets — focus on:
  - `dict` comprehensions, `dict.setdefault`, `collections.defaultdict`
  - Hashable vs unhashable, why this matters for keys
  - `frozenset` and when you'd use it
- [ ] Ch4 Unicode Text vs Bytes — focus on:
  - `str` vs `bytes` mental model
  - `.encode()` / `.decode()` — when each fails
  - Why `errors='replace'` saves bacon in real APIs

**Deliverable**: `day02/scratch_fluent_py_ch3_4.py` with at least 10 small experiments
showing you understood each concept.

### Block 2 · 11:00-12:00 (1h) — LeetCode warm-up

Solve 5 Easy problems in Python. Idiomatic, not just correct.

- [ ] LC 1 Two Sum (use a dict, O(n))
- [ ] LC 217 Contains Duplicate (set comprehension one-liner)
- [ ] LC 242 Valid Anagram (`collections.Counter`)
- [ ] LC 49 Group Anagrams (`defaultdict(list)`)
- [ ] LC 125 Valid Palindrome (string filtering, two pointers)

Commit them under `day02/leetcode/`.

### Block 3 · 14:00-17:00 (3h) — Git deep dive

Read [Pro Git Ch.3](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell)
and **practice on a throwaway repo**. Don't just read — do.

- [ ] Branch hygiene: create / list / delete / rename
- [ ] **Rebase** (the one PMs are scared of): `git rebase main` from a feature branch
- [ ] **Cherry-pick**: pull one commit from one branch into another
- [ ] **Resolve a merge conflict** intentionally — create one yourself, fix it
- [ ] `git reflog` — your safety net when you screw up rebase
- [ ] `git stash` — save uncommitted work to switch branches

**Deliverable**: `~/workspace/git-playground/` (gitignored from main repo) +
a 300-word note in `logs/day-02-git-notes.md` of "what surprised me".

### Block 4 · 21:00-22:00 (1h) — English + reflection

- [ ] 30 min English podcast (Latent Space latest episode)
- [ ] Fill in this file's reflection sections
- [ ] Plan Day 3 top-3 tasks

## 📊 Time breakdown (fill at end of day)

| activity | hours |
|---|---|
| key rotation + posts | _0.x_ |
| Fluent Python Ch3-4 | _x.x_ |
| LeetCode | _x.x_ |
| Git deep dive | _x.x_ |
| English / reflection | _x.x_ |
| **total** | _x.x_ |

## 💡 Aha moment

_(one sentence — the most surprising thing I learned today)_

## 🚧 Stuck on

_(what blocked me, and how I got past it — or what I'll try tomorrow)_

## 🌅 Top 3 for tomorrow (Day 3)

1. _(decide tonight)_
2. _
3. _

## 📷 Public outputs

- GitHub commits: _link_
- LinkedIn post: _link_
- 即刻 post: _link_
- Blog: _none today_

---

## Reflection (English)

_~150 words, written tonight._

## 反思（中文）

_~150 字，今晚写。_
