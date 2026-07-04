# How to Use LeetCode (the Site)

*The mechanics of the judge — what the boilerplate means, what the verdicts mean, and the site features worth knowing.*

## The boilerplate

Every problem hands you a class with one method to fill in:

```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # your code here
```

- You only write the body. LeetCode calls the method with each hidden test case and compares your return value to the expected answer. You almost never `print` the answer — you **return** it.
- `self` is there because it's a [class method](../syntax/class-basics.md); ignore it beyond that.
- The `List[int]` annotations are [type hints](../syntax/type-hints.md) — documentation, not enforcement.
- `List`, `Optional`, `TreeNode`, `ListNode` are pre-imported by the judge; run the same code locally and you must define them yourself — see [testing-locally](testing-locally.md).

## The verdicts

| Verdict | Meaning | First thing to check |
|---------|---------|----------------------|
| **Accepted (AC)** | Passed every hidden test. | Celebrate, then re-read your code once — could it be cleaner? |
| **Wrong Answer (WA)** | Ran fine, returned the wrong thing. | The shown failing input. Trace your code on it *by hand*. Usually an edge case: empty input, single element, duplicates, negatives. |
| **Time Limit Exceeded (TLE)** | Too slow for the input sizes. | The constraints — your Big-O is one class too high. O(n²) with n = 10⁵ is the classic. See [constraints-cheatsheet](constraints-cheatsheet.md). |
| **Runtime Error (RE)** | Crashed — index out of range, None access, etc. | The traceback it shows. See [common-python-errors](common-python-errors.md). |
| **Memory Limit Exceeded (MLE)** | Allocated too much. | Are you building a huge extra structure where O(1) space was intended? |
| **Output Limit Exceeded** | You printed massively (usually a debug print inside a loop). | Delete stray `print`s. |

**Run vs. Submit:** *Run* executes only the visible examples (plus any you add) — fast feedback, proves nothing. *Submit* runs the full hidden suite and is what counts.

## Features worth actually using

- **Custom testcase** — the input box under the editor. The moment you suspect an edge case (empty list, one element, all duplicates), type it in and Run. This is 10× faster than submit-and-pray.
- **Constraints block** — read it *before* designing. `n ≤ 10⁵` and `n ≤ 20` are different problems. See [how-to-approach-a-problem](how-to-approach-a-problem.md).
- **Editorial / Solutions tab** — after a real attempt (see [the 30-minute rule](study-plan.md)), reading solutions is studying, not cheating. Reading them *instead of* attempting is the trap that feels like progress.
- **Runtime percentile** — mostly noise. Judge times vary run to run; chasing 99% often means unreadable micro-optimizations. Right complexity class ≫ fast constant.
- **Daily challenge & streaks** — nice for habit, but random topics; the [roadmap](../../roadmap.md) order teaches better. Don't let streak anxiety replace deliberate practice.
- **Premium** — not needed. Every pattern is learnable from free problems (this repo's lists prove it). Company-tagged questions are the one genuinely useful paid feature, and only right before a specific interview.

## Small print that bites people

- Your method may be called **multiple times per run** — if you use a global/class-level cache, stale state can leak between test cases. Keep state inside the method.
- Python solutions get generous time multipliers vs. C++, but a wrong complexity class still TLEs — the multiplier forgives constants, not O(n²).
- LeetCode's Python is a recent 3.x: [f-strings](../syntax/f-strings.md), [walrus](../syntax/walrus-operator.md), [match](../syntax/match-statement.md) all work.

**Related:** [how-to-approach-a-problem](how-to-approach-a-problem.md) · [testing-locally](testing-locally.md) · [constraints-cheatsheet](constraints-cheatsheet.md) · [study-plan](study-plan.md)
