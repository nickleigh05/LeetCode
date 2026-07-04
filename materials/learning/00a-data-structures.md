# 00a. Data Structures

*What a data structure actually is — and the one memory picture that explains half of all structure choices.*

[← Roadmap](../../roadmap.md) · [🗺 Roadmap](../../roadmap.md) · [Next →](00b-algorithms.md)

---

## What even *is* a data structure?

A **data structure** is just a way of organizing data in memory so you can use it efficiently. That's it. A shopping list, a stack of plates, a family tree — each organizes information differently, and each makes some actions easy and others awkward.

- A **list** is good for "give me item #3" but bad for "is *banana* anywhere in here?"
- A **stack of plates** is great for "take the top one" but you can't grab the bottom without moving everything.
- A **family tree** makes "who are this person's children?" instant.

The whole game is matching the structure to what your problem asks for most often.

## How to pick one

Ask: **what operation does my problem do over and over?** Then reach for the structure that makes *that* operation cheap.

| You keep needing… | Reach for… |
|-------------------|-----------|
| "give me item #i" | array / list |
| "have I seen this before?" | hash set / hash map |
| "the most recent thing" | stack |
| "the oldest thing" | queue |
| "the smallest/largest so far" | heap |
| "everything related to X" | tree / graph |

You'll meet each of these properly in its own lesson — this table is just the mindset.

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

For a full catalog of structures (one page each), see the [Data Structures reference hub](../data-structures/_index.md).

## Check Yourself

- [ ] I can say what a data structure is in one sentence, without jargon.
- [ ] Given an operation ("have I seen this?", "give me the most recent"), I can name a structure that makes it cheap.
- [ ] I can explain why arrays index in O(1) but insert in O(n), and why linked lists are the reverse.

---

**Up next:** [Algorithms](00b-algorithms.md) — the step-by-step recipes that *use* these structures.

[← Roadmap](../../roadmap.md) · [🗺 Roadmap](../../roadmap.md) · [Next →](00b-algorithms.md)
