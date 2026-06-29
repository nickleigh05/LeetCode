# 00. Foundations

*Start here even if you've never heard the words "data structure." By the end you'll know what they are, why Big O matters, and how to use this repo.*

[← Roadmap](../roadmap.md) · [🗺 Roadmap](../roadmap.md) · [Next →](00b-foundations-practice.md)

---

If you're brand new, nothing here assumes prior computer-science classes — only that you can read a little Python. We'll build the vocabulary you need before the first real lesson. Take your time; this is the one page everything else stands on.

## What even *is* a data structure?

A **data structure** is just a way of organizing data in memory so you can use it efficiently. That's it. A shopping list, a stack of plates, a family tree — each organizes information differently, and each makes some actions easy and others awkward.

- A **list** is good for "give me item #3" but bad for "is *banana* anywhere in here?"
- A **stack of plates** is great for "take the top one" but you can't grab the bottom without moving everything.
- A **family tree** makes "who are this person's children?" instant.

The whole game is matching the structure to what your problem asks for most often.

## What is an algorithm?

An **algorithm** is a step-by-step recipe for solving a problem — finding a name in a phone book, sorting cards in your hand, finding the shortest route on a map. The same problem can have many algorithms, and they are *not* equally fast. Learning algorithms is learning the handful of recipes that show up again and again, so you recognize them instead of reinventing a slow one each time.

## Big O — measuring "how does this scale?"

You can't judge code by how fast it runs on *your* laptop with *10* items. The real question is: **as the input grows, how does the work grow?** **Big O notation** answers that, ignoring constants and small details to capture the shape of the growth.

| Big O | Name | "If input doubles, work…" | Example |
|-------|------|---------------------------|---------|
| O(1) | constant | stays the same | look up `arr[5]`, hash-map get |
| O(log n) | logarithmic | grows by one step | binary search |
| O(n) | linear | doubles | scan a list once |
| O(n log n) | linearithmic | a bit more than doubles | good sorting |
| O(n²) | quadratic | quadruples | compare every pair (nested loop) |
| O(2ⁿ) | exponential | *squares* — explodes | try every subset (naive) |

A quick picture of how fast these pull apart as `n` grows:

```
work
 │                                        O(2ⁿ)   O(n²)
 │                                      ·        /
 │                                   ·         /
 │                                ·          /
 │                             ·           /
 │                          ·            /            O(n log n)
 │                       ·             /          ___/
 │                    ·              /        ___/          O(n)
 │                 ·               /     ___/      _________/
 │              ·                /  ___/  ________/
 │         ·    ·    ·    ·    /__/______/________________  O(log n)
 │   · · ·  ____________________________________________   O(1)
 └────────────────────────────────────────────────────────► n  (input size)
```

The lesson: an O(n²) solution that's fine for 100 items can be hopeless at 100,000. Interviewers care about Big O because it predicts what happens at scale. Most of this course is really about turning O(n²) brute force into O(n) or O(log n) by picking the right structure and pattern.

**Time vs. space.** Big O describes *time* (steps) and *space* (extra memory) separately. A classic trade is spending O(n) memory (a hash map) to cut time from O(n²) to O(n). That trade-off is the heartbeat of [Lesson 01](01-arrays-hashing.md).

## A peek at memory: contiguous vs. linked

Two ways to store a sequence, and the difference explains half of all data-structure choices:

```
ARRAY  — one contiguous block. Jump to any index instantly (math on the address).
┌────┬────┬────┬────┬────┐
│ 10 │ 20 │ 30 │ 40 │ 50 │     arr[3] → O(1)
└────┴────┴────┴────┴────┘     inserting in the middle → shift everyone → O(n)

LINKED LIST — scattered nodes, each pointing to the next. No instant indexing,
but splicing is cheap once you're holding the spot.
┌────┐    ┌────┐    ┌────┐    ┌────┐
│ 10 │──► │ 20 │──► │ 30 │──► │ 40 │──► None
└────┘    └────┘    └────┘    └────┘
find the 3rd → walk 3 hops → O(n);  insert after a node you hold → O(1)
```

You don't need more than this intuition right now — [Lesson 06](06-linked-list.md) goes deep. Just remember: **arrays win at random access, linked structures win at splicing.**

## How to use this repo

This is a self-paced course. The loop for every topic is the same:

1. **Read the lesson** (`roadmap/learning/NN-topic.md`) — the concept, the pattern, the diagrams.
2. **Study the template** in [`appendix/templates/`](../appendix/templates/) — the reusable code shape. Type it out from memory.
3. **Drill problems** from the matching section of [`lists/recommended.md`](../../lists/recommended.md), easy → hard.
4. **Check yourself** with the 3 boxes at the bottom of each lesson before moving on.

Three rules that make it stick:

- **Don't jump around.** DSA is cumulative — each lesson leans on the last. Follow the [roadmap](../roadmap.md) order.
- **The 30-minute rule.** Stuck for 30 minutes? Read the template's "common bugs" and hints rather than suffering for hours. Struggle is good; spinning is not.
- **Spaced review.** Revisit a topic 3 days after it first clicks. Re-deriving it is what moves it to long-term memory.

When you're ready, take a breath and do the [**Foundations Practice drills →**](00b-foundations-practice.md) to make Big O stick before the first real lesson.

---

[← Roadmap](../roadmap.md) · [🗺 Roadmap](../roadmap.md) · [Next →](00b-foundations-practice.md)
