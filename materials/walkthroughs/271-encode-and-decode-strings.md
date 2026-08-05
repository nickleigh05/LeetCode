# 271. Encode and Decode Strings

**Medium** · [LeetCode](https://leetcode.com/problems/encode-and-decode-strings/) · [Solution file (no hints)](../../problems/0001-0499/271.py)

[📖 01. Arrays & Hashing lesson](../learning/01-arrays-hashing.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 01. Arrays & Hashing problems](../rmap-practice/01-arrays-hashing.md)

---

Design an algorithm to **encode** a list of strings into a single string, which is then sent over the network and **decoded** back into the original list.

```
["neet","code","love","you"]  →  encode  →  "4#neet4#code4#love3#you"  →  decode  →  ["neet","code","love","you"]
```

Your encoder and decoder are the only two parties — you may design the format however you like, but the strings can contain **any** characters, including whatever you'd like to use as a separator.

**Constraints:** `0 <= strs.length < 200` · `0 <= strs[i].length < 200` · `strs[i]` contains any possible character

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

This one is a **design** problem, not a search problem — there's no clever data structure to spot. The whole difficulty is in a single line of the spec.

| The statement says | Which really means |
|---|---|
| "encode … then **decode** back" | Two functions that must be exact inverses. Design them **together** — every encoder choice is a decoder obligation |
| "strings can contain **any** character" | ⚠️ **This is the whole problem.** Any separator you pick — `,`, `#`, `\|`, even `\0` — could appear inside a string and fool the decoder |
| "you may design the format" | You control the protocol. You're not parsing someone else's format, you're inventing one that can't be ambiguous |
| strings may be **empty** | `["", ""]` must survive the round trip and stay distinguishable from `[]` and from `[""]` |
| lengths < 200 | Tiny. Efficiency is not the point here; **correctness under adversarial input** is |

Try the naive idea and watch it break: join with `","`. Then `["a,b"]` encodes to `"a,b"` and decodes to `["a", "b"]` — one string became two. Any pure-delimiter scheme has this hole.

So the question becomes: **how can the decoder know where a string ends without searching for a character that might be part of the data?**

🤔 **Before you open the next section:** if the decoder knew *in advance* exactly how many characters to read, it would never need to search for a boundary at all. How could you tell it that?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Format | Verdict |
|---|---|---|
| Plain delimiter | `"neet,code"` | ❌ Breaks the moment a string contains `,` |
| "Unlikely" delimiter | `"neet\|\|\|code"` | ❌ Same bug, just rarer. "Unlikely" is not "impossible" — and the spec says *any* character |
| Escaping | Double the delimiter inside data, `,` → `,,` | ⚠️ Genuinely works, but the decoder needs real escape-state logic. Easy to get subtly wrong |
| **Length prefix** | `"4#neet4#code"` | ✅ Unambiguous by construction |

**The decision: length-prefixed encoding — `<length>#<string>` for each string.**

The insight is that the delimiter is never *searched for inside the data*. The decoder reads digits until it hits the first `#`, converts them to a number `L`, and then **blindly consumes exactly `L` characters**. Whatever those characters are — `#`, newlines, digits, emoji — they're consumed as data because the length said so, not because they looked like data.

Walk `["4#hi"]` through it — the adversarial case that kills delimiter schemes:

```
encode:  "4#" + "4#hi"   →   "44#hi"
                                ↑ note: length 4, then the literal 4-char string "4#hi"

decode:  read digits until '#'  →  "4"  →  L = 4
         skip the '#'
         take the next 4 chars  →  "4#hi"   ✅ recovered exactly
```

The embedded `#` never confuses anything, because after reading the length the decoder stops *looking* and starts *counting*.

This is exactly how real protocols work — HTTP's `Content-Length`, netstrings, and most binary wire formats all prefix payloads with their size. Worth naming out loud; it shows the idea isn't a puzzle trick but standard practice.

**Why not escaping?** It's a legitimate alternative and fine to mention. But it needs the decoder to track escape state character by character, and off-by-one bugs there are nasty. Length prefixing is simpler to write, simpler to prove correct, and faster (no scanning for escapes).

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

**Encoding:**

```python
def encode(self, strs: list[str]) -> str:
    return "".join(f"{len(s)}#{s}" for s in strs)
```

Each string becomes `<len>#<string>`, and all the pieces are concatenated with nothing between them — no separator is needed *between* records, because each record's length tells the decoder exactly where it ends and the next begins.

`"".join(...)` over a generator builds the result in one pass; repeatedly doing `result += ...` would be O(n²) because Python strings are immutable and each `+=` copies.
→ [f-strings](../syntax/f-strings.md) · [generator-expressions](../syntax/generator-expressions.md) · [string-join-slice](../syntax/string-join-slice.md) · [string-immutability](../syntax/string-immutability.md)

**Decoding:**

```python
result = []
i = 0
while i < len(s):
```

`i` is the read cursor, always parked at the **start of the next length field**. A `while` rather than a `for` because the step size varies — each iteration jumps forward by a different amount.
→ [while-loop](../syntax/while-loop.md) · [list-basics](../syntax/list-basics.md)

```python
    j = s.index("#", i)
```

Find the **first** `#` at or after `i`. Everything between `i` and `j` is the length field. This is safe despite `#` appearing in the data: `i` always points at a length field, and lengths are digits only, so the first `#` found is guaranteed to be the delimiter of *this* record.
→ [string-methods](../syntax/string-methods.md)

```python
    length = int(s[i:j])
```

Slice out the digit characters and convert. `s[i:j]` excludes index `j` — exactly the digits, not the `#`.
→ [string-join-slice](../syntax/string-join-slice.md) · [type-conversion](../syntax/type-conversion.md) · [list-slicing](../syntax/list-slicing.md)

```python
    result.append(s[j + 1 : j + 1 + length])
```

The payload. `j + 1` skips the `#`, and the slice runs exactly `length` characters. **This is the line that makes the whole scheme work** — a blind count, no searching, so the content can't lie to us.
→ [list-methods](../syntax/list-methods.md)

```python
    i = j + 1 + length
```

Advance the cursor past this record to the start of the next length field. Getting this arithmetic wrong is the classic bug — it's `#` (1 char) plus the payload.

```python
return result
```

Cursor reached the end ⇒ every record consumed.

<details>
<summary>The whole thing together</summary>

```python
class Solution:

    def encode(self, strs: list[str]) -> str:
        return "".join(f"{len(s)}#{s}" for s in strs)

    def decode(self, s: str) -> list[str]:
        result = []
        i = 0
        while i < len(s):
            j = s.index("#", i)
            length = int(s[i:j])
            result.append(s[j + 1 : j + 1 + length])
            i = j + 1 + length
        return result
```

</details>

**Trace it** — decoding `"4#neet4#code"`:

| `i` | `j` (first `#`) | `s[i:j]` | `length` | payload `s[j+1 : j+1+len]` | next `i` |
|---|---|---|---|---|---|
| 0 | 1 | `"4"` | 4 | `"neet"` | 6 |
| 6 | 7 | `"4"` | 4 | `"code"` | 12 |
| 12 | — | | | loop ends (`12 == len(s)`) | |

**The edge cases fall out for free:**

- `[]` → encodes to `""` → the `while` never runs → `[]` ✅
- `[""]` → encodes to `"0#"` → length 0, empty slice → `[""]` ✅
- `["", ""]` → `"0#0#"` → `["", ""]` ✅

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)** for both directions, where n is the total number of characters across all strings.

**Encode:** builds one `<len>#<string>` piece per string, then joins. Every character is copied exactly once → O(n). (Plus O(d) for the length digits, where d is tiny — a 199-character string needs 3 digits.)

**Decode:** the cursor `i` only ever moves forward and never revisits a character. Each `s.index("#", i)` scans only the short digit field, and each slice copies its payload once. Summed over all records, that's every character touched a constant number of times → **O(n)**.

**Why the `while` loop is still linear** even though `.index()` is itself a scan: the searches never overlap. Record k's search covers only record k's length field. This is the same amortized argument as the inner loop in [Longest Consecutive Sequence](128-longest-consecutive-sequence.md) — a nested loop isn't automatically quadratic if the total work across all iterations is bounded.

**The trap that would make it O(n²):** building the encoded string with `result += piece` in a loop. Python strings are immutable, so each `+=` copies everything so far. Use `"".join`.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n).**

**Encode:** the output string is n characters plus the length prefixes → O(n). The prefixes add O(d) per string, so with m strings it's O(n + m·d) — and since d ≤ 4 for any realistic length, that's O(n).

**Decode:** the output list holds all the original characters again → O(n). The cursor variables `i`, `j`, `length` are O(1).

**Auxiliary space is O(1)** in both directions if you don't count the output — you're producing a transformed copy, not building a scratch structure. That's the honest framing: the space is *inherent to the task* (you must return the data), not overhead of the algorithm.

**The overhead of the protocol** is worth knowing: each string costs `len(digits) + 1` extra characters. For 200-string lists of short strings that's a few percent. Binary formats use a fixed-width length field (say 4 bytes) to make parsing even simpler at a slightly different cost.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The trap is that the strings can contain any character, so no delimiter is safe — whatever I pick could appear in the data. Instead of separating with a character the decoder has to *search* for, I'll prefix each string with its length: `4#neet`. The decoder reads digits up to the first `#`, then blindly consumes exactly that many characters — so the content can't be misinterpreted, because after reading the length it stops looking and starts counting. O(n) both ways. It's the same idea as HTTP's Content-Length."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "What if a string contains `#`?" | Handled — it's inside the counted payload, never searched for. Walk them through `["4#hi"]` → `"44#hi"`. This is the question they're really asking. |
| "Why not escape the delimiter?" | Valid alternative: double it inside data and un-double when decoding. Correct, but needs escape-state tracking in the decoder and is easier to get wrong. |
| "Could you use a fixed-width length?" | Yes — pad to 4 digits, `"0004neet"`. No delimiter at all, and the decoder always reads exactly 4 chars first. Costs more bytes for short strings, caps the maximum length. |
| "What about Unicode / multi-byte?" | In Python `len()` counts *characters*, so it round-trips. Over a real byte-oriented socket you'd prefix the **byte** length after encoding to UTF-8, or the count and the payload disagree. |
| "Empty list vs. list of one empty string?" | `""` vs `"0#"` — distinguishable, which is the point of a well-designed format. Demonstrate it. |
| "Make it robust to corrupted input." | Validate: the digits must parse, `j+1+length` must not exceed `len(s)`. Raise rather than silently returning garbage. |

**Traps:**

- **Any delimiter-only scheme.** The interviewer *will* test `["a,b"]` or `["#"]`.
- **Cursor arithmetic.** `i = j + 1 + length` — forgetting the `+1` for the `#` leaves the cursor on the delimiter and everything after it is garbage.
- **`s.index("#")` without the start argument** — always finds the *first* `#` in the whole string, so the loop never advances.
- **`+=` string building** in encode — quietly O(n²).
- **Assuming non-empty strings.** `"0#"` must work; test it.
- **Designing encode without decode.** They're one design. Any format you can't parse deterministically is not a format.

**This same move shows up in:** [Serialize and Deserialize Binary Tree](297-serialize-and-deserialize-binary-tree.md) (the same encode/decode design problem, on a tree — and the same "make the format unambiguous" lesson) · [Design Twitter](355-design-twitter.md) and [LRU Cache](146-lru-cache.md) (other design problems where the API contract, not an algorithm, is the work).

</details>

---
