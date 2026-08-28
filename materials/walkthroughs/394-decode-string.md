# 394. Decode String

**Medium** · [LeetCode](https://leetcode.com/problems/decode-string/) · [Solution file (no hints)](../../problems/0001-0499/394.py)

[📖 04. Stack lesson](../learning/04-stack.md) · [📖 Recursion](../learning/04b-recursion.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 04. Stack problems](../rmap-practice/04-stack.md)

---

Given an encoded string, return its decoded form. The rule is `k[encoded_string]`, meaning the string inside the brackets repeats exactly `k` times. Input is always valid, `k` is a positive integer, and the original data contains no digits.

```
s = "3[a]2[bc]"      →  "aaabcbc"
s = "3[a2[c]]"       →  "accaccacc"
s = "2[abc]3[cd]ef"  →  "abcabccdcdcdef"
```

**Constraints:** `1 <= s.length <= 30` · lowercase letters, digits, `[`, `]` · input is valid · `1 <= k <= 300`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| `k[...]` can **nest** | ⚠️ `3[a2[c]]` — the inner group must resolve before the outer can repeat. That's a recursive structure |
| "input is always **valid**" | Brackets are balanced; no error handling needed |
| `1 <= k <= 300` | ⚠️ **`k` can be multi-digit.** `12[a]` means twelve, not one-then-two |
| "original data has **no digits**" | So any digit you see is part of a repeat count, never literal content |
| output ≤ 10⁵ | Decoding can expand enormously — `s` is ≤ 30 chars but the result can be huge |

**The shape of the problem:** nesting means you must *suspend* work on the outer group while resolving the inner one, then resume with the outer context restored. "Suspend, do something else, resume the most recent thing" is exactly LIFO.

Walk `3[a2[c]]` and watch what needs remembering:

```
3[a2[c]]
│
├─ see 3, then '['  → suspend: remember (count=3, text so far="")
│  ├─ build "a"
│  ├─ see 2, then '[' → suspend: remember (count=2, text so far="a")
│  │  ├─ build "c"
│  │  └─ see ']' → resume: "a" + 2×"c" = "acc"
│  └─ see ']' → resume: "" + 3×"acc" = "accaccacc"
```

At each `[` you push **two** things: the repeat count, and the text accumulated *before* the bracket. At each `]` you pop them and combine.

That's the whole algorithm. The only real subtlety is remembering that the *prefix* must be saved too — not just the count.

🤔 **Before you open the next section:** when you hit `]` and repeat the inner text `k` times, what do you need to prepend to it — and where did that come from?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Repeated regex substitution | Find innermost `k[...]`, expand, repeat | O(n · output) | O(output) | ⚠️ Works, but re-scans repeatedly and is fiddly |
| **Two stacks** | Push count + prefix at `[`, pop and combine at `]` | **O(output)** | O(output) | ✅ |
| Recursion | Recursive descent with an index pointer | O(output) | O(depth) stack | ✅ Equally good; mirrors the grammar |

**The decision: two stacks — one for counts, one for accumulated prefixes.**

Track a `current` string and a `current_number`, plus two stacks. Four cases per character:

| Character | Action |
|---|---|
| **digit** | `num = num * 10 + int(ch)` — build a possibly multi-digit number |
| **`[`** | push `num` and `current`; reset both to empty |
| **`]`** | pop count `k` and prefix `prev`; `current = prev + k * current` |
| **letter** | `current += ch` |

**Why two stacks and not one.** At `]` you need *both* the repeat count and the text that preceded the bracket. Bundling them into one stack of tuples works equally well — `stack.append((num, current))` — and is arguably cleaner. Two parallel stacks is the more common presentation; either is fine as long as they stay in lockstep.

**Why the prefix must be saved.** This is the step people miss. In `"2[abc]3[cd]ef"`, when the second `]` is reached, `current` holds `"cd"` — but the already-decoded `"abcabc"` must be preserved and prepended. Saving `current` at each `[` and restoring it at each `]` is what keeps sibling groups from clobbering each other.

**Why `num * 10 + digit`.** Digits arrive one at a time, so `12[a]` gives you `1` then `2`. The standard accumulation `num = num*10 + int(ch)` builds 12. Treating each digit as a separate count would decode `12[a]` as `1[2[a]]`-ish nonsense — a very common bug given that most test cases use single digits and hide it.

**Recursion is equally valid.** The grammar is genuinely recursive, and a recursive-descent parser with a shared index reads beautifully. The stack version is just the same thing with the call stack made explicit. Since `s.length <= 30`, nesting depth is tiny and there's no overflow concern. Mention both; the iterative one is easier to demonstrate correctness on a whiteboard.

**Why not repeated regex?** `re.sub(r'(\d+)\[([a-z]*)\]', ...)` applied until stable does work, expanding innermost groups outward. But it re-scans the whole string each round and the complexity is awkward to state. The stack does it in one pass.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
count_stack = []
string_stack = []
current = ""
num = 0
```

- `count_stack` — repeat counts awaiting their `]`
- `string_stack` — text accumulated *before* each `[`
- `current` — the string being built at the current nesting level
- `num` — the repeat count being parsed digit by digit

→ [list-basics](../syntax/list-basics.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
for ch in s:
    if ch.isdigit():
        num = num * 10 + int(ch)
```

**Accumulate multi-digit numbers.** Each new digit shifts the existing value left one decimal place. `1` then `2` → `1*10+2` = 12.
→ [string-methods](../syntax/string-methods.md) · [type-conversion](../syntax/type-conversion.md)

```python
    elif ch == '[':
        count_stack.append(num)
        string_stack.append(current)
        num = 0
        current = ""
```

**Suspend the current level.** Save both the count and everything built so far, then start fresh for the inner group.

Resetting **both** `num` and `current` is essential — the inner group needs a clean slate, and the outer context is safely stored.
→ [list-methods](../syntax/list-methods.md)

```python
    elif ch == ']':
        k = count_stack.pop()
        prev = string_stack.pop()
        current = prev + current * k
```

**Resume the outer level.** Pop the matching count and prefix, repeat the inner text `k` times, and append it to the prefix.

`current * k` is Python's string repetition. Order matters: `prev + current * k`, not `current * k + prev` — the prefix came first in the input.

Because pops are LIFO, they always pair with the *matching* `[` even when deeply nested — no bracket-matching bookkeeping needed.
→ [string-basics](../syntax/string-basics.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
    else:
        current += ch
```

**A literal letter** — append it to the current level's text.

```python
return current
```

All brackets are closed, so `current` holds the fully decoded string.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def decodeString(self, s: str) -> str:

        count_stack = []
        string_stack = []
        current = ""
        num = 0

        for ch in s:
            if ch.isdigit():
                num = num * 10 + int(ch)

            elif ch == '[':
                count_stack.append(num)
                string_stack.append(current)
                num = 0
                current = ""

            elif ch == ']':
                k = count_stack.pop()
                prev = string_stack.pop()
                current = prev + current * k

            else:
                current += ch

        return current
```

</details>

**Trace the nested case** — `s = "3[a2[c]]"`:

| `ch` | Action | `num` | `current` | `count_stack` | `string_stack` |
|---|---|---|---|---|---|
| `3` | digit | 3 | `""` | `[]` | `[]` |
| `[` | push 3 and `""`; reset | 0 | `""` | `[3]` | `[""]` |
| `a` | append | 0 | `"a"` | `[3]` | `[""]` |
| `2` | digit | 2 | `"a"` | `[3]` | `[""]` |
| `[` | push 2 and `"a"`; reset | 0 | `""` | `[3, 2]` | `["", "a"]` |
| `c` | append | 0 | `"c"` | `[3, 2]` | `["", "a"]` |
| `]` | pop 2, `"a"` → `"a" + "c"*2` | 0 | `"acc"` | `[3]` | `[""]` |
| `]` | pop 3, `""` → `"" + "acc"*3` | 0 | `"accaccacc"` | `[]` | `[]` |

Return **`"accaccacc"`** ✅

**And the sibling-groups case** — `s = "2[abc]3[cd]ef"`:

| `ch` | `current` after | Note |
|---|---|---|
| `2[abc]` | `"abcabc"` | first group resolved |
| `3` `[` | `""` | pushes `"abcabc"` as the prefix ⭐ |
| `cd` | `"cd"` | |
| `]` | `"abcabc" + "cd"*3` = `"abcabccdcdcd"` | prefix restored |
| `ef` | `"abcabccdcdcdef"` | trailing literals |

Return **`"abcabccdcdcdef"`** ✅

The starred step is why the prefix stack exists — without it, `"abcabc"` would be lost when the second group starts.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(output length)</summary>

**O(m)** where `m` is the length of the **decoded output** — not the input.

That distinction matters here. The input is at most 30 characters, but `"300[300[ab]]"`-style nesting expands enormously (the problem caps the output at 10⁵ precisely because of this).

Where the work goes:

- One pass over `s` — O(n) character dispatches
- Each `]` performs `current * k`, which copies `k × len(current)` characters

Summed across all groups, the total character-copying is proportional to the final output size — each character of the result is produced once by the repetition that creates it, though nested repetitions do copy inner results again as they're multiplied outward.

**A precise bound:** O(m) for a single level of nesting, and O(m · d) in the worst case for depth `d`, since each nesting level can re-copy the accumulated string. With `n <= 30` the depth is at most ~15, so this is comfortably fast in practice.

**Compare to repeated regex substitution:** each round re-scans the whole (growing) string, giving a worse constant and a messier bound. One pass wins.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(output length)</summary>

**O(m)** — dominated by the decoded string itself, which you must build.

Breaking it down:

- `current` and the final result — up to O(m)
- `string_stack` — holds prefixes from each open bracket; their combined length is bounded by O(m)
- `count_stack` — O(d), one integer per nesting level

The output is inherently O(m), so that's the floor.

**Recursion comparison:** a recursive parser uses O(d) call-stack frames instead of the two explicit stacks — asymptotically similar, since `d ≤ n`. With `n ≤ 30` neither is a concern, but for adversarially deep nesting the iterative version avoids any recursion-limit risk. See [recursion-limit](../syntax/recursion-limit.md).

**One Python note:** `current += ch` in a loop is O(n²) in general because strings are [immutable](../syntax/string-immutability.md). For `n ≤ 30` it's irrelevant, but the scalable form accumulates into a list and joins:

```python
current = []          # instead of ""
current.append(ch)    # instead of +=
...
current = list(prev) + current * k
```

Mention it if asked about very large inputs; don't complicate the code for this problem's constraints.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The encoding nests, so when I hit an inner `k[...]` I need to suspend work on the outer group and resume it afterwards — that's LIFO, so a stack. I keep a `current` string and a `num` being parsed. On a digit I do `num = num*10 + digit`, since `k` can be multi-digit. On `[` I push both the count **and** the text accumulated so far, then reset both — saving the prefix is the step people forget, and it's what keeps sibling groups from clobbering each other. On `]` I pop the count and prefix and set `current = prefix + current * k`. Letters just append. Because pops are LIFO they automatically pair with the matching bracket. O(output) time and space. A recursive-descent parser is equally natural — the stack version is just the call stack made explicit."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "What if `k` is multi-digit?" | **Already handled** — `num = num*10 + int(ch)`. Treating each digit separately is the classic bug. |
| "Solve it recursively." | Recursive descent with a shared index: parse a number, expect `[`, recurse until `]`, return `k * inner`. Same complexity, O(d) call stack. |
| "Why save `current` at `[`?" | Sibling groups. In `2[abc]3[cd]`, the second group must not lose `"abcabc"`. |
| "What if the input could be **invalid**?" | Check the stacks are non-empty before popping, and that they're empty at the end. The problem guarantees validity. |
| "Encode a string (the inverse)?" | Much harder — finding the optimal compression is a DP problem ([LeetCode 471](https://leetcode.com/problems/encode-string-with-shortest-length/)). |
| "Handle nested counts like `2[3[a]]`?" | Already works — that's exactly what the trace demonstrates. |
| "What if output could be enormous?" | Accumulate into lists and `join`, or return a lazy/generator representation rather than materializing the string. |

**Traps:**

- **Not accumulating multi-digit numbers.** `12[a]` decodes wrongly. Single-digit test cases hide this.
- **Forgetting to push `current` at `[`.** Sibling groups overwrite each other — `"2[abc]3[cd]ef"` exposes it.
- **Forgetting to reset `current` and `num` after pushing.** The inner group inherits the outer's text and count.
- **Wrong concatenation order.** It's `prev + current * k`; reversing puts the prefix after the repeated block.
- **Using one stack for both** without pairing the values. Fine if you push tuples; broken if the two get out of sync.
- **Assuming brackets need explicit matching.** The stack's LIFO discipline handles it for free.

**This same move shows up in:** [Valid Parentheses](20-valid-parentheses.md) (the LIFO bracket-matching primitive underneath) · [Simplify Path](71-simplify-path.md) (a stack tracking nested context) · [Basic Calculator](https://leetcode.com/problems/basic-calculator/) (the same suspend/resume pattern with signs and parentheses) · [Generate Parentheses](22-generate-parentheses.md) (recursive structure over bracket grammars).

</details>

---
