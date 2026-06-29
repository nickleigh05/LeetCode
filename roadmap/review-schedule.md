# Spaced Repetition & Phase Milestones

*Knowing a topic once isn't mastery. This schedule tells you when to come back.*

---

## The core rule

After you first finish a lesson and pass the "Check Yourself" boxes: **review it on day +3, +10, and +30**. A review is brief — 10–15 minutes. Rederive the key template from memory, solve one medium problem cold, check the complexity. If it comes back easily, you own it. If it doesn't, work the practice set again before moving on.

> The "30-minute rule" still applies: if you're stuck on any review problem for 30 minutes, open the lesson and read — then close it and try again.

---

## Spaced Review Table

| # | Lesson | First pass | Day +3 | Day +10 | Day +30 |
|---|--------|-----------|--------|---------|---------|
| 00 | Foundations | | [ ] | [ ] | [ ] |
| 00b | Big-O Practice | | [ ] | [ ] | [ ] |
| 01 | Arrays & Hashing | | [ ] | [ ] | [ ] |
| 02 | Two Pointers | | [ ] | [ ] | [ ] |
| 03 | Sliding Window | | [ ] | [ ] | [ ] |
| 04 | Stacks & Queues | | [ ] | [ ] | [ ] |
| 04b | Recursion | | [ ] | [ ] | [ ] |
| 05 | Binary Search | | [ ] | [ ] | [ ] |
| 05b | Sorting | | [ ] | [ ] | [ ] |
| 06 | Linked Lists | | [ ] | [ ] | [ ] |
| 07 | Trees & BSTs | | [ ] | [ ] | [ ] |
| 08 | Tries | | [ ] | [ ] | [ ] |
| 09 | Heaps | | [ ] | [ ] | [ ] |
| 10 | Backtracking | | [ ] | [ ] | [ ] |
| 10b | Grids Primer | | [ ] | [ ] | [ ] |
| 11 | Graphs (BFS/DFS) | | [ ] | [ ] | [ ] |
| 12 | Union-Find | | [ ] | [ ] | [ ] |
| 13 | Advanced Graphs | | [ ] | [ ] | [ ] |
| 14 | 1-D DP | | [ ] | [ ] | [ ] |
| 15 | 2-D DP | | [ ] | [ ] | [ ] |
| 16 | Greedy | | [ ] | [ ] | [ ] |
| 17 | Intervals | | [ ] | [ ] | [ ] |
| 18 | Bit Manipulation | | [ ] | [ ] | [ ] |
| 19 | Math & Geometry | | [ ] | [ ] | [ ] |

---

## Phase Milestone Checkpoints

Complete each checkpoint before starting the next phase. These test whether the pattern recognition is real, not just code memorization.

---

### ✅ Phase 0–1 Checkpoint (before Phase 2)
*After: Foundations, Big-O Practice, Arrays & Hashing, Two Pointers, Sliding Window, Stacks & Queues, Recursion*

- [ ] Without looking at code, write the hash-map two-sum solution from scratch. State its Big-O.
- [ ] Without looking, write the two-pointer pair-sum-in-sorted-array solution. State its Big-O.
- [ ] Without looking, write the variable sliding-window template (longest substring with constraint).
- [ ] Draw the call stack for `factorial(4)` on paper. Count the frames.
- [ ] For the code below, state both time and space complexity:
  ```python
  for i in range(n):
      for j in range(i):
          seen.add((i, j))
  ```
- [ ] Solve [LeetCode 217 — Contains Duplicate](https://leetcode.com/problems/contains-duplicate/) and [LeetCode 3 — Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) cold (no hints).

---

### ✅ Phase 2 Checkpoint (before Phase 3)
*After: Binary Search, Sorting, Linked Lists*

- [ ] Write the binary-search template (lo/hi loop, mid, why `mid = lo + (hi-lo)//2` avoids overflow).
- [ ] Without looking, trace merge sort on `[3,1,2]`. Show the split and merge steps.
- [ ] Implement `reverse_linked_list` iteratively with a dummy head from memory.
- [ ] Solve [LeetCode 704 — Binary Search](https://leetcode.com/problems/binary-search/) and [LeetCode 206 — Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) cold.

---

### ✅ Phase 3 Checkpoint (before Phase 4)
*After: Trees & BSTs, Tries, Heaps*

- [ ] Write the base→recurse→combine DFS tree skeleton from memory.
- [ ] Write a `max_depth` function and an `is_balanced` function without any reference.
- [ ] Insert and search in a Trie from memory.
- [ ] Solve [LeetCode 104 — Maximum Depth of Binary Tree](https://leetcode.com/problems/maximum-depth-of-binary-tree/) and [LeetCode 347 — Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) cold.

---

### ✅ Phase 4 Checkpoint (before Phase 5)
*After: Backtracking, Grids Primer, Graphs, Union-Find, Advanced Graphs*

- [ ] Write the backtracking skeleton (choose/recurse/un-choose) for subsets from memory.
- [ ] Write BFS on a grid (shortest path) from memory, including bounds check.
- [ ] Write `numIslands` (DFS flood fill) from memory.
- [ ] Explain Dijkstra's algorithm — what data structure, why, what does it guarantee?
- [ ] Solve [LeetCode 200 — Number of Islands](https://leetcode.com/problems/number-of-islands/) and [LeetCode 46 — Permutations](https://leetcode.com/problems/permutations/) cold.

---

### ✅ Phase 5–6 Checkpoint (final mastery check)
*After: 1-D DP, 2-D DP, Greedy, Intervals, Bit Manipulation, Math & Geometry*

- [ ] Solve Climbing Stairs, House Robber, and Coin Change from memory — explain the state and transition for each.
- [ ] Fill the Unique-Paths grid for a 3×3 case by hand without code.
- [ ] Explain why a greedy solution works for Jump Game (LeetCode 55).
- [ ] Solve [LeetCode 70 — Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) and [LeetCode 62 — Unique Paths](https://leetcode.com/problems/unique-paths/) cold.
- [ ] 🔴 **Final cold solve:** pick any hard problem from `lists/recommended.md` without knowing its category. Identify the pattern first, then solve. If you can do this, you're ready for interviews.

---

## What "review" looks like in practice

A +3 day review (10–15 min):
1. Open the lesson. Read only the "Recognize this pattern when…" or "Concept" section headings.
2. Close the lesson. Write the template from memory.
3. Solve one 🟢 Easy problem from that lesson's practice set cold.

A +10 day review (20–30 min):
1. Same as above but solve one 🟡 Medium problem cold.

A +30 day review (30–45 min):
1. Solve one 🟡 Medium *and* attempt one 🔴 Hard, no hints.
2. If you struggle with the Hard, re-read the lesson once and retry.

---

*Practice lists: [recommended.md](../lists/recommended.md) · [rushed40.md](../lists/rushed40.md) · [Blind75](../lists/neetcodeblind75.md)*
