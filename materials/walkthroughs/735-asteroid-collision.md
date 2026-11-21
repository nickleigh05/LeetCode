# 735. Asteroid Collision

**Medium** · [LeetCode](https://leetcode.com/problems/asteroid-collision/) · [Solution file (no hints)](../../problems/0500-0999/735.py)

[📖 04. Stack lesson](../learning/04-stack.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 04. Stack problems](../rmap-practice/04-stack.md)

---

You're given an array `asteroids` of integers representing asteroids in a row. For each one, the **absolute value** is its size and the **sign** is its direction: positive moves right, negative moves left. All asteroids move at the same speed.

When two asteroids meet, the **smaller one explodes**. If they're the **same size, both explode**. Two asteroids moving in the same direction never meet. Return the state after all collisions.

```
asteroids = [5,10,-5]     →  [5,10]     (10 and -5 collide; -5 explodes)
asteroids = [8,-8]        →  []         (same size; both explode)
asteroids = [10,2,-5]     →  [10]       (2 and -5 → -5 survives; then 10 and -5 → 10 survives)
asteroids = [-2,-1,1,2]   →  [-2,-1,1,2] (lefts move left, rights move right: they never meet)
```

**Constraints:** `2 <= asteroids.length <= 10⁴` · `-1000 <= asteroids[i] <= 1000` · `asteroids[i] != 0`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| sign = direction | `+` moves right, `−` moves left |
| asteroids **meet** | Only one pattern collides: a **right-mover on the left** and a **left-mover on the right**, `(+, −)` |
| smaller explodes, equal both explode | Compare absolute sizes. There are three outcomes |
| state after **all** collisions | A survivor can go on to hit the next one. `[10, 2, -5]` needs two collisions |

**Which pairs collide, and which don't?**

| Left | Right | Collide? |
|---|---|---|
| → (+) | → (+) | no, same direction |
| ← (−) | ← (−) | no, same direction |
| ← (−) | → (+) | no, moving **apart** |
| → (+) | ← (−) | **yes**, moving towards each other |

So collisions happen only when a **negative** asteroid arrives and the most recent survivor before it is **positive**.

**Why a stack.** Process left to right. Everything that has survived so far sits on a stack. When a new left-mover arrives, it hits the **most recent** right-mover, the top of the stack. If it wins, that right-mover is gone and the new asteroid carries on into the *next* one down. It's the same "the newcomer knocks things off the top" pattern as a [monotonic stack](../data-structures/monotonic-stack.md).

🤔 **Before you open the next section:** a new `-5` arrives and the stack is `[10, 2]`. What happens step by step, and when does it stop?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Simulate repeatedly | Scan for an adjacent `(+, −)` pair, resolve it, rescan | O(n²) | O(n) | ❌ Rescanning is slow |
| **Stack of survivors** | Each new left-mover fights the stack top until it dies or nothing is left to fight | **O(n)** | O(n) | ✅ |

**The decision: a [stack](../data-structures/stack.md)** holding the survivors so far.

When a left-mover arrives, it can only ever hit right-movers that are **on top** of the stack. Anything below a left-mover on the stack is moving away from it. So the fight is always with the top, and every loss is a pop.

**The three outcomes when `a < 0` meets a positive top:**

| Comparison | What happens | Keep fighting? |
|---|---|---|
| `top < |a|` | the top explodes, so pop it | **yes**, `a` meets the next one |
| `top == |a|` | both explode, so pop, and `a` dies | no |
| `top > |a|` | `a` explodes | no |

An `alive` flag tracks whether the newcomer survives, and so whether it should be pushed at the end.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
stack = []
for a in asteroids:
    alive = True
```

The stack holds the current survivors, left to right. Each new asteroid starts out alive.
→ [list-basics](../syntax/list-basics.md) · [for-loop](../syntax/for-loop.md) · [boolean-basics](../syntax/boolean-basics.md)

```python
    while alive and a < 0 and stack and stack[-1] > 0:
```

**The collision condition, all four parts:**
- `alive`: the newcomer hasn't exploded yet.
- `a < 0`: it's moving left. Right-movers never hit anything already on the stack.
- `stack`: there's something to hit. An empty list is falsy.
- `stack[-1] > 0`: the top is moving right, towards it.

The order matters. `stack` is checked before `stack[-1]`, so you never index an empty list.
→ [while-loop](../syntax/while-loop.md) · [logical-operators](../syntax/logical-operators.md) · [truthy-falsy-values](../syntax/truthy-falsy-values.md)

```python
        if stack[-1] < -a:
            stack.pop()
```

**The top is smaller, so it explodes.** `-a` is the newcomer's size, since `a` is negative. The loop goes round again: the newcomer meets the next asteroid down.
→ [list-methods](../syntax/list-methods.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
        elif stack[-1] == -a:
            stack.pop()
            alive = False
```

**Same size, so both explode.** Pop the top and mark the newcomer as dead, which ends the loop.

```python
        else:
            alive = False
```

**The top is bigger.** The newcomer explodes and the stack is unchanged.
→ [elif-else](../syntax/elif-else.md)

```python
    if alive:
        stack.append(a)
return stack
```

If the newcomer survived (it never fought, or it won every fight), it joins the survivors. Whatever is left on the stack at the end is the answer, in order.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def asteroidCollision(self, asteroids: List[int]) -> List[int]:
        stack = []
        for a in asteroids:
            alive = True
            while alive and a < 0 and stack and stack[-1] > 0:
                if stack[-1] < -a:
                    stack.pop()
                elif stack[-1] == -a:
                    stack.pop()
                    alive = False
                else:
                    alive = False
            if alive:
                stack.append(a)
        return stack
```

</details>

**Trace it.** `asteroids = [10, 2, -5]`:

| `a` | Stack before | Fight | Stack after |
|---|---|---|---|
| 10 | `[]` | none (moving right) | `[10]` |
| 2 | `[10]` | none (moving right) | `[10, 2]` |
| −5 | `[10, 2]` | 2 < 5 → pop 2; then 10 > 5 → −5 dies | `[10]` |

Answer `[10]` ✅.

**Moving apart.** `[-2, -1, 1, 2]`: the left-movers arrive with an empty stack or a negative top, so there's no fight. The right-movers never fight. The answer is the whole array ✅.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).** The `while` loop looks nested, but each asteroid is **pushed at most once and popped at most once**. Every iteration of the inner loop either pops something or ends the loop, so the total number of inner-loop iterations across the whole run is at most n pops plus n endings.

This "amortised O(n)" argument is the standard one for stack problems where each element enters and leaves once.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n).** The stack holds every survivor, which is all n asteroids if none collide (for example, all moving the same way). The answer is the stack itself, so this space is also the output.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Only a right-mover followed by a left-mover can collide. I process left to right with a stack of survivors. A right-mover just gets pushed. A left-mover fights the stack top while the top is a right-mover: if the top is smaller it pops and the fight continues, if they're equal both go, and if the top is bigger the newcomer dies. If the newcomer survives, I push it. Each asteroid is pushed and popped at most once, so it's O(n) time and O(n) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why don't `(−, +)` pairs collide?" | The left one moves left and the right one moves right. They're moving apart. |
| "Why is the nested loop O(n)?" | Each inner-loop iteration pops an asteroid or ends the loop. There are at most n pops in total. |
| "Different speeds?" | Then the order of collisions depends on timing. You'd need event simulation sorted by collision time, a much harder problem. |
| "Count the explosions?" | Increment a counter on each pop, and when the newcomer dies. |

**Traps:**

- **Letting right-movers fight.** A new positive asteroid can't hit anything already on the stack.
- **Fighting only once.** `[10, 2, -5]` needs the `-5` to win against `2` and *then* lose to `10`. Use a `while`, not an `if`.
- **Forgetting the equal case.** Both explode, so pop **and** don't push.
- **Indexing `stack[-1]` on an empty stack.** Check `stack` first.
- **Comparing `stack[-1] < a`.** `a` is negative. Compare with `-a` (or `abs(a)`).

**This same move shows up in:** [Daily Temperatures](739-daily-temperatures.md) (a newcomer pops smaller items off the stack) · [Backspace String Compare](844-backspace-string-compare.md) (a new character can cancel the top) · [Baseball Game](682-baseball-game.md) (operations act on the most recent items) · [Car Fleet](853-car-fleet.md) (things moving in one direction merging when they catch up).

</details>

---
