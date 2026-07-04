# Competitive Programming I/O

*Reading input and printing output yourself — for Codeforces, AtCoder, USACO, Advent of Code, and any judge that isn't LeetCode.*

LeetCode is unusual: it calls your function and handles all I/O. Almost every other judge hands your program raw text on **stdin** and expects raw text on **stdout**. Same algorithms, different wrapper — this page is the wrapper.

## The standard pattern

A typical problem says: *first line contains n; second line contains n integers.*

```python
import sys
input = sys.stdin.readline          # fast drop-in replacement for input()

n = int(input())
nums = list(map(int, input().split()))

print(max(nums) - min(nums))        # answer goes to stdout, print() is fine
```

The three moves that cover 90% of formats:

```python
x = int(input())                          # one integer on a line
a, b = map(int, input().split())          # two integers, space-separated
grid = [input().strip() for _ in range(r)]  # r lines of a character grid
```

## Why `sys.stdin`?

Built-in `input()` is slow per call; with 10⁶ input lines it alone can TLE. Two standard fixes:

```python
input = sys.stdin.readline                 # ~10x faster, keeps the same shape

data = sys.stdin.read().split()            # nuclear option: slurp every token
idx = 0                                    # then walk an index through them
n = int(data[idx]); idx += 1
```

For heavy *output*, collect lines in a list and print once: `print("\n".join(out))` — a million separate `print` calls is its own TLE.

## Testing locally

Put the sample input in a file and pipe it in ([terminal-basics](terminal-basics.md)):

```bash
python3 solution.py < sample.txt
```

This is exactly what the judge does, so if it works there, format-wise it works everywhere.

## Judge-specific quirks worth knowing

- **Multiple test cases per run** — first line `t`, then t cases; wrap your solve in `for _ in range(t):`. Reset all state each iteration.
- **Read until EOF** (no count given): `for line in sys.stdin:`.
- **`readline()` keeps the trailing `\n`** — harmless for `int()`/`split()`, but `.strip()` strings before comparing.
- **Recursion limits bite harder** off-LeetCode — deep DFS needs [sys.setrecursionlimit](../syntax/recursion-limit.md) or an iterative rewrite.
- **PyPy vs CPython** — Codeforces-style judges often let you submit with PyPy, which runs loop-heavy Python ~10x faster. If both are offered, pick PyPy.
- **USACO (older format)** reads/writes named files: `open("problem.in")` / `open("problem.out", "w")`.

## Where to use this

[Codeforces](https://codeforces.com) (live contests, huge archive), [AtCoder](https://atcoder.jp) (clean problems, beginner-friendly ABC rounds), [USACO](https://usaco.org) (self-paced divisions), [Advent of Code](https://adventofcode.com) (December fun, parse-heavy). All pair well with the [mastery track](../../roadmap.md) — see [whats-next](whats-next.md).

**Related:** [whats-next](whats-next.md) · [terminal-basics](terminal-basics.md) · [recursion-limit (syntax)](../syntax/recursion-limit.md) · [testing-locally](testing-locally.md)
