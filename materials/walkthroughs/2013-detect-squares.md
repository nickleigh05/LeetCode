# 2013. Detect Squares

**Medium** · [LeetCode](https://leetcode.com/problems/detect-squares/)

[📖 17. Math & Geometry lesson](../learning/19-math-geometry.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 17. Math & Geometry problems](../rmap-practice/17-math-geometry.md)

---

Solution: not yet solved in this repo.

Support adding points and counting axis-aligned squares formed with existing points. Why does fixing one diagonal corner and checking for the other diagonal corner (plus the two remaining corners) cover every possible square through a query point?

<details>
<summary>Hint</summary>

Keep a [hashmap](../data-structures/hashmap.md) of point counts. For a query `(x, y)`, look for every existing point `(x, y2)` sharing the same x-coordinate — that gives a candidate side length `y2 - y`. Then check whether the other two corners, `(x + side, y)` and `(x + side, y2)` (and the mirrored `x - side` case), exist too.
</details>

<details>
<summary>Solution</summary>

```python
from collections import defaultdict

class DetectSquares:

    def __init__(self):
        self.point_count = defaultdict(int)

    def add(self, point: List[int]) -> None:
        self.point_count[tuple(point)] += 1

    def count(self, point: List[int]) -> int:
        x, y = point
        total = 0

        for (px, py), cnt in list(self.point_count.items()):
            if px != x or py == y:
                continue

            side = py - y
            for x2 in (x + side, x - side):
                total += cnt * self.point_count[(x2, y)] * self.point_count[(x2, py)]

        return total
```

Building blocks: [defaultdict](../syntax/defaultdict.md) · [dict-methods](../syntax/dict-methods.md) (`.items()`) · [tuple-basics](../syntax/tuple-basics.md) · [for-loop](../syntax/for-loop.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** per `count` call, where n is the number of distinct points added.
**Space: O(n)** — the hashmap of point counts.
</details>
