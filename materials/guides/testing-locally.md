# Testing Solutions Locally

*Running LeetCode-style code on your own machine — the missing glue between the browser editor and a real dev setup.*

Paste a LeetCode solution into a local file and it won't run: nothing calls the method, and names like `List` or `ListNode` don't exist. The fix is a tiny harness at the bottom of the file.

## The minimal harness

```python
from typing import List, Optional      # the names LeetCode pre-imports

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}
        for i, n in enumerate(nums):
            if target - n in seen:
                return [seen[target - n], i]
            seen[n] = i
        return []

if __name__ == "__main__":             # runs only when you execute this file directly
    s = Solution()
    assert s.twoSum([2, 7, 11, 15], 9) == [0, 1]
    assert s.twoSum([3, 3], 6) == [0, 1]
    assert s.twoSum([1, 2], 7) == []   # no-answer edge case
    print("all tests passed")
```

`python3 two_sum.py` → either `all tests passed` or an [AssertionError](../syntax/assert-statement.md) pointing at the failing case. Write the asserts *from the problem's examples* first, then add your own edge cases: empty input, one element, duplicates, negatives, already-sorted, all-equal.

## Linked-list and tree problems

LeetCode auto-defines these; locally you paste the standard definitions and a builder helper:

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val, self.next = val, next

def build_list(values):                # [1,2,3] -> 1->2->3
    head = cur = ListNode()
    for v in values:
        cur.next = cur = ListNode(v)
    return head.next

def to_pylist(head):                   # 1->2->3 -> [1,2,3], for asserting
    out = []
    while head:
        out.append(head.val); head = head.next
    return out
```

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right
```

Keep these in one `helpers.py` you [import](../syntax/import-basics.md) everywhere, and you'll never rewrite them.

## Leveling up: pytest

Once asserts feel cramped, `pip install pytest` (see [virtual-environments](virtual-environments.md)), name test functions `test_*`, and run `pytest`:

```python
def test_examples():
    assert Solution().twoSum([2, 7, 11, 15], 9) == [0, 1]
```

You get per-test pass/fail output and it shows the actual vs. expected values on failure — no `print` needed.

## Why bother, when the browser works?

Local files give you a real [debugger](debugging-python.md), your own editor, a permanent [git history](git-basics.md) of solutions, and zero temptation to peek at the solutions tab mid-attempt. The browser editor is for the final submit.

**Related:** [how-to-use-leetcode](how-to-use-leetcode.md) · [debugging-python](debugging-python.md) · [assert-statement (syntax)](../syntax/assert-statement.md) · [setup-editor](setup-editor.md)
