# Convex Hull (Monotone Chain)

```python
def cross(o, a, b):                    # z of (a-o) × (b-o): >0 = left turn
    return (a[0]-o[0]) * (b[1]-o[1]) - (a[1]-o[1]) * (b[0]-o[0])

def convex_hull(points):
    pts = sorted(set(map(tuple, points)))
    if len(pts) <= 2:
        return pts
    def half(points_iter):             # build one side, monotonic-stack style
        chain = []
        for p in points_iter:
            while len(chain) >= 2 and cross(chain[-2], chain[-1], p) <= 0:
                chain.pop()            # last point makes a right turn → not on hull
            chain.append(p)
        return chain[:-1]
    return half(pts) + half(reversed(pts))   # lower chain + upper chain
```

The smallest convex polygon containing all points — the rubber band snapped around the nails. Monotone chain builds it like a [monotonic stack](../data-structures/monotonic-stack.md): sweep the sorted points, popping any point that would create a clockwise turn, once left-to-right for the bottom edge and once back for the top. The only real geometry needed is the **cross product sign** = turn direction, which is also the answer to half of all other geometry questions (segment orientation, point-in-triangle). LeetCode's lone direct hit is Erect the Fence (LC 587); beyond that it's collision detection, GIS boundaries, and the opening move of many computational-geometry problems.

**Complexity:** O(n log n) — the sort dominates; the two sweeps are O(n).

**Related:** [monotonic-stack (data-structures)](../data-structures/monotonic-stack.md) · [Math & Geometry lesson](../learning/19-math-geometry.md) · [sorting-key (syntax)](../syntax/sorting-key.md)
