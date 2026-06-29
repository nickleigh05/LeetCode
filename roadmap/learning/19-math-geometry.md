# 19. Math & Geometry
*GCD, fast power, and in-place matrix transforms.*

[← Prev](18-bit-manipulation.md) · [🗺 Roadmap](../roadmap.md)

---

> **Read first if rusty:** [Grids Primer](10b-grids-primer.md) — the matrix half of this lesson (rotate, spiral, set-zeroes) builds directly on the 2-D indexing and transform idioms there.

The grab-bag finale: number theory (GCD, primes, fast exponentiation) and grid/matrix manipulation (rotate in place, spiral order, set-zeroes). Less about a single pattern, more about a toolbox of tricks — lean on the template and the [core cheatsheet](../appendix/cheatsheet-core.md) and learn them as they come up.

## Concept

This last stop is a small toolbox rather than one big pattern. Three tricks cover most of it.

### GCD — Euclid's algorithm

The greatest common divisor of two numbers: repeatedly replace the larger with the remainder.

```python
def gcd(a, b):
    while b:
        a, b = b, a % b     # O(log(min(a, b)))
    return a
```

The same idea underlies fraction reduction and many number-theory problems. Least common multiple
falls right out: `lcm(a, b) = a * b // gcd(a, b)`.

### Fast exponentiation — square as you go

Computing `x**n` by multiplying `n` times is O(n); squaring halves the exponent each step for
O(log n):

```python
def power(x, n):
    result = 1
    while n:
        if n & 1:        # bit set → fold in this power of x
            result *= x
        x *= x           # x, x², x⁴, x⁸, ...
        n >>= 1
    return result
```

### In-place matrix transforms

Grid problems often ask you to mutate the matrix with **O(1) extra space**. Rotating 90°
clockwise = **transpose, then reverse each row**:

```
1 2 3      transpose      1 4 7      reverse rows     7 4 1
4 5 6   ───────────────►  2 5 8   ───────────────►    8 5 2
7 8 9                     3 6 9                        9 6 3
```

Spiral traversal and "set matrix zeroes" are the same flavor: walk the indices carefully and
mutate in place. Reach for the template and the
[core cheatsheet](../appendix/cheatsheet-core.md) when one comes up.

## The Template

The reusable code skeleton for this pattern lives in [`appendix/templates/math-geometry/`](../appendix/templates/math-geometry/). Read the README (when to reach for it, variations, common bugs), then type out [`template.py`](../appendix/templates/math-geometry/template.py) from memory before you drill problems.

## Practice

Work the matching set in the curated list: [**Math & Geometry problems →**](../../lists/recommended.md#17-math--geometry-16-problems). Easy → hard, top to bottom. When the pattern feels automatic, move on — don't grind it forever.

## Check Yourself

- [ ] I can write GCD (Euclid) and fast modular exponentiation from memory.
- [ ] I can do the in-place matrix transforms (rotate 90°, spiral, set-zeroes) without scratch space.
- [ ] I know the common overflow / modulo pitfalls (less in Python, but I can articulate them).
- [ ] I solved a 🔴 Hard math/geometry problem (e.g. Max Points on a Line or Basic Calculator).

---

*That's the core roadmap. For mastery-level range-query problems, continue with [Segment & Fenwick Trees →](20-segment-trees.md).*

[← Prev](18-bit-manipulation.md) · [🗺 Roadmap](../roadmap.md) · [Next (mastery) →](20-segment-trees.md)

