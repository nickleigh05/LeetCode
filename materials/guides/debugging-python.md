# Debugging Python

*Reading tracebacks, print-debugging without shame, and stepping through code — the skill that converts "it's broken" into "line 12 is wrong."*

## Read the traceback bottom-up

```
Traceback (most recent call last):
  File "solution.py", line 24, in <module>
    print(s.maxProfit(prices))
  File "solution.py", line 12, in maxProfit
    profit = prices[i + 1] - prices[i]
IndexError: list index out of range
```

The **last line** is what went wrong (`IndexError`) and the line just above it is **where** (`line 12`). Lines above that are the call chain that led there. Start at the bottom, and don't skim the error type — Python's messages are unusually literal. Decode the common ones in [common-python-errors](common-python-errors.md).

## Print debugging (it's legitimate)

Every professional does it. The trick is printing *state*, labeled, at the decision points:

```python
while left < right:
    mid = (left + right) // 2
    print(f"left={left} right={right} mid={mid} nums[mid]={nums[mid]}")  # DEBUG
    ...
```

- Label everything (`f"left={left}"`) — five bare numbers in the output are useless. [f-strings](../syntax/f-strings.md) make this painless; `print(f"{left=}")` even auto-labels.
- Tag the lines `# DEBUG` so you can find and delete them all before submitting — a stray print inside a loop is an instant Output Limit Exceeded on LeetCode.
- For recursion, print an indented trace: `print("  " * depth, node.val)` shows the call tree shape instantly.

Then **trace by hand**: run the failing input on paper, one line at a time, writing variable values. Slow, and it finds the bug more reliably than staring. Comparing your paper trace to the printed trace shows exactly where reality diverges from your mental model — that divergence *is* the bug.

## The real debugger

In VS Code: click left of a line number (red dot = breakpoint), press `F5`, and execution pauses there with every variable visible in the sidebar. `F10` steps to the next line, `F11` steps *into* a function call. Watching a [backtracking](../algorithms/backtracking.md) solution build and unwind its path in the variables panel teaches more than any diagram.

Terminal equivalent: drop `breakpoint()` on any line, run normally, and you land in **pdb** — `n` next line, `s` step in, `p variable` print, `c` continue, `q` quit.

## A five-step method when you're stuck

1. **Reproduce small.** Shrink the failing input to the tiniest case that still fails (`[3,1]` beats a 40-element array).
2. **State your expectation.** "After the first loop, `seen` should be `{2: 0}`." Vague expectations can't be violated.
3. **Check the boundaries first.** Off-by-ones live at loop edges: first iteration, last iteration, empty input, single element. `<` vs `<=`, `range(n)` vs `range(n - 1)`.
4. **Bisect with prints.** One print halfway through the suspect region tells you which half holds the bug. Repeat. (Binary search on your own code.)
5. **Explain it out loud** — to a person, a rubber duck, or an empty room. Verbalizing forces the skipped assumption into the open; the bug is usually in the sentence you say fastest.

**Related:** [common-python-errors](common-python-errors.md) · [testing-locally](testing-locally.md) · [setup-editor](setup-editor.md) · [recursion-basics (syntax)](../syntax/recursion-basics.md)
