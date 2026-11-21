# 844. Backspace String Compare

**Easy** · [LeetCode](https://leetcode.com/problems/backspace-string-compare/) · [Solution file (no hints)](../../problems/0500-0999/844.py)

[📖 04. Stack lesson](../learning/04-stack.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 04. Stack problems](../rmap-practice/04-stack.md)

---

Given two strings `s` and `t`, return `True` if they are **equal when both are typed into empty text editors**. `'#'` means a backspace. Backspacing an empty editor leaves it empty.

```
s = "ab#c",  t = "ad#c"  →  True     (both become "ac")
s = "ab##",  t = "c#d#"  →  True     (both become "")
s = "a#c",   t = "b"     →  False    ("c" vs "b")
```

**Constraints:** `1 <= s.length, t.length <= 200` · `s` and `t` contain only lowercase letters and `'#'`

**Follow-up:** can you solve it in O(n) time and **O(1) space**?

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**typed into** a text editor" | Simulate it. Characters go on the end, and `#` removes the **most recent** one |
| `#` is backspace | Last in, first out. That's exactly what a **stack** does |
| backspace on empty "stays empty" | Guard the pop. Never pop an empty stack |
| compare the results | Build both final texts, then check they're equal |
| follow-up: O(1) space | You can't store the results. Walk **backwards**, because that's the direction where you know how many characters to skip |

**Why a stack is the natural model.** Typing pushes a character, and backspace undoes the most recent push. An editor's buffer *is* a stack whose only removal is from the top. Recognising "undo the most recent thing" as a stack is the skill this problem teaches.

**Why the follow-up runs backwards.** Reading left to right, you don't know whether a character survives until you've seen what comes after it. Reading right to left, a `#` tells you to skip the *next* character you meet, and you can keep a "skip" counter as you go. So you can decide character by character without storing anything.

🤔 **Before you open the next section:** if you push letters onto a list and pop when you see `#`, what must you check before popping?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| String rebuilding | `text = text[:-1]` on each `#` | O(n²) | O(n) | ⚠️ Each slice copies the string |
| **Two stacks** | Simulate each editor with a list, compare | **O(n + m)** | O(n + m) | ✅ Clearest |
| Two pointers from the end | Walk both strings backwards with skip counters | O(n + m) | **O(1)** | ✅ Answers the follow-up |

**The decision: a [stack](../data-structures/stack.md) per string.** It's a direct model of the editor, so it's very hard to get wrong. Lead with it, then offer the two-pointer version for the follow-up.

**The O(1)-space version**, so you have it ready:

```python
def next_valid(text, i):
    skip = 0
    while i >= 0:
        if text[i] == '#':
            skip += 1
        elif skip > 0:
            skip -= 1
        else:
            return i          # this character survives
        i -= 1
    return -1

i, j = len(s) - 1, len(t) - 1
while True:
    i, j = next_valid(s, i), next_valid(t, j)
    if i < 0 or j < 0:
        return i < 0 and j < 0   # both exhausted together?
    if s[i] != t[j]:
        return False
    i -= 1
    j -= 1
```

It's the same answer with no buffers, but there are more places to make an off-by-one mistake. Interviewers often accept the stack version and then ask for this one.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
stack1 = []
stack2 = []
```

One stack per editor. A Python list works as a stack: `append` pushes onto the end and `pop()` removes from the end, both O(1).
→ [list-basics](../syntax/list-basics.md) · [list-methods](../syntax/list-methods.md)

```python
for char in s:
    if char == '#':
        if stack1:
            stack1.pop()
    else:
        stack1.append(char)
```

**Type `s` into editor 1.** A letter is pushed. A `#` pops the most recent letter, **but only if there is one**. `if stack1:` relies on an empty list being falsy, which handles "backspace on an empty editor stays empty."

Without that guard, `"#a"` would raise `IndexError: pop from empty list`.
→ [truthy-falsy-values](../syntax/truthy-falsy-values.md) · [elif-else](../syntax/elif-else.md) · [for-loop](../syntax/for-loop.md)

```python
for char in t:
    if char == '#':
        if stack2:
            stack2.pop()
    else:
        stack2.append(char)
```

The same simulation for `t`. If this repetition bothers you, pull it into a helper `build(text)` that returns the list. Two copies are fine for an Easy, though.

```python
return stack1 == stack2
```

List equality compares element by element and length, which is exactly "do the two editors show the same text?"
→ [comparison-operators](../syntax/comparison-operators.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def backspaceCompare(self, s: str, t: str) -> bool:

        stack1 = []
        stack2 = []

        for char in s:
            if char == '#':
                if stack1:
                    stack1.pop()
            else:
                stack1.append(char)

        for char in t:
            if char == '#':
                if stack2:
                    stack2.pop()
            else:
                stack2.append(char)

        return stack1 == stack2
```

</details>

**Trace it.** `s = "ab##"`, `t = "c#d#"`:

| `s` step | char | `stack1` | | `t` step | char | `stack2` |
|---|---|---|---|---|---|---|
| 1 | a | `[a]` | | 1 | c | `[c]` |
| 2 | b | `[a, b]` | | 2 | # | `[]` |
| 3 | # | `[a]` | | 3 | d | `[d]` |
| 4 | # | `[]` | | 4 | # | `[]` |

`[] == []` → **True** ✅.

**An edge case.** `s = "#a"`: the first `#` hits an empty stack and the guard skips the pop, then `a` is pushed. The result is `[a]`.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n + m)</summary>

**O(n + m)**, for `n = len(s)` and `m = len(t)`.

Each character is pushed or popped at most once, and both are O(1). The final comparison is O(min(n, m)) at worst.

**Compare with string slicing:** `text = text[:-1]` copies the whole string each time, so a run of backspaces costs O(n²). The stack avoids that by changing a list in place.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n + m)</summary>

**O(n + m).** In the worst case (no `#` at all) each stack holds its whole string.

**The follow-up gets this to O(1).** The two-pointer version in section 2 stores only indices and skip counters. That's the trade:

| | Time | Space | Risk |
|---|---|---|---|
| **Two stacks** | O(n + m) | O(n + m) | Low: a direct simulation |
| Two pointers backwards | O(n + m) | **O(1)** | Higher: easy to get the end-of-string check wrong |

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "A backspace removes the most recently typed character, which is last-in-first-out, so I'll simulate each editor with a stack. Letters push, `#` pops if the stack isn't empty, then I compare the two stacks. That's O(n + m) time and space. For O(1) space I'd walk both strings from the end with a skip counter: each `#` adds a skip, each letter either uses up a skip or is the next real character, and I compare those characters pairwise."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "O(1) space?" | Two pointers from the end with skip counters, as in section 2. |
| "Why go backwards?" | Going forwards, you can't tell whether a character survives until you've seen what follows it. Going backwards, every `#` you meet applies to the characters you're about to see. |
| "What about other editing keys, like undo?" | Still a stack. Undo means keeping a second stack of operations, the classic editor design. |
| "Return the final string?" | `''.join(stack1)`. |

**Traps:**

- **Popping an empty stack.** `"#a"` or `"##"` crash without the guard.
- **Rebuilding the string with slices.** O(n²) on backspace-heavy inputs.
- **In the two-pointer version, returning `True` when only one string is exhausted.** You need `i < 0 and j < 0` together.
- **Forgetting that the `#` itself is never kept.** It's an action, not a character.

**This same move shows up in:** [Valid Parentheses](20-valid-parentheses.md) (push, then pop the most recent match) · [Simplify Path](71-simplify-path.md) (`..` pops a directory the way `#` pops a letter) · [Baseball Game](682-baseball-game.md) (`"C"` cancels the last score) · [Asteroid Collision](735-asteroid-collision.md) (new items destroy the top of the stack).

</details>

---
