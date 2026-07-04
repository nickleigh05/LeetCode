# Setting Up an Editor

*A comfortable place to write code. Any editor works — this page gets you productive in VS Code, the common default.*

You can solve every problem in this repo in LeetCode's browser editor. But practicing in a real editor pays off: you learn the tools you'll use at an actual job, and you can run and debug locally.

## VS Code (recommended default)

1. Download from <https://code.visualstudio.com> (free, all platforms).
2. Open it, go to the Extensions panel (square icon in the sidebar, or `Ctrl+Shift+X`), and install **Python** (published by Microsoft). That one extension gives you syntax highlighting, error squiggles, autocomplete, and a run button.
3. Open this repo's folder: *File → Open Folder…*
4. Open any `.py` file and click the ▶ button (top right) to run it in the built-in terminal.

Worth adding later, none required:

- **Pylance** — richer autocomplete and type checking (usually installed with the Python extension).
- **Error Lens** — shows errors inline on the line instead of only underlining.
- A formatter (**Black** or **Ruff**) — auto-formats on save so you stop thinking about spacing.

## Useful VS Code habits

| Shortcut | What it does |
|----------|--------------|
| `Ctrl+`` ` | Toggle the built-in terminal |
| `F5` | Run with the debugger (breakpoints work) |
| `Ctrl+P` | Jump to any file by name |
| `Ctrl+/` | Comment/uncomment the selected lines |
| `F2` | Rename a variable everywhere |

Setting a **breakpoint** (click in the gutter left of a line number, then `F5`) and stepping through your solution line by line is the single most underrated learning tool — you *watch* your algorithm run. See [debugging-python](debugging-python.md).

## Alternatives (all fine)

- **PyCharm Community** — heavier, but the best out-of-the-box debugger. Good if VS Code feels too bare.
- **Vim / Neovim** — if you already use it, you know. If you don't, learn DSA first; one steep learning curve at a time.
- **IDLE** — ships with Python. Fine for week one, outgrown quickly.
- **Jupyter / notebooks** — great for experiments, awkward for LeetCode-style functions. Not recommended as the main tool here.

The editor is not the bottleneck — don't spend a weekend configuring. Install VS Code + the Python extension and get back to [the roadmap](../../roadmap.md).

**Related:** [setup-python](setup-python.md) · [terminal-basics](terminal-basics.md) · [debugging-python](debugging-python.md) · [testing-locally](testing-locally.md)
