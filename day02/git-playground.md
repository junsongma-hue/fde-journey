# Day 2 · Block 3 — Git Deep Dive (3 hours)

> Goal: stop being scared of `rebase`, `cherry-pick`, and merge conflicts.
> Method: do everything on a throwaway repo. Make mistakes on purpose.

## Setup — make a sandbox (5 min)

A fresh repo outside `fde-journey/` so nothing dangerous happens.

```bash
mkdir -p ~/workspace/git-playground
cd ~/workspace/git-playground
git init
echo "# git playground" > README.md
git add . && git commit -m "init"
```

> Note: `~/workspace/git-playground/` is OUTSIDE `~/workspace/fde-journey/`,
> so it'll use your **work email** by default (per `.gitconfig` rules).
> That's fine — this repo is a throwaway.

## Drill 1 — Branches: create / switch / delete (15 min)

```bash
# Create a feature branch and switch to it (modern syntax)
git switch -c feature/login

# Make changes
echo "login" > login.txt
git add . && git commit -m "add login"

# Switch back to main
git switch main

# List branches
git branch                # local
git branch -a             # all (including remote)

# Delete the feature branch (must not be checked out)
git branch -d feature/login    # safe: refuses if unmerged
git branch -D feature/login    # force: delete anyway
```

**Make a mistake on purpose**: try `git branch -d feature/login` while
you're still ON it. Read the error. That's the kind of "obvious but
people-still-do-it" mistake that's good to feel once.

## Drill 2 — `rebase` vs `merge` (30 min)

The thing PMs find scary. Let's demystify it.

### Setup the scenario

```bash
git switch main
echo "v1" > app.txt && git add . && git commit -m "main: v1"

git switch -c feature/x
echo "feature work" > x.txt && git add . && git commit -m "feature: work A"
echo "more work" >> x.txt && git add . && git commit -m "feature: work B"

# Meanwhile, main moves forward
git switch main
echo "v2" >> app.txt && git add . && git commit -m "main: v2"
```

Now the history looks like:

```
main:    A --- B           (v1, v2)
feature:    \-- C --- D    (work A, work B)
```

### Option 1: merge (preserves history exactly)

```bash
git switch feature/x
git merge main             # creates a merge commit
git log --graph --oneline  # see the diamond shape
```

### Option 2: rebase (rewrites feature commits ON TOP of main)

```bash
# Reset to before the merge — practice undoing
git reset --hard HEAD~1    # nukes the merge commit; you can recover via reflog!

git rebase main            # replay C and D as new C', D' on top of main
git log --graph --oneline  # straight line — no diamond
```

**Key insight**:
- `merge` keeps history "true" but messy.
- `rebase` keeps history "linear" but rewritten — DON'T rebase commits
  others have already pulled (you'll force-push and break their world).

## Drill 3 — Resolving a merge conflict (30 min)

```bash
git switch main
echo "main says hello" > greeting.txt && git add . && git commit -m "main: greeting"

git switch -c feature/y
echo "feature says HOWDY" > greeting.txt && git add . && git commit -m "feature: greeting"

git switch main
echo "main says HI" > greeting.txt && git add . && git commit -m "main: revised greeting"

# Now try to merge feature into main — boom, conflict
git merge feature/y
```

You'll see something like:

```
Auto-merging greeting.txt
CONFLICT (content): Merge conflict in greeting.txt
```

Open `greeting.txt`. You'll see conflict markers:

```
<<<<<<< HEAD
main says HI
=======
feature says HOWDY
>>>>>>> feature/y
```

**To resolve**:
1. Edit the file. Pick one side, or merge them by hand.
2. Remove the markers (`<<<<<<<`, `=======`, `>>>>>>>`).
3. `git add greeting.txt`
4. `git commit` (Git pre-fills a merge message; just save).

## Drill 4 — `cherry-pick` (15 min)

"I want just *that* one commit from another branch."

```bash
git switch -c feature/many
echo "fix typo" > typo.txt && git add . && git commit -m "fix typo"
echo "broken" > broken.txt && git add . && git commit -m "broken huge change"
echo "another fix" > fix.txt && git add . && git commit -m "another fix"

git log --oneline       # note the SHA of "fix typo"

git switch main
git cherry-pick <SHA>   # paste the SHA — only that one commit lands here
```

Real-world use: hot-fix on a release branch needs to be backported to main.

## Drill 5 — `reflog` — your safety net (15 min)

The single most underrated Git command. **It's saved careers.**

```bash
git reflog       # shows every HEAD movement in the last 90 days
```

You'll see lines like:

```
abc1234 HEAD@{0}: commit: latest
def5678 HEAD@{1}: reset: moving to HEAD~1
...
```

**The magic**: even if you `git reset --hard` and "lose" a commit, it's
still in the reflog for 90 days. Just `git reset --hard <SHA>` to bring
it back.

Test it:

```bash
git switch main
echo "important" > important.txt && git add . && git commit -m "important work"
git reset --hard HEAD~1     # "oh no, I lost it!"
git log                      # gone from log
git reflog                   # still here!
git reset --hard HEAD@{1}    # recover
git log                      # back!
```

## Drill 6 — `stash` (15 min)

"I'm in the middle of something messy and I need to switch branches NOW."

```bash
echo "WIP work" > wip.txt
git status              # untracked or modified — but you don't want to commit junk

git stash               # saves all changes, restores clean state
git status              # clean

git switch other-branch
# ... do hot-fix stuff ...
git switch original-branch
git stash pop           # bring your WIP back
```

Useful variations:
- `git stash list` — see all stashes
- `git stash save "investigating bug 123"` — give it a name
- `git stash apply` — apply but keep the stash (vs `pop` which removes)

## Wrap-up exercise — write `logs/day-02-git-notes.md`

300 words on:
1. The single most surprising thing today
2. One thing you'll definitely use this month
3. One thing you're still nervous about

Commit it back to `fde-journey`.

## Cheat sheet (keep this)

| I want to... | Command |
|---|---|
| switch branches | `git switch <branch>` |
| create + switch | `git switch -c <branch>` |
| linear history | `git rebase main` (on feature branch) |
| pull one commit | `git cherry-pick <SHA>` |
| undo my last commit, keep changes | `git reset --soft HEAD~1` |
| undo my last commit, nuke changes | `git reset --hard HEAD~1` |
| recover from `--hard` | `git reflog` then `git reset --hard HEAD@{N}` |
| stash WIP | `git stash` / `git stash pop` |
| see history graphically | `git log --graph --oneline --all` |
