# Virtual Environments & pip

*Installing Python packages without making a mess. Optional for this repo — essential knowledge for everything after it.*

**You don't need this for LeetCode.** Every solution here uses only the standard library. But the first time you want `pytest`, `sortedcontainers`, or any other package, do it the right way — inside a virtual environment.

## The problem it solves

`pip install` normally installs packages globally, shared by every project on your machine. Two projects needing different versions of the same package then fight, and on Linux/macOS you can even break system tools. A **virtual environment (venv)** is a private, disposable copy of Python per project — packages installed there stay there.

## The recipe

```bash
cd ~/Projects/LeetCode

python3 -m venv .venv              # 1. create it (once) — makes a .venv/ folder

source .venv/bin/activate          # 2. activate it (each session) — macOS/Linux
.venv\Scripts\activate             #    …or on Windows PowerShell

pip install pytest sortedcontainers  # 3. install whatever you want

deactivate                         # 4. leave when done (or just close the terminal)
```

While active, your prompt shows `(.venv)` and `python` / `pip` refer to the private copy. VS Code usually detects `.venv` automatically and offers to use it — say yes.

## Packages actually worth knowing for DSA practice

- **`sortedcontainers`** — `SortedList`, the "ordered set with O(log n) insert" Python's stdlib lacks. LeetCode has it pre-installed, so learning it is directly useful. See [sorted-list (data-structures)](../data-structures/sorted-list.md).
- **`pytest`** — nicer test running than raw [asserts](../syntax/assert-statement.md). See [testing-locally](testing-locally.md).

That's about it. If a DSA tutorial has you installing numpy/pandas, it's not teaching you DSA.

## Odds and ends

- `.venv` is a junk folder you can delete and recreate anytime; never commit it (add `.venv/` to `.gitignore`).
- `pip list` shows what's installed in the active environment; `pip freeze > requirements.txt` snapshots it.
- `python3 -m pip install …` is a safer spelling of `pip install …` — it guarantees the pip matches the python.
- Seeing `error: externally-managed-environment` on Linux/macOS? That's the OS protecting global Python — it's telling you to use a venv, i.e. exactly this page.

**Related:** [setup-python](setup-python.md) · [terminal-basics](terminal-basics.md) · [testing-locally](testing-locally.md) · [import-basics (syntax)](../syntax/import-basics.md)
