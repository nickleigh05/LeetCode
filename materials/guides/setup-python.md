# Installing Python

*Getting Python onto your machine — the very first step, before any lesson.*

Everything in this repo runs on plain Python 3. No packages, no frameworks — if `python3` works in your terminal, you're done. Aim for **Python 3.10 or newer** (LeetCode itself runs a recent 3.x, and a few lessons use `match` which needs 3.10+).

## Check if you already have it

Open a terminal ([what's a terminal?](terminal-basics.md)) and run:

```bash
python3 --version    # macOS / Linux
python --version     # Windows
```

If it prints `Python 3.10` or higher, skip the rest of this page.

## Windows

1. Go to <https://www.python.org/downloads/> and click the big download button.
2. Run the installer. **Check the box that says "Add python.exe to PATH"** — this is the step everyone misses, and without it the terminal can't find Python.
3. Click "Install Now."
4. Open a new PowerShell window and run `python --version` to confirm.

Alternative: install from the Microsoft Store (search "Python"). It auto-updates and handles PATH for you.

> **Gotcha:** if `python` opens the Microsoft Store instead of running Python, search Windows settings for "app execution aliases" and turn off the `python.exe` / `python3.exe` aliases, or just use the Store install.

## macOS

macOS ships with an old or missing Python, so install your own:

```bash
# Option A — Homebrew (recommended if you have it; get it at https://brew.sh)
brew install python

# Option B — installer from https://www.python.org/downloads/
```

Then confirm with `python3 --version`. On macOS the command is `python3`, not `python`.

## Linux

Most distros already ship Python 3. If not:

```bash
sudo apt install python3        # Debian / Ubuntu
sudo dnf install python3        # Fedora
sudo pacman -S python           # Arch
```

## Run your first file

Make a file called `hello.py` containing:

```python
print("hello, leetcode")
```

Then from the folder containing it:

```bash
python3 hello.py     # macOS / Linux
python hello.py      # Windows
```

If you see `hello, leetcode`, your environment works. That one command — *run a `.py` file from the terminal* — is 95% of what this repo ever asks your machine to do.

## The REPL (interactive mode)

Run `python3` with no filename and you get a `>>>` prompt where you can type Python line by line — perfect for testing a one-liner ("what does `-7 // 2` give again?") without making a file. Exit with `exit()` or Ctrl-D (Ctrl-Z then Enter on Windows).

**Related:** [setup-editor](setup-editor.md) · [terminal-basics](terminal-basics.md) · [virtual-environments](virtual-environments.md) · [variables-assignment (syntax)](../syntax/variables-assignment.md)
