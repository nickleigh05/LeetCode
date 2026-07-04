# Terminal Basics

*The text window where you run programs. Ten commands cover everything this repo needs.*

The **terminal** (also called shell, command line, or console) is a program where you type commands instead of clicking. You need it for exactly three things here: navigating to a folder, running Python files, and using [git](git-basics.md).

## Opening one

- **Windows:** Start menu → "PowerShell" (or "Terminal" on Windows 11).
- **macOS:** Spotlight (`Cmd+Space`) → "Terminal."
- **Linux:** you likely know; usually `Ctrl+Alt+T`.
- **Any OS:** VS Code has one built in — `` Ctrl+` `` — already opened at your project folder. Honestly the easiest option.

## The commands that matter

```bash
pwd             # "print working directory" — where am I?
ls              # list files here            (Windows PowerShell: also ls, or dir)
cd problems     # move into the folder named problems
cd ..           # move up one level
cd ~            # jump to your home folder
mkdir practice  # make a new folder
python3 two_sum.py   # run a Python file     (Windows: python two_sum.py)
```

That's genuinely most of it. A few quality-of-life tricks:

- **Tab completion** — type the first letters of a file/folder and press `Tab`; the terminal finishes the name. Use it constantly, it also prevents typos.
- **↑ arrow** — cycles through previous commands, so you never retype `python3 solution.py`.
- **`Ctrl+C`** — kills the currently running program. Your infinite [while loop](../syntax/while-loop.md) will make you need this.
- **Drag a folder onto the terminal window** — pastes its full path (handy for `cd`).

## Reading a path

```
/home/nick/Projects/LeetCode/problems/two_sum.py     ← macOS / Linux
C:\Users\nick\Projects\LeetCode\problems\two_sum.py  ← Windows
```

An **absolute path** starts from the root (`/` or `C:\`) and works from anywhere. A **relative path** (`problems/two_sum.py`) is relative to where you currently are (`pwd`). If Python says `No such file or directory`, you're almost always in the wrong folder — run `pwd` and `ls` to see where you actually are.

## What the `$` means in guides

Documentation writes `$ python3 hello.py` to mean "type this at the prompt." You don't type the `$` — it just marks the line as a command rather than output.

**Related:** [setup-python](setup-python.md) · [git-basics](git-basics.md) · [virtual-environments](virtual-environments.md) · [competitive-programming-io](competitive-programming-io.md)
