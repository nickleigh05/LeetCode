# What's Next After the Roadmap

*You've finished Phase 6 (or 7). Where the road forks from here, depending on what you're optimizing for.*

## Fork 1 — Interview prep (most people)

The gap between "knows the patterns" and "passes onsites" is reps under realistic conditions:

- **Mixed-topic randomness.** Real interviews don't announce "this is a graph problem." Drill random problems from the [NeetCode 150](../../lists/neetcode150.md)/[250](../../lists/neetcode250.md) with no topic label and a 35-minute timer — recognizing the pattern *is* the skill now.
- **Mock interviews weekly** — the performance layer needs its own reps. See [interview-guide](interview-guide.md).
- **System design** — half the loop for mid-level+ roles and completely absent from LeetCode. Standard starting points: *Designing Data-Intensive Applications* (the book), then practice designs (URL shortener, chat, news feed). Different muscle; budget real weeks for it.
- **Behavioral stories** — prepared, practiced aloud, same as code.

## Fork 2 — Competitive programming (the mastery rabbit hole)

If the [Phase 7 material](../learning/20-segment-trees.md) was *fun*, contests are the natural next arena: [Codeforces](https://codeforces.com) rounds, [AtCoder](https://atcoder.jp) ABCs, USACO divisions. Start with the I/O wrapper ([competitive-programming-io](competitive-programming-io.md)), do virtual contests before live ones, and **upsolve** — after each contest, solve the first problem you couldn't. That habit is the entire training algorithm.

The topics past this repo, roughly in order of appearance: [string matching](../algorithms/kmp.md) ([Z-algorithm](../algorithms/z-algorithm.md), hashing), [Tarjan's SCC / bridges](../algorithms/tarjan-scc.md), [binary lifting / LCA](../algorithms/binary-lifting-lca.md), [sparse tables](../data-structures/sparse-table.md), segment trees with lazy propagation, [matrix exponentiation](../algorithms/matrix-exponentiation.md), [convex hull](../algorithms/convex-hull.md), DP on trees/bitmasks/digits, and eventually suffix structures ([suffix arrays](../data-structures/suffix-array.md)) and flows. The [CP-Algorithms site](https://cp-algorithms.com) is the standard reference for all of it.

## Fork 3 — Becoming a better engineer (the honest one)

DSA is one leg of the stool. If interviews aren't imminent, the highest-return next moves are usually elsewhere:

- **Build something real** and ship it — a tool you actually use, deployed. Design, debugging-in-the-large, and finishing are skills LeetCode never touches.
- **Read real codebases** — pick a small open-source project you use, read it end to end, fix one issue.
- **Go one level deeper**: how Python actually runs (bytecode, the GIL), how an OS schedules, how a database indexes (B-trees — the [BST](../data-structures/binary-search-tree.md)'s industrial cousin). *Computer Systems: A Programmer's Perspective* and *Operating Systems: Three Easy Pieces* are the classic follow-ons.
- **A second language** — one static (Go, Rust, Java, C++) to make types and memory visible. Re-solving 20 favorite problems in it is a fast on-ramp.

## Whatever fork: maintenance mode

Skills decay. Two or three mixed-random problems a week — with the [redo-list discipline](study-plan.md) — keeps the whole roadmap warm for the day a recruiter emails. That's the difference between "I did LeetCode once" and "I can interview in two weeks."

**Related:** [interview-guide](interview-guide.md) · [study-plan](study-plan.md) · [competitive-programming-io](competitive-programming-io.md) · [Roadmap](../../roadmap.md)
