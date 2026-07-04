# 00b. Algorithms

*A step-by-step recipe for solving a problem — and why some recipes are thousands of times faster than others.*

[← Prev](00a-data-structures.md) · [🗺 Roadmap](../../roadmap.md) · [Next →](00c-big-o-notation.md)

---

## What is an algorithm?

An **algorithm** is a step-by-step recipe for solving a problem — finding a name in a phone book, sorting cards in your hand, finding the shortest route on a map. If a computer (or a very patient person) can follow the steps and always arrive at the answer, it's an algorithm.

## Same problem, very different recipes

The same problem can have many algorithms, and they are *not* equally fast. Find "Nguyen" in a 1,000-page phone book:

- **Recipe 1 — scan every page** from page 1 until you hit it. Works, but could take 1,000 page-turns.
- **Recipe 2 — open the middle**, see which half "Nguyen" falls in, throw the other half away, repeat. Ten page-turns, guaranteed.

Both are correct. One is a hundred times faster — and the gap *grows* with the size of the book. That second recipe is [binary search](05-binary-search.md), and you'll write it yourself in Phase 2.

## Why this course exists

Learning algorithms is learning the handful of recipes that show up again and again — search, sort, traverse, accumulate — so you *recognize* them in a new problem instead of reinventing a slow one under interview pressure. Data structures ([previous lesson](00a-data-structures.md)) and algorithms are two halves of one skill: the structure holds the data, the algorithm walks it.

For a catalog of the named recipes (one page each), see the [Algorithms reference hub](../algorithms/_index.md).

## Check Yourself

- [ ] I can say what an algorithm is in one sentence.
- [ ] I can explain, with the phone book example, how two correct algorithms can differ wildly in speed.
- [ ] I get why "recognize the recipe" beats "invent from scratch" in an interview.

---

**Up next:** [Big O Notation](00c-big-o-notation.md) — the language for comparing those recipes precisely.

[← Prev](00a-data-structures.md) · [🗺 Roadmap](../../roadmap.md) · [Next →](00c-big-o-notation.md)
