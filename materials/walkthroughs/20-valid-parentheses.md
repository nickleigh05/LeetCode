# 20. Valid Parentheses

**Easy** · [LeetCode](https://leetcode.com/problems/valid-parentheses/) · [Solution file (no hints)](../../problems/0001-0499/20.py)

[📖 04. Stack lesson](../learning/04-stack.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 04. Stack problems](../rmap-practice/04-stack.md)

---

Given a string `s` containing only the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input is **valid**.

A string is valid if:
1. Open brackets are closed by the **same type** of bracket, and
2. Open brackets are closed in the **correct order**.

```
"()"        →  true
"()[]{}"    →  true
"(]"        →  false    (wrong type)
"([)]"      →  false    (wrong order — interleaved, not nested)
"([])"      →  true
```

**Constraints:** `1 <= s.length <= 10⁴` · `s` consists only of those six bracket characters

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "same **type** of bracket" | Counting alone is insufficient — you must remember *which kind* is open |
| "closed in the **correct order**" | ⚠️ The real requirement: brackets must be properly **nested**. `"([)]"` has equal counts of everything and is still invalid |
| three bracket types | Three independent counters won't work either — `"([)]"` passes all three |
| n up to 10⁴ | O(n) is trivially achievable |
| the string can be **odd-length** | Then it can't possibly balance — a free early exit |

The example that kills every naive approach is `"([)]"`. Counts are balanced. Each type appears exactly once open and once closed. It's *still* invalid, because the brackets interleave rather than nest.

So what does correct nesting actually mean? Look at `"([{}])"` and ask: when you meet `'}'`, which bracket must it close? The `'{'` — the **most recently opened** one still waiting. Not the first, not any other. Always the most recent.

> **The bracket that opened last must close first.**

That's the literal definition of **LIFO** — last in, first out — which is a [stack](../data-structures/stack.md).

🤔 **Before you open the next section:** when you encounter a closing bracket, which of the currently-open brackets is the *only* one it's allowed to match? What structure gives you that one in O(1)?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Count each type | Three counters, check they balance | O(n) | ❌ `"([)]"` passes. Ignores order entirely |
| Repeatedly delete pairs | Strip `"()"`, `"[]"`, `"{}"` until nothing changes | O(n²) | ⚠️ Correct but quadratic — each pass rescans |
| Recursion | Parse nested groups recursively | O(n) | ⚠️ Works; the call stack is just an implicit stack |
| **Stack** | Push opens, match closes against the top | **O(n)** | ✅ |

**The decision: a [stack](../data-structures/stack.md) of unmatched opening brackets.**

- **Opening bracket** → push it. It's now waiting to be closed.
- **Closing bracket** → it must match the top of the stack. If it does, pop (that pair is resolved). If not — or if the stack is empty — the string is invalid.
- **At the end** → the stack must be empty. Anything left is an unclosed bracket.

**Why a stack is the *exact* fit, not just a workable one.** The nesting requirement and the LIFO discipline are the same rule stated two ways. Correctly nested brackets are precisely those a stack can consume. That's why this problem is the canonical stack introduction — the data structure isn't a clever choice, it's the direct encoding of the problem's definition.

**Note the two failure modes**, which are easy to conflate:

- `")("` — a closing bracket arriving with an **empty stack**. Caught during the loop.
- `"(("` — leftovers on the stack at the **end**. Caught by the final check.

You need both. Handling only one is the most common incomplete solution.

**The general signal:** whenever a problem involves *matching, nesting, or "the most recent unresolved thing"*, reach for a stack. See the [Stack lesson](../learning/04-stack.md).

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
stack = []
pairs = {")": "(", "]": "[", "}": "{"}
```

A Python list used as a stack — `.append()` pushes, `.pop()` removes from the end, both O(1).

`pairs` maps each **closing** bracket to its opening partner. Keying by the closer is a deliberate choice: it lets one `in` test answer *"is this a closing bracket?"* **and** retrieve what it must match.
→ [list-basics](../syntax/list-basics.md) · [dict-basics](../syntax/dict-basics.md) · [stack](../data-structures/stack.md)

```python
for char in s:
    if char in pairs:
```

`char in pairs` checks the dict's **keys**, which are exactly the three closing brackets. So this reads as *"is this a closer?"* — and if not, it must be an opener, since the constraints promise only these six characters.
→ [for-loop](../syntax/for-loop.md) · [membership-operators](../syntax/membership-operators.md)

```python
        if stack and stack[-1] == pairs[char]:
            stack.pop()
```

A closing bracket. Two conditions must hold, and the order matters:

1. **`stack`** — truthy only if non-empty. This guards `")("`, where a closer arrives with nothing open. It also prevents `stack[-1]` from raising `IndexError` on an empty list — Python's `and` short-circuits, so the second test never runs when the stack is empty.
2. **`stack[-1] == pairs[char]`** — the top must be this bracket's exact partner. `stack[-1]` is the top of the stack (last element).

Both true ⇒ matched pair ⇒ pop it off.
→ [truthy-falsy-values](../syntax/truthy-falsy-values.md) · [logical-operators](../syntax/logical-operators.md) · [list-methods](../syntax/list-methods.md)

```python
        else:
            return False
```

Either the stack was empty, or the top was the wrong type. Either way the string is invalid — return immediately, no need to look further.
→ [if-return](../syntax/if-return.md)

```python
    else:
        stack.append(char)
```

Not a closer ⇒ an opener. Push it and wait for its partner.

```python
return not stack
```

The elegant finish. An empty list is falsy, so `not stack` is `True` exactly when everything was matched. Leftovers like `"(("` mean unclosed brackets ⇒ `False`.

More idiomatic than `len(stack) == 0`, and it's the reason the second failure mode is handled in one line.
→ [truthy-falsy-values](../syntax/truthy-falsy-values.md) · [logical-operators](../syntax/logical-operators.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def isValid(self, s: str) -> bool:

        stack = []
        pairs = {")": "(", "]": "[", "}": "{"}

        for char in s:
            if char in pairs:
                if stack and stack[-1] == pairs[char]:
                    stack.pop()
                else:
                    return False
            else:
                stack.append(char)

        return not stack
```

</details>

**Trace it** — `s = "([{}])"`:

| char | Type | Stack before | Action | Stack after |
|---|---|---|---|---|
| `(` | open | `[]` | push | `[(]` |
| `[` | open | `[(]` | push | `[( []` |
| `{` | open | `[( []` | push | `[( [ {]` |
| `}` | close | `[( [ {]` | top is `{` ✅ pop | `[( []` |
| `]` | close | `[( []` | top is `[` ✅ pop | `[(]` |
| `)` | close | `[(]` | top is `(` ✅ pop | `[]` |

Empty stack ⇒ **`True`** ✅

**And the case that defeats counting** — `s = "([)]"`:

| char | Stack | Action |
|---|---|---|
| `(` | `[(]` | push |
| `[` | `[( []` | push |
| `)` | `[( []` | top is `[`, needs `(` ❌ → **`return False`** |

The stack catches the interleaving immediately, because it knows the *most recent* open bracket was `[`, not `(`.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

One pass over the string. Each character does O(1) work:

- A dict membership test → O(1).
- `stack[-1]` — indexing a list end → O(1).
- `.append()` / `.pop()` at the end of a list → O(1) amortized.

n × O(1) = **O(n)**.

**Every character is pushed at most once and popped at most once**, so total stack operations are bounded by 2n. The same "each element enters and leaves once" accounting that made the sliding-window problems linear.

**Early exit:** an invalid string returns at the first mismatch — `")((((..."` costs one step.

**Versus the delete-pairs approach:** repeatedly stripping `"()"` needs up to n/2 passes over an n-length string → O(n²). The stack resolves each pair the moment its closer arrives, so nothing is ever rescanned.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n).**

The stack holds unmatched opening brackets. Worst case — all openers, like `"((((("` — it holds every character.

- **Worst case O(n):** `"((((("` or the deeply nested `"((((()))))"`, which reaches depth n/2 before unwinding.
- **Best case O(1):** `"()()()()"` — each pair resolves immediately, so the stack never exceeds one element.

**The stack's maximum depth is the maximum nesting depth** of the string, which is a genuinely useful way to think about it: you're paying memory proportional to how deeply nested the input gets, not to its length as such.

**Can it be done in O(1)?** Not for three bracket types. With a *single* type you could just use a counter — increment on open, decrement on close, fail if it goes negative. That works precisely because with one type there's nothing to remember except *how many* are open. Three types means you must remember *which*, in order — and that requires the stack.

Worth saying out loud: **the counter is the O(1) solution to the one-type version, and the stack is what the three-type version costs.**

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Counting brackets isn't enough — `"([)]"` has balanced counts of every type but interleaves instead of nesting. The real rule is that the most recently opened bracket must be the next one closed, which is LIFO, so it's a stack. I push opening brackets; on a closing bracket I check it against the top of the stack and pop if it matches, otherwise it's invalid. Two failure modes: a closer arriving with an empty stack, and leftovers at the end — I handle the first in the loop and the second by returning whether the stack is empty. O(n) time, O(n) space for the worst-case nesting depth."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "What if there were only one bracket type?" | A counter, O(1) space — increment on open, decrement on close, fail if it ever goes negative or ends non-zero. The stack exists only because types must be remembered. |
| "What if other characters are allowed?" | Ignore anything that isn't a bracket — add an explicit `elif char in "([{"` rather than relying on the `else`. **Ask this before coding**; the current code would push a letter as if it were an opener. |
| "Return the index of the first invalid bracket." | Use `enumerate` and return `i` at the failure point. |
| "**Minimum** insertions/removals to make it valid?" | Count unmatched closers during the pass plus leftovers at the end. LeetCode 921 / 1249. |
| "What about a wildcard `*` that can be either?" | Much harder — a greedy range of possible open counts, or DP. See [Valid Parenthesis String](678-valid-parenthesis-string.md). |
| "**Longest** valid substring?" | A stack of *indices* rather than characters, tracking the last unmatched position. LeetCode 32, Hard. |
| "Can you skip work early?" | Odd length can never balance — return `False` immediately. |

**Traps:**

- **Counting instead of stacking.** The defining mistake; `"([)]"` is the test case that exposes it.
- **Forgetting the empty-stack check.** `")"` then raises `IndexError` on `stack[-1]`.
- **Forgetting the final emptiness check.** `"(("` returns `True` — you validated every closer but never confirmed everything closed.
- **Mapping openers to closers** instead of the reverse. It works, but then you need a separate test for "is this a closing bracket", losing the neat `char in pairs`.
- **Using `stack[0]`** instead of `stack[-1]`. That's the *bottom* — you'd be matching against the first bracket opened, i.e. FIFO, which is the wrong discipline entirely.

**This same move shows up in:** [Min Stack](155-min-stack.md) (augmenting a stack with extra per-element state) · [Evaluate Reverse Polish Notation](150-evaluate-reverse-polish-notation.md) (a stack of pending operands) · [Generate Parentheses](22-generate-parentheses.md) (the same validity rule, used to *build* strings rather than check them) · [Daily Temperatures](739-daily-temperatures.md) (a monotonic stack — same structure, "most recent unresolved item" logic).

</details>
