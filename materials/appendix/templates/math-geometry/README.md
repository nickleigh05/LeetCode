# Math & Geometry

*Modular arithmetic, GCD, fast power, matrix ops. Usually a short routine once you remember the trick — the trick is the whole problem.*

## Recognize this pattern when...

- The problem is about **digits, divisibility, GCD/LCM, or primes**.
- You need **exponentiation** of a huge power (often `mod 1e9+7`).
- It's an **in-place matrix transform**: rotate, transpose, spiral, set-zeroes.
- **Overflow** is called out explicitly (a real concern in fixed-width languages).
- **Points, lines, slopes, or squares** on a coordinate plane.

## Variations

1. **Digit iteration** — peel digits with `% 10` and `// 10`. *(Palindrome Number, Reverse Integer, Happy Number)*
2. **GCD / LCM (Euclid)** — `lcm(a, b) = a // gcd(a, b) * b`. *(Greatest Common Divisor of Strings)*
3. **Fast exponentiation** — square-and-halve; handle negative and zero exponents. *(Pow(x, n))*
4. **In-place matrix transform** — transpose + reverse, or layer-by-layer boundary walk. *(Rotate Image, Spiral Matrix)*
5. **Slope / point hashing** — reduce `(dy, dx)` by their GCD to dedupe collinear points exactly. *(Max Points on a Line)*

## Representative problems

| # | Difficulty | Problem |
|---|------------|---------|
| 9 | Easy | Palindrome Number |
| 202 | Easy | Happy Number |
| 50 | Medium | [Pow(x, n)](../../../../problems/0001-0499/50.py) |
| 48 | Medium | Rotate Image |
| 54 | Medium | Spiral Matrix |
| 149 | Hard | Max Points on a Line |

## Common bugs & traps

- **Overflow (in C/Java/Go).** Python ints are unbounded, but interview answers should still clamp to the 32-bit range when the problem demands it.
- **Negative modulo.** Python's `%` returns a result with the divisor's sign — different from C. Normalize when porting logic.
- **Fast power edge cases.** Exponent `0` returns `1`; negative exponent flips to `1 / base`. Don't loop on the raw negative.
- **Transpose swapping twice.** Start the inner loop at `j = i + 1`; iterating the full grid swaps each pair back to where it started.
- **Spiral boundary off-by-one.** Shrink top/bottom/left/right after each edge and re-check bounds before the vertical passes, or you revisit a row.
- **Float slopes lose precision.** Compare slopes as reduced integer fractions `(dy // g, dx // g)`, not floating-point division.
---

*See also: [Lesson 19 →](../../../learning/19-math-geometry.md) · [🗺 Roadmap](../../../../roadmap.md) · [problem lists](../../../../lists/)*
