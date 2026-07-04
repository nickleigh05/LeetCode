# Git & GitHub Basics

*Version control for your solutions — a save-point system for code, and the tool every employer expects you to know.*

**Git** tracks snapshots ("commits") of a folder over time. **GitHub** hosts those snapshots online. For this repo the payoff is simple: your solutions live safely off your laptop, and your GitHub profile becomes visible proof that you've been grinding.

## Install & one-time setup

- **Windows:** <https://git-scm.com/download/win> (accept defaults).
- **macOS:** run `git` in the terminal — it offers to install itself. Or `brew install git`.
- **Linux:** `sudo apt install git` (or your distro's equivalent).

Then introduce yourself (goes into every commit you make):

```bash
git config --global user.name  "Your Name"
git config --global user.email "you@example.com"
```

## The daily loop — four commands

```bash
git status                       # what changed since my last save-point?
git add problems/two_sum.py      # stage it ("include this in the next snapshot")
git add .                        #   …or stage everything changed
git commit -m "Solve Two Sum"    # take the snapshot, with a message
git push                         # upload commits to GitHub
```

That's the whole habit: solve a problem → `add` → `commit` → `push`. Small, frequent commits with messages like "Solve 875 with binary search" beat one giant "updates" commit — six months from now the history *is* your progress log.

## Starting a repo of your own

```bash
cd ~/Projects/my-leetcode
git init                         # start tracking this folder
git add . && git commit -m "First commit"
```

Then on github.com: **New repository** → name it → follow the "push an existing repository" instructions it shows (two `git remote`/`git push` commands to copy-paste). Cloning someone else's repo instead: `git clone <url>`.

## Enough to un-stick yourself

```bash
git log --oneline        # list past commits
git diff                 # exact line-by-line changes not yet staged
git restore file.py      # throw away uncommitted changes to a file (careful!)
git pull                 # download commits (if you work from two machines)
```

- A `.gitignore` file lists junk git should never track — for Python put `__pycache__/`, `*.pyc`, and `.venv/` in it.
- Merge conflicts, branches, rebasing: real topics, none needed for a solo practice repo. `add`/`commit`/`push` covers you for months.
- Golden rule while learning: **commit before experimenting.** A committed state is always recoverable.

**Related:** [terminal-basics](terminal-basics.md) · [setup-editor](setup-editor.md) · [study-plan](study-plan.md)
