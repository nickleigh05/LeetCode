# 71. Simplify Path

**Medium** · [LeetCode](https://leetcode.com/problems/simplify-path/) · [Solution file (no hints)](../../problems/0001-0499/71.py)

[📖 04. Stack lesson](../learning/04-stack.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 04. Stack problems](../rmap-practice/04-stack.md)

---

Given an absolute Unix-style path, return its **simplified canonical path**:

- `.` — the current directory (no effect)
- `..` — the parent directory (go up one level)
- Multiple consecutive slashes collapse to one
- Any other sequence of periods (`...`, `....`) is a **valid directory name**

The result must start with `/`, separate directories with a single `/`, and not end with `/` unless it's the root.

```
path = "/home/"                        →  "/home"
path = "/home//foo/"                   →  "/home/foo"
path = "/home/user/Documents/../Pictures"  →  "/home/user/Pictures"
path = "/../"                          →  "/"       (can't go above root)
path = "/.../a/../b/c/../d/./"         →  "/.../b/d"
```

**Constraints:** `1 <= path.length <= 3000` · letters, digits, `.`, `/`, `_` · `path` is a valid absolute Unix path

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "`..` goes to the **parent**" | ⚠️ Undo the most recent directory — that's a **pop**, and the reason this is a stack problem |
| "`.` is the current directory" | A no-op. Skip it entirely |
| "multiple slashes collapse" | Splitting on `/` produces **empty strings** you must discard |
| "`...` is a **valid name**" | ⚠️ The trap. Only *exactly* `.` and `..` are special; three or more dots is an ordinary directory |
| "`/../` → `/`" | Going above root is a **no-op**, not an error. Pop only if non-empty |
| "must not end with `/`" unless root | Joining needs care so the root case comes out as `"/"` not `""` |
| absolute path | Always starts with `/`, so the result always does too |

The structure is a stack of directory names, and every token maps to one operation:

| Token | Action |
|---|---|
| `""` (from `//` or leading/trailing `/`) | skip |
| `"."` | skip |
| `".."` | **pop** (if non-empty) |
| anything else — including `"..."` | **push** |

The whole problem is: split on `/`, apply those four rules, then join with `/` and prepend a `/`.

Two details do most of the damage in practice: **`...` is not special**, and **popping an empty stack must be silently ignored** rather than raising.

🤔 **Before you open the next section:** if you split `"/home//foo/"` on `"/"`, what exactly does the resulting list contain — including the pieces you might not expect?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Repeated regex/string replace | Substitute `//`, `/./`, `x/../` away, looping | O(n²) or worse | O(n) | ❌ Fragile, hard to make correct, easy to break on `...` |
| Manual character parsing | Walk the string building tokens by hand | O(n) | O(n) | ⚠️ Correct but verbose; `split` already does this |
| **`split('/')` + stack** | Tokenize, then apply four rules | **O(n)** | O(n) | ✅ |

**The decision: split on `/`, process tokens with a [stack](../data-structures/stack.md).**

Why a stack is the *right* structure and not just a convenient one: `..` must undo the **most recent** directory, and undoing the most recent thing is the definition of LIFO. No other structure gives you that in O(1).

**What `split('/')` actually produces** — worth being precise, because the empty strings are where bugs come from:

```python
"/home//foo/".split('/')   →  ['', 'home', '', 'foo', '']
 ↑                    ↑         ↑              ↑        ↑
leading slash    trailing   from leading   from '//'  from trailing
```

Every leading slash, trailing slash, and doubled slash yields an empty string. Filtering out `""` handles **all three** collapse rules at once — that's why `split` is the right tool rather than something to be avoided.

**Why `...` must not be special-cased.** A tempting shortcut is `if token.startswith('.')` or `if all(c == '.' for c in token)`. Both wrongly capture `"..."`, which the problem explicitly declares a legal directory name. The test must be **exact equality**: `token == '.'` and `token == '..'`. Nothing else.

**Why popping empty is a no-op.** `/../` means "go above root," which in Unix simply leaves you at root. So guard the pop: `if stack: stack.pop()`. An unguarded `stack.pop()` raises `IndexError` on `"/../"` — one of the given examples.

**Why the join is `'/' + '/'.join(stack)`.** Joining `['home','foo']` gives `"home/foo"`, so the leading `/` must be added back. And when the stack is empty, `'/'.join([])` is `""`, so `'/' + ""` correctly yields `"/"` — the root case falls out with no special handling. That's a small elegance worth noticing.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
parts = path.split("/")
stack = []
```

**Tokenize up front**, then keep a stack of the surviving directory names, in order from root outward.
→ [string-methods](../syntax/string-methods.md) · [list-basics](../syntax/list-basics.md) · [stack](../data-structures/stack.md)

```python
for part in parts:
```

Walk the tokens. Splitting on `/` yielded directory names plus empty strings wherever slashes were adjacent, leading, or trailing.
→ [for-loop](../syntax/for-loop.md)

```python
    if part == "" or part == ".":
        continue
```

**Skip the no-ops.** Empty strings come from collapsed/leading/trailing slashes; `.` means "stay here." Neither changes the path.

Handling both in one branch is why the slash-collapsing rules need no separate logic.
→ [break-continue](../syntax/break-continue.md)

```python
    elif part == "..":
        if len(stack) > 0:
            stack.pop()
```

**Go up one level — if there is one.**

`part == ".."` is **exact equality**, so `"..."` falls through to the `else` and is treated as a directory name, as required.

The `len(stack) > 0` guard makes `/../` a silent no-op instead of an `IndexError`. (`if stack:` is the more idiomatic spelling of the same test.)
→ [truthy-falsy-values](../syntax/truthy-falsy-values.md) · [list-methods](../syntax/list-methods.md)

```python
    else:
        stack.append(part)
```

**A real directory name** — including `...`, `....`, `_foo`, `a1`, and anything else.

```python
result = "/" + "/".join(stack)
return result
```

**Rebuild the canonical path.** Join with single slashes and prepend the root slash.

- `['home','foo']` → `"home/foo"` → `"/home/foo"` ✅
- `[]` → `""` → `"/"` ✅ (root, with no special case)

No trailing slash is ever produced, satisfying that rule automatically.
→ [string-join-slice](../syntax/string-join-slice.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def simplifyPath(self, path: str) -> str:

        parts = path.split("/")
        stack = []

        for part in parts:
            if part == "" or part == ".":
                continue
            elif part == "..":
                if len(stack) > 0:
                    stack.pop()
            else:
                stack.append(part)

        result = "/" + "/".join(stack)
        return result
```

</details>

**Trace it** — `path = "/.../a/../b/c/../d/./"`:

`path.split('/')` → `['', '...', 'a', '..', 'b', 'c', '..', 'd', '.', '']`

| Token | Rule | Stack after |
|---|---|---|
| `''` | skip (leading slash) | `[]` |
| `'...'` | ⚠️ **not** special → push | `['...']` |
| `'a'` | push | `['...', 'a']` |
| `'..'` | pop | `['...']` |
| `'b'` | push | `['...', 'b']` |
| `'c'` | push | `['...', 'b', 'c']` |
| `'..'` | pop | `['...', 'b']` |
| `'d'` | push | `['...', 'b', 'd']` |
| `'.'` | skip | `['...', 'b', 'd']` |
| `''` | skip (trailing slash) | `['...', 'b', 'd']` |

Return `'/' + '/'.join(['...', 'b', 'd'])` → `'/' + ".../b/d"` = **`"/.../b/d"`** ✅

The `'...'` token at step 2 is the discriminating case — any rule based on "starts with a dot" or "is all dots" would have mishandled it.

**And the root case** — `path = "/../"`:

| Token | Rule | Stack |
|---|---|---|
| `''` | skip | `[]` |
| `'..'` | pop, but stack is empty → **no-op** | `[]` |
| `''` | skip | `[]` |

Return `'/' + ''` = **`"/"`** ✅

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)**, where `n` is the length of `path`.

- `split('/')` — one O(n) pass, producing tokens whose total length is ≤ `n`
- The loop — one iteration per token; each does O(1) comparisons plus an O(1) amortized `append` or `pop`

  (Strictly, the string comparisons cost O(len(token)), but summed across all tokens that's O(n) total.)
- `'/'.join(stack)` — one O(n) pass

Total **O(n)**.

**Why the naive regex approach is worse:** repeatedly substituting `x/../` requires re-scanning the string after each replacement, giving O(n²) at best — and getting the pattern right around `...` and root-escaping is genuinely difficult. This is a case where the "clever" one-liner is both slower *and* more likely to be wrong.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n).**

- `split` produces a list of tokens totalling O(n) characters
- The stack holds at most all of them
- The joined result is O(n)

All three are linear, and the output alone is O(n), so this is the floor.

**Could you avoid `split`'s intermediate list?** Yes — parse the string character by character, accumulating tokens in place. It saves a constant factor but not an asymptotic one, and it's considerably more code. Not worth it unless the interviewer specifically asks about memory-constrained parsing.

Building the result with `'/'.join(...)` rather than repeated `+=` matters for the same reason as always: string concatenation in a loop is O(n²) in Python because strings are [immutable](../syntax/string-immutability.md). One `join` is O(n).

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "`..` means undo the most recent directory, which is a pop — so this is a stack problem. I split the path on `/`, which conveniently turns every leading, trailing, and doubled slash into an empty string, so filtering out empties handles all the slash-collapsing rules at once. Then four cases: empty or `.` I skip, `..` pops if the stack is non-empty — going above root is a no-op, not an error — and anything else is a directory name I push. The important subtlety is that only *exactly* `.` and `..` are special: `...` is a legal directory name, so I compare with exact equality rather than checking whether the token starts with or consists of dots. Finally I join with `/` and prepend the root slash, which also gives `\"/\"` correctly when the stack is empty. O(n) time and space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "What about `...`?" | **The trap.** It's a valid directory name. Only exact `.` and `..` are special — use equality, not `startswith`. |
| "What does `/../` return?" | `"/"`. You can't go above root, so the pop is silently skipped. |
| "Handle **relative** paths (not starting with `/`)?" | `..` at the start can no longer be discarded — you'd keep a count of leading `..` tokens and re-emit them, and the result wouldn't get a leading slash. |
| "Handle symlinks?" | Out of scope for pure string simplification — resolving symlinks requires filesystem access, since `a/../b` may not equal `b` if `a` is a link. |
| "Support `~` for home?" | Expand it to the home directory before this logic runs, then proceed unchanged. |
| "Why not regex?" | Repeated substitution is O(n²) and fragile around `...` and root-escaping. The stack is linear and states the rules directly. |
| "Windows-style paths?" | Different separator and drive letters (`C:\`); the same stack logic applies after adjusting tokenization. |

**Traps:**

- **Treating `...` as special.** *The* trap. `startswith('.')` or "all characters are dots" both break it. Use `==`.
- **Unguarded `stack.pop()`.** `IndexError` on `"/../"`, which is a given example.
- **Forgetting empty tokens.** `split` yields `''` for leading, trailing, and doubled slashes — skipping them is what implements the collapse rules.
- **Returning `''` for root.** `'/' + '/'.join([])` gives `"/"` — but only if you remember the leading `'/'`.
- **Leaving a trailing slash.** Joining rather than appending `'/'` after each part avoids it.
- **Building the result with `+=` in a loop.** O(n²) from string immutability.
- **Using `os.path.normpath`.** It gets `"/../"` right but isn't the exercise — and its behaviour differs across platforms.

**This same move shows up in:** [Valid Parentheses](20-valid-parentheses.md) (a stack undoing the most recent open item) · [Baseball Game](682-baseball-game.md) (a stack where one operation invalidates the previous entry) · [Decode String](394-decode-string.md) (a stack tracking nested context) · [Evaluate Reverse Polish Notation](150-evaluate-reverse-polish-notation.md) (token stream processed with a stack).

</details>

---
