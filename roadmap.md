# DSA Roadmap

**153 problems · 131 core + 22 stretch · ≈183 h** — about 5–6 months at an hour a day, or 3 at two hours. Slower than the "Blind 75 in 30 days" posts promise; unlike them, it sticks.

The loop, per unit: read the lesson → type its [template](materials/appendix/templates/README.md) from memory → solve the core problems → tick the lesson's *Check Yourself* boxes → move on.

> **New to all of this?** Don't start at Unit 01. Open **Start here** below — it's a five-hour on-ramp that assumes nothing, not even that Python is installed.

**Every Hard is marked *(stretch)*.** Skip them on your first pass; a unit counts as complete without them. Come back at the end of the phase, when the pattern is automatic and the Hard is just a harder instance of it. Grinding Trapping Rain Water as your fourteenth-ever problem teaches nothing except that you're bad at this.

**This is the [NeetCode 150](lists/neetcode150.md) plus three.** [560 · Subarray Sum Equals K](materials/walkthroughs/560-subarray-sum-equals-k.md) is the exam for the prefix-sums lesson and one of the most-asked Mediums anywhere; [34 · Find First and Last Position](materials/walkthroughs/34-find-first-and-last-position-of-element-in-sorted-array.md) teaches binary search on a *boundary*, a distinct skill from [704](materials/walkthroughs/704-binary-search.md); [88 · Merge Sorted Array](materials/walkthroughs/88-merge-sorted-array.md) is a phone-screen staple. The 150 omits all three.

[🎯 Interview prep](interview.md) · [🧭 Study plan & retention](materials/guides/study-plan.md) · [📋 Blank tracker](blank-roadmap.md) · [📚 Materials](#materials)

---

## The four phases

| Phase | Units | Core | Stretch | ≈Hours | Where it gets you |
|-------|-------|------|---------|--------|-------------------|
| **Start here** | on-ramp | — | — | 5 | Python runs; you can read a problem and use LeetCode |
| **1 · Linear patterns** | 00–04 | 25 | 4 | 38 | Most Easies, and the Mediums that show up in screens |
| **2 · Recursion & structures** | 05–10 | 37 | 7 | 53 | Trees, heaps, linked lists — the phone-screen core |
| **3 · Search, graphs & DP** | 11–15 | 41 | 10 | 60 | **The junior→mid bar.** Onsite coding rounds |
| **4 · Rounding out** | 16–19 | 28 | 1 | 27 | Greedy and interval questions; the long tail |

**Where to stop.** Phases 1–3, core problems only, is a complete junior→mid coding prep: 103 problems, ≈151 h of units plus the five-hour on-ramp. Everything past that is polish — worth having, not worth delaying an application for. And if you have two weeks, not five months, stop reading this page and work the [Rushed 40](lists/rushed40.md) instead.

---

<a id="start-here"></a>

<details open>
<summary><b>Start here</b> — can you already code? · ≈5 h</summary>

This roadmap assumes you can write and run a Python function. It does **not** assume anything before that. If any line below is a "no", do it now — Big-O is meaningless before you can write a loop, and Unit 00 will feel like nonsense.

- [ ] Python installed, and a `.py` file you can actually run — [Installing Python](materials/guides/setup-python.md) · [Virtual environments](materials/guides/virtual-environments.md)
- [ ] An editor you're not fighting — [Editor setup](materials/guides/setup-editor.md)
- [ ] Enough terminal to run a file and move around — [Terminal basics](materials/guides/terminal-basics.md)
- [ ] I can write, from scratch: a `for` loop, a `while` loop, an `if/else`, a function, a list, a dict — [Python Syntax Cookbook](materials/syntax/_index.md)
- [ ] A LeetCode account, and I know how its editor works — [How to use LeetCode](materials/guides/how-to-use-leetcode.md)
- [ ] I can run and debug a solution on my own machine — [Testing locally](materials/guides/testing-locally.md) · [Debugging](materials/guides/debugging-python.md) · [Common Python errors](materials/guides/common-python-errors.md)
- [ ] I know what to do in the first five minutes with a problem I've never seen — [How to approach a problem](materials/guides/how-to-approach-a-problem.md)
- [ ] **I've read the study plan.** — [Study plan & retention](materials/guides/study-plan.md) ← the highest-return page in this repo. Read it before Unit 01, not after you've forgotten sliding window.
- [ ] Version control, so you don't lose work — [Git basics](materials/guides/git-basics.md) *(optional)*

</details>


<a id="phase-1"></a>

## Phase 1 · Linear patterns

*Units 00–04 · 25 core + 4 stretch · ≈38 h*

The vocabulary, then the scans: one pass, a hash map, two cursors, a stack. Nothing recursive yet. After this phase you can clear most Easies and the Mediums that show up in screens.

<details>
<summary><b>00 · Foundations</b> — 7 readings · ≈5 h</summary>

No problems here. Read these once, then never guess at a complexity again.

- [ ] [Data Structures](materials/learning/00a-data-structures.md) — What a data structure *is*, and matching structure to operation.
- [ ] [Algorithms](materials/learning/00b-algorithms.md) — Why two correct recipes differ wildly in speed.
- [ ] [Big O Notation](materials/learning/00c-big-o-notation.md) — The growth classes, O(1) → O(2ⁿ).
- [ ] [Time Complexity](materials/learning/00d-time-complexity.md) — Add sequential, multiply nested, halving = log.
- [ ] [Space Complexity](materials/learning/00e-space-complexity.md) — Counting extra memory, recursion depth included.
- [ ] [Foundations Practice](materials/learning/00f-foundations-practice.md) — Drills that make Unit 00 stick.
- [ ] [Pattern Recognition](materials/learning/00g-pattern-recognition.md) — How to read a cold problem statement and decide which data structure or algorithm it wants.

</details>

<details>
<summary><b>01 · Arrays & Hashing</b> — 10 core · ≈11 h · ✅</summary>

Trade memory for O(1) lookups; kill brute-force double loops.

[📖 Lesson](materials/learning/01-arrays-hashing.md) · [📖 Prefix sums](materials/learning/01b-prefix-sums.md)

- [x] **217** · Easy · Contains Duplicate · [LeetCode](https://leetcode.com/problems/contains-duplicate/) · [Solution](problems/0001-0499/217.py) · [Walkthrough](materials/walkthroughs/217-contains-duplicate.md)
- [x] **242** · Easy · Valid Anagram · [LeetCode](https://leetcode.com/problems/valid-anagram/) · [Solution](problems/0001-0499/242.py) · [Walkthrough](materials/walkthroughs/242-valid-anagram.md)
- [x] **1** · Easy · Two Sum · [LeetCode](https://leetcode.com/problems/two-sum/) · [Solution](problems/0001-0499/1.py) · [Walkthrough](materials/walkthroughs/1-two-sum.md)
- [x] **49** · Med · Group Anagrams · [LeetCode](https://leetcode.com/problems/group-anagrams/) · [Solution](problems/0001-0499/49.py) · [Walkthrough](materials/walkthroughs/49-group-anagrams.md)
- [x] **347** · Med · Top K Frequent Elements · [LeetCode](https://leetcode.com/problems/top-k-frequent-elements/) · [Solution](problems/0001-0499/347.py) · [Walkthrough](materials/walkthroughs/347-top-k-frequent-elements.md)
- [x] **238** · Med · Product of Array Except Self · [LeetCode](https://leetcode.com/problems/product-of-array-except-self/) · [Solution](problems/0001-0499/238.py) · [Walkthrough](materials/walkthroughs/238-product-of-array-except-self.md)
- [x] **560** · Med · Subarray Sum Equals K · [LeetCode](https://leetcode.com/problems/subarray-sum-equals-k/) · [Solution](problems/0500-0999/560.py) · [Walkthrough](materials/walkthroughs/560-subarray-sum-equals-k.md)
- [x] **36** · Med · Valid Sudoku · [LeetCode](https://leetcode.com/problems/valid-sudoku/) · [Solution](problems/0001-0499/36.py) · [Walkthrough](materials/walkthroughs/36-valid-sudoku.md)
- [x] **271** · Med · Encode and Decode Strings · [LeetCode](https://leetcode.com/problems/encode-and-decode-strings/) · [Solution](problems/0001-0499/271.py) · [Walkthrough](materials/walkthroughs/271-encode-and-decode-strings.md)
- [x] **128** · Med · Longest Consecutive Sequence · [LeetCode](https://leetcode.com/problems/longest-consecutive-sequence/) · [Solution](problems/0001-0499/128.py) · [Walkthrough](materials/walkthroughs/128-longest-consecutive-sequence.md)

</details>

<details>
<summary><b>02 · Two Pointers</b> — 5 core + 1 stretch · ≈7 h · ✅</summary>

Two cursors on a sorted array drop the O(n²).

[📖 Lesson](materials/learning/02-two-pointers.md)

- [x] **125** · Easy · Valid Palindrome · [LeetCode](https://leetcode.com/problems/valid-palindrome/) · [Solution](problems/0001-0499/125.py) · [Walkthrough](materials/walkthroughs/125-valid-palindrome.md)
- [x] **88** · Easy · Merge Sorted Array · [LeetCode](https://leetcode.com/problems/merge-sorted-array/) · [Solution](problems/0001-0499/88.py) · [Walkthrough](materials/walkthroughs/88-merge-sorted-array.md)
- [x] **167** · Med · Two Sum II · [LeetCode](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) · [Solution](problems/0001-0499/167.py) · [Walkthrough](materials/walkthroughs/167-two-sum-ii-input-array-is-sorted.md)
- [x] **15** · Med · 3Sum · [LeetCode](https://leetcode.com/problems/3sum/) · [Solution](problems/0001-0499/15.py) · [Walkthrough](materials/walkthroughs/15-3sum.md)
- [x] **11** · Med · Container With Most Water · [LeetCode](https://leetcode.com/problems/container-with-most-water/) · [Solution](problems/0001-0499/11.py) · [Walkthrough](materials/walkthroughs/11-container-with-most-water.md)
- [x] **42** · Hard *(stretch)* · Trapping Rain Water · [LeetCode](https://leetcode.com/problems/trapping-rain-water/) · [Solution](problems/0001-0499/42.py) · [Walkthrough](materials/walkthroughs/42-trapping-rain-water.md)

</details>

<details>
<summary><b>03 · Sliding Window</b> — 4 core + 2 stretch · ≈7 h · ✅</summary>

A moving boundary over contiguous ranges; O(n).

[📖 Lesson](materials/learning/03-sliding-window.md)

- [x] **121** · Easy · Best Time to Buy and Sell Stock · [LeetCode](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) · [Solution](problems/0001-0499/121.py) · [Walkthrough](materials/walkthroughs/121-best-time-to-buy-and-sell-stock.md)
- [x] **3** · Med · Longest Substring Without Repeating Characters · [LeetCode](https://leetcode.com/problems/longest-substring-without-repeating-characters/) · [Solution](problems/0001-0499/3.py) · [Walkthrough](materials/walkthroughs/3-longest-substring-without-repeating-characters.md)
- [x] **424** · Med · Longest Repeating Character Replacement · [LeetCode](https://leetcode.com/problems/longest-repeating-character-replacement/) · [Solution](problems/0001-0499/424.py) · [Walkthrough](materials/walkthroughs/424-longest-repeating-character-replacement.md)
- [x] **567** · Med · Permutation in String · [LeetCode](https://leetcode.com/problems/permutation-in-string/) · [Solution](problems/0500-0999/567.py) · [Walkthrough](materials/walkthroughs/567-permutation-in-string.md)
- [x] **76** · Hard *(stretch)* · Minimum Window Substring · [LeetCode](https://leetcode.com/problems/minimum-window-substring/) · [Solution](problems/0001-0499/76.py) · [Walkthrough](materials/walkthroughs/76-minimum-window-substring.md)
- [x] **239** · Hard *(stretch)* · Sliding Window Maximum · [LeetCode](https://leetcode.com/problems/sliding-window-maximum/) · [Solution](problems/0001-0499/239.py) · [Walkthrough](materials/walkthroughs/239-sliding-window-maximum.md)

</details>

<details>
<summary><b>04 · Stack</b> — 6 core + 1 stretch · ≈8 h · ✅</summary>

LIFO/FIFO for order-sensitive work; monotonic stack for next-greater.

[📖 Lesson](materials/learning/04-stack.md) · [📖 Recursion](materials/learning/05-recursion.md)

- [x] **20** · Easy · Valid Parentheses · [LeetCode](https://leetcode.com/problems/valid-parentheses/) · [Solution](problems/0001-0499/20.py) · [Walkthrough](materials/walkthroughs/20-valid-parentheses.md)
- [x] **155** · Med · Min Stack · [LeetCode](https://leetcode.com/problems/min-stack/) · [Solution](problems/0001-0499/155.py) · [Walkthrough](materials/walkthroughs/155-min-stack.md)
- [x] **150** · Med · Evaluate Reverse Polish Notation · [LeetCode](https://leetcode.com/problems/evaluate-reverse-polish-notation/) · [Solution](problems/0001-0499/150.py) · [Walkthrough](materials/walkthroughs/150-evaluate-reverse-polish-notation.md)
- [x] **22** · Med · Generate Parentheses · [LeetCode](https://leetcode.com/problems/generate-parentheses/) · [Solution](problems/0001-0499/22.py) · [Walkthrough](materials/walkthroughs/22-generate-parentheses.md)
- [x] **739** · Med · Daily Temperatures · [LeetCode](https://leetcode.com/problems/daily-temperatures/) · [Solution](problems/0500-0999/739.py) · [Walkthrough](materials/walkthroughs/739-daily-temperatures.md)
- [x] **853** · Med · Car Fleet · [LeetCode](https://leetcode.com/problems/car-fleet/) · [Solution](problems/0500-0999/853.py) · [Walkthrough](materials/walkthroughs/853-car-fleet.md)
- [x] **84** · Hard *(stretch)* · Largest Rectangle in Histogram · [LeetCode](https://leetcode.com/problems/largest-rectangle-in-histogram/) · [Solution](problems/0001-0499/84.py) · [Walkthrough](materials/walkthroughs/84-largest-rectangle-in-histogram.md)

</details>


<a id="phase-2"></a>

## Phase 2 · Recursion & core structures

*Units 05–10 · 37 core + 7 stretch · ≈53 h*

Recursion first, because everything after it is recursion in a costume. Then the structures interviewers reach for by default — binary search, linked lists, trees, tries, heaps. This is the phone-screen core.

<details>
<summary><b>05 · Recursion</b> — 5 drills · ≈5 h · <i>gate before Trees</i></summary>

No LeetCode problems — this one is a skills gate. The call stack *is* a stack, and Trees, Backtracking and both DP units are recursion wearing different clothes. Most people who stall out in DP are actually stalled here, nine units earlier.

[📖 Lesson](materials/learning/05-recursion.md) · [📖 The five drills](materials/rmap-practice/05-recursion.md) · [📖 Syntax: recursion basics](materials/syntax/recursion-basics.md)

- [ ] Write from scratch, no reference: `factorial`, `fibonacci` (naïve), `sum_of_list`, `power(base, n)`, `count_digits(n)`
- [ ] Trace a call stack by hand — predict the output *before* running it, then check
- [ ] Draw the recursion tree for `fibonacci(5)` and derive its Big-O from the shape
- [ ] Memoize naïve Fibonacci and time `fib(35)` both ways — that's your first DP solution
- [ ] State the space cost of each function you wrote (call-stack depth *is* memory)

**Don't open Unit 08 until all five are ticked.**

</details>

<details>
<summary><b>06 · Binary Search</b> — 7 core + 1 stretch · ≈9 h · 7/8 core done</summary>

Halve any ordered search space — including the answer.

[📖 Lesson](materials/learning/06-binary-search.md) · [📖 Sorting](materials/learning/06b-sorting.md)

- [x] **704** · Easy · Binary Search · [LeetCode](https://leetcode.com/problems/binary-search/) · [Solution](problems/0500-0999/704.py) · [Walkthrough](materials/walkthroughs/704-binary-search.md)
- [ ] **34** · Med · Find First and Last Position of Element in Sorted Array · [LeetCode](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/) · [Solution](problems/0001-0499/34.py) · [Walkthrough](materials/walkthroughs/34-find-first-and-last-position-of-element-in-sorted-array.md)
- [x] **74** · Med · Search a 2D Matrix · [LeetCode](https://leetcode.com/problems/search-a-2d-matrix/) · [Solution](problems/0001-0499/74.py) · [Walkthrough](materials/walkthroughs/74-search-a-2d-matrix.md)
- [x] **875** · Med · Koko Eating Bananas · [LeetCode](https://leetcode.com/problems/koko-eating-bananas/) · [Solution](problems/0500-0999/875.py) · [Walkthrough](materials/walkthroughs/875-koko-eating-bananas.md)
- [x] **153** · Med · Find Minimum in Rotated Sorted Array · [LeetCode](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/) · [Solution](problems/0001-0499/153.py) · [Walkthrough](materials/walkthroughs/153-find-minimum-in-rotated-sorted-array.md)
- [x] **33** · Med · Search in Rotated Sorted Array · [LeetCode](https://leetcode.com/problems/search-in-rotated-sorted-array/) · [Solution](problems/0001-0499/33.py) · [Walkthrough](materials/walkthroughs/33-search-in-rotated-sorted-array.md)
- [x] **981** · Med · Time Based Key-Value Store · [LeetCode](https://leetcode.com/problems/time-based-key-value-store/) · [Solution](problems/0500-0999/981.py) · [Walkthrough](materials/walkthroughs/981-time-based-key-value-store.md)
- [x] **4** · Hard *(stretch)* · Median of Two Sorted Arrays · [LeetCode](https://leetcode.com/problems/median-of-two-sorted-arrays/) · [Solution](problems/0001-0499/4.py) · [Walkthrough](materials/walkthroughs/4-median-of-two-sorted-arrays.md)

</details>

<details>
<summary><b>07 · Linked List</b> — 9 core + 2 stretch · ≈11 h · ✅</summary>

Pointer surgery: reverse, dummy head, fast/slow.

[📖 Lesson](materials/learning/07-linked-list.md)

- [x] **206** · Easy · Reverse Linked List · [LeetCode](https://leetcode.com/problems/reverse-linked-list/) · [Solution](problems/0001-0499/206.py) · [Walkthrough](materials/walkthroughs/206-reverse-linked-list.md)
- [x] **21** · Easy · Merge Two Sorted Lists · [LeetCode](https://leetcode.com/problems/merge-two-sorted-lists/) · [Solution](problems/0001-0499/21.py) · [Walkthrough](materials/walkthroughs/21-merge-two-sorted-lists.md)
- [x] **143** · Med · Reorder List · [LeetCode](https://leetcode.com/problems/reorder-list/) · [Solution](problems/0001-0499/143.py) · [Walkthrough](materials/walkthroughs/143-reorder-list.md)
- [x] **19** · Med · Remove Nth Node From End of List · [LeetCode](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) · [Solution](problems/0001-0499/19.py) · [Walkthrough](materials/walkthroughs/19-remove-nth-node-from-end-of-list.md)
- [x] **138** · Med · Copy List with Random Pointer · [LeetCode](https://leetcode.com/problems/copy-list-with-random-pointer/) · [Solution](problems/0001-0499/138.py) · [Walkthrough](materials/walkthroughs/138-copy-list-with-random-pointer.md)
- [x] **2** · Med · Add Two Numbers · [LeetCode](https://leetcode.com/problems/add-two-numbers/) · [Solution](problems/0001-0499/2.py) · [Walkthrough](materials/walkthroughs/2-add-two-numbers.md)
- [x] **141** · Easy · Linked List Cycle · [LeetCode](https://leetcode.com/problems/linked-list-cycle/) · [Solution](problems/0001-0499/141.py) · [Walkthrough](materials/walkthroughs/141-linked-list-cycle.md)
- [x] **287** · Med · Find the Duplicate Number · [LeetCode](https://leetcode.com/problems/find-the-duplicate-number/) · [Solution](problems/0001-0499/287.py) · [Walkthrough](materials/walkthroughs/287-find-the-duplicate-number.md)
- [x] **146** · Med · LRU Cache · [LeetCode](https://leetcode.com/problems/lru-cache/) · [Solution](problems/0001-0499/146.py) · [Walkthrough](materials/walkthroughs/146-lru-cache.md)
- [x] **23** · Hard *(stretch)* · Merge k Sorted Lists · [LeetCode](https://leetcode.com/problems/merge-k-sorted-lists/) · [Solution](problems/0001-0499/23.py) · [Walkthrough](materials/walkthroughs/23-merge-k-sorted-lists.md)
- [x] **25** · Hard *(stretch)* · Reverse Nodes in k-Group · [LeetCode](https://leetcode.com/problems/reverse-nodes-in-k-group/) · [Solution](problems/0001-0499/25.py) · [Walkthrough](materials/walkthroughs/25-reverse-nodes-in-k-group.md)

</details>

<details>
<summary><b>08 · Trees & BSTs</b> — 13 core + 2 stretch · ≈16 h · ✅</summary>

DFS base→recurse→combine, or BFS level-by-level.

**Prerequisite: Unit 05.** Every problem here is *base case → recurse → combine*. If the recursion drills aren't ticked, go back — it is faster than pushing forward.

[📖 Lesson](materials/learning/08-trees.md)

- [x] **226** · Easy · Invert Binary Tree · [LeetCode](https://leetcode.com/problems/invert-binary-tree/) · [Solution](problems/0001-0499/226.py) · [Walkthrough](materials/walkthroughs/226-invert-binary-tree.md)
- [x] **104** · Easy · Maximum Depth of Binary Tree · [LeetCode](https://leetcode.com/problems/maximum-depth-of-binary-tree/) · [Solution](problems/0001-0499/104.py) · [Walkthrough](materials/walkthroughs/104-maximum-depth-of-binary-tree.md)
- [x] **543** · Easy · Diameter of Binary Tree · [LeetCode](https://leetcode.com/problems/diameter-of-binary-tree/) · [Solution](problems/0500-0999/543.py) · [Walkthrough](materials/walkthroughs/543-diameter-of-binary-tree.md)
- [x] **110** · Easy · Balanced Binary Tree · [LeetCode](https://leetcode.com/problems/balanced-binary-tree/) · [Solution](problems/0001-0499/110.py) · [Walkthrough](materials/walkthroughs/110-balanced-binary-tree.md)
- [x] **100** · Easy · Same Tree · [LeetCode](https://leetcode.com/problems/same-tree/) · [Solution](problems/0001-0499/100.py) · [Walkthrough](materials/walkthroughs/100-same-tree.md)
- [x] **572** · Easy · Subtree of Another Tree · [LeetCode](https://leetcode.com/problems/subtree-of-another-tree/) · [Solution](problems/0500-0999/572.py) · [Walkthrough](materials/walkthroughs/572-subtree-of-another-tree.md)
- [x] **235** · Med · Lowest Common Ancestor of a Binary Search Tree · [LeetCode](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/) · [Solution](problems/0001-0499/235.py) · [Walkthrough](materials/walkthroughs/235-lowest-common-ancestor-of-a-binary-search-tree.md)
- [x] **102** · Med · Binary Tree Level Order Traversal · [LeetCode](https://leetcode.com/problems/binary-tree-level-order-traversal/) · [Solution](problems/0001-0499/102.py) · [Walkthrough](materials/walkthroughs/102-binary-tree-level-order-traversal.md)
- [x] **199** · Med · Binary Tree Right Side View · [LeetCode](https://leetcode.com/problems/binary-tree-right-side-view/) · [Solution](problems/0001-0499/199.py) · [Walkthrough](materials/walkthroughs/199-binary-tree-right-side-view.md)
- [x] **1448** · Med · Count Good Nodes in Binary Tree · [LeetCode](https://leetcode.com/problems/count-good-nodes-in-binary-tree/) · [Solution](problems/1000-1499/1448.py) · [Walkthrough](materials/walkthroughs/1448-count-good-nodes-in-binary-tree.md)
- [x] **98** · Med · Validate Binary Search Tree · [LeetCode](https://leetcode.com/problems/validate-binary-search-tree/) · [Solution](problems/0001-0499/98.py) · [Walkthrough](materials/walkthroughs/98-validate-binary-search-tree.md)
- [x] **230** · Med · Kth Smallest Element in a BST · [LeetCode](https://leetcode.com/problems/kth-smallest-element-in-a-bst/) · [Solution](problems/0001-0499/230.py) · [Walkthrough](materials/walkthroughs/230-kth-smallest-element-in-a-bst.md)
- [x] **105** · Med · Construct Binary Tree from Preorder and Inorder Traversal · [LeetCode](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/) · [Solution](problems/0001-0499/105.py) · [Walkthrough](materials/walkthroughs/105-construct-binary-tree-from-preorder-and-inorder-traversal.md)
- [x] **124** · Hard *(stretch)* · Binary Tree Maximum Path Sum · [LeetCode](https://leetcode.com/problems/binary-tree-maximum-path-sum/) · [Solution](problems/0001-0499/124.py) · [Walkthrough](materials/walkthroughs/124-binary-tree-maximum-path-sum.md)
- [x] **297** · Hard *(stretch)* · Serialize and Deserialize Binary Tree · [LeetCode](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) · [Solution](problems/0001-0499/297.py) · [Walkthrough](materials/walkthroughs/297-serialize-and-deserialize-binary-tree.md)

</details>

<details>
<summary><b>09 · Tries</b> — 2 core + 1 stretch · ≈4 h · ✅</summary>

Prefix trees: O(k) prefix queries.

[📖 Lesson](materials/learning/09-tries.md)

- [x] **208** · Med · Implement Trie (Prefix Tree) · [LeetCode](https://leetcode.com/problems/implement-trie-prefix-tree/) · [Solution](problems/0001-0499/208.py) · [Walkthrough](materials/walkthroughs/208-implement-trie-prefix-tree.md)
- [x] **211** · Med · Design Add and Search Words Data Structure · [LeetCode](https://leetcode.com/problems/design-add-and-search-words-data-structure/) · [Solution](problems/0001-0499/211.py) · [Walkthrough](materials/walkthroughs/211-design-add-and-search-words-data-structure.md)
- [x] **212** · Hard *(stretch)* · Word Search II · [LeetCode](https://leetcode.com/problems/word-search-ii/) · [Solution](problems/0001-0499/212.py) · [Walkthrough](materials/walkthroughs/212-word-search-ii.md)

</details>

<details>
<summary><b>10 · Heap / Priority Queue</b> — 6 core + 1 stretch · ≈8 h · ✅</summary>

The always-available extreme element; top-K & streaming.

[📖 Lesson](materials/learning/10-heap-priority-queue.md)

- [x] **703** · Easy · Kth Largest Element in a Stream · [LeetCode](https://leetcode.com/problems/kth-largest-element-in-a-stream/) · [Solution](problems/0500-0999/703.py) · [Walkthrough](materials/walkthroughs/703-kth-largest-element-in-a-stream.md)
- [x] **1046** · Easy · Last Stone Weight · [LeetCode](https://leetcode.com/problems/last-stone-weight/) · [Solution](problems/1000-1499/1046.py) · [Walkthrough](materials/walkthroughs/1046-last-stone-weight.md)
- [x] **973** · Med · K Closest Points to Origin · [LeetCode](https://leetcode.com/problems/k-closest-points-to-origin/) · [Solution](problems/0500-0999/973.py) · [Walkthrough](materials/walkthroughs/973-k-closest-points-to-origin.md)
- [x] **215** · Med · Kth Largest Element in an Array · [LeetCode](https://leetcode.com/problems/kth-largest-element-in-an-array/) · [Solution](problems/0001-0499/215.py) · [Walkthrough](materials/walkthroughs/215-kth-largest-element-in-an-array.md)
- [x] **621** · Med · Task Scheduler · [LeetCode](https://leetcode.com/problems/task-scheduler/) · [Solution](problems/0500-0999/621.py) · [Walkthrough](materials/walkthroughs/621-task-scheduler.md)
- [x] **355** · Med · Design Twitter · [LeetCode](https://leetcode.com/problems/design-twitter/) · [Solution](problems/0001-0499/355.py) · [Walkthrough](materials/walkthroughs/355-design-twitter.md)
- [x] **295** · Hard *(stretch)* · Find Median from Data Stream · [LeetCode](https://leetcode.com/problems/find-median-from-data-stream/) · [Solution](problems/0001-0499/295.py) · [Walkthrough](materials/walkthroughs/295-find-median-from-data-stream.md)

</details>


<a id="phase-3"></a>

## Phase 3 · Search, graphs & DP

*Units 11–15 · 41 core + 10 stretch · ≈60 h*

The three hardest families, and the ones onsite rounds actually reach for. **This is where the junior→mid bar sits** — clear Phases 1–3 and you are prepared for the coding rounds.

<details>
<summary><b>11 · Backtracking</b> — 8 core + 1 stretch · ≈10 h · ✅</summary>

Choose → explore → un-choose over partial solutions.

[📖 Lesson](materials/learning/11-backtracking.md)

- [x] **78** · Med · Subsets · [LeetCode](https://leetcode.com/problems/subsets/) · [Solution](problems/0001-0499/78.py) · [Walkthrough](materials/walkthroughs/78-subsets.md)
- [x] **39** · Med · Combination Sum · [LeetCode](https://leetcode.com/problems/combination-sum/) · [Solution](problems/0001-0499/39.py) · [Walkthrough](materials/walkthroughs/39-combination-sum.md)
- [x] **46** · Med · Permutations · [LeetCode](https://leetcode.com/problems/permutations/) · [Solution](problems/0001-0499/46.py) · [Walkthrough](materials/walkthroughs/46-permutations.md)
- [x] **90** · Med · Subsets II · [LeetCode](https://leetcode.com/problems/subsets-ii/) · [Solution](problems/0001-0499/90.py) · [Walkthrough](materials/walkthroughs/90-subsets-ii.md)
- [x] **40** · Med · Combination Sum II · [LeetCode](https://leetcode.com/problems/combination-sum-ii/) · [Solution](problems/0001-0499/40.py) · [Walkthrough](materials/walkthroughs/40-combination-sum-ii.md)
- [x] **79** · Med · Word Search · [LeetCode](https://leetcode.com/problems/word-search/) · [Solution](problems/0001-0499/79.py) · [Walkthrough](materials/walkthroughs/79-word-search.md)
- [x] **131** · Med · Palindrome Partitioning · [LeetCode](https://leetcode.com/problems/palindrome-partitioning/) · [Solution](problems/0001-0499/131.py) · [Walkthrough](materials/walkthroughs/131-palindrome-partitioning.md)
- [x] **17** · Med · Letter Combinations of a Phone Number · [LeetCode](https://leetcode.com/problems/letter-combinations-of-a-phone-number/) · [Solution](problems/0001-0499/17.py) · [Walkthrough](materials/walkthroughs/17-letter-combinations-of-a-phone-number.md)
- [x] **51** · Hard *(stretch)* · N-Queens · [LeetCode](https://leetcode.com/problems/n-queens/) · [Solution](problems/0001-0499/51.py) · [Walkthrough](materials/walkthroughs/51-n-queens.md)

</details>

<details>
<summary><b>12 · Graphs</b> — 12 core + 1 stretch · ≈14 h · ✅</summary>

BFS for shortest unweighted paths, DFS for connectivity.

Do the [grids primer](materials/learning/11b-grids-primer.md) first if you haven't — half these problems are grids wearing a graph costume.

[📖 Lesson](materials/learning/12-graphs.md) · [📖 Grids primer](materials/learning/11b-grids-primer.md) · [📖 Union-Find](materials/learning/12b-union-find.md)

- [x] **200** · Med · Number of Islands · [LeetCode](https://leetcode.com/problems/number-of-islands/) · [Solution](problems/0001-0499/200.py) · [Walkthrough](materials/walkthroughs/200-number-of-islands.md)
- [x] **133** · Med · Clone Graph · [LeetCode](https://leetcode.com/problems/clone-graph/) · [Solution](problems/0001-0499/133.py) · [Walkthrough](materials/walkthroughs/133-clone-graph.md)
- [x] **695** · Med · Max Area of Island · [LeetCode](https://leetcode.com/problems/max-area-of-island/) · [Solution](problems/0500-0999/695.py) · [Walkthrough](materials/walkthroughs/695-max-area-of-island.md)
- [x] **417** · Med · Pacific Atlantic Water Flow · [LeetCode](https://leetcode.com/problems/pacific-atlantic-water-flow/) · [Solution](problems/0001-0499/417.py) · [Walkthrough](materials/walkthroughs/417-pacific-atlantic-water-flow.md)
- [x] **130** · Med · Surrounded Regions · [LeetCode](https://leetcode.com/problems/surrounded-regions/) · [Solution](problems/0001-0499/130.py) · [Walkthrough](materials/walkthroughs/130-surrounded-regions.md)
- [x] **994** · Med · Rotting Oranges · [LeetCode](https://leetcode.com/problems/rotting-oranges/) · [Solution](problems/0500-0999/994.py) · [Walkthrough](materials/walkthroughs/994-rotting-oranges.md)
- [x] **286** · Med · Walls and Gates · [LeetCode](https://leetcode.com/problems/walls-and-gates/) · [Solution](problems/0001-0499/286.py) · [Walkthrough](materials/walkthroughs/286-walls-and-gates.md)
- [x] **207** · Med · Course Schedule · [LeetCode](https://leetcode.com/problems/course-schedule/) · [Solution](problems/0001-0499/207.py) · [Walkthrough](materials/walkthroughs/207-course-schedule.md)
- [x] **210** · Med · Course Schedule II · [LeetCode](https://leetcode.com/problems/course-schedule-ii/) · [Solution](problems/0001-0499/210.py) · [Walkthrough](materials/walkthroughs/210-course-schedule-ii.md)
- [x] **684** · Med · Redundant Connection · [LeetCode](https://leetcode.com/problems/redundant-connection/) · [Solution](problems/0500-0999/684.py) · [Walkthrough](materials/walkthroughs/684-redundant-connection.md)
- [x] **323** · Med · Number of Connected Components in an Undirected Graph · [LeetCode](https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/) · [Solution](problems/0001-0499/323.py) · [Walkthrough](materials/walkthroughs/323-number-of-connected-components-in-an-undirected-graph.md)
- [x] **261** · Med · Graph Valid Tree · [LeetCode](https://leetcode.com/problems/graph-valid-tree/) · [Solution](problems/0001-0499/261.py) · [Walkthrough](materials/walkthroughs/261-graph-valid-tree.md)
- [x] **127** · Hard *(stretch)* · Word Ladder · [LeetCode](https://leetcode.com/problems/word-ladder/) · [Solution](problems/0001-0499/127.py) · [Walkthrough](materials/walkthroughs/127-word-ladder.md)

</details>

<details>
<summary><b>13 · Advanced Graphs</b> — 3 core + 3 stretch · ≈8 h · ✅</summary>

Weighted shortest paths (Dijkstra), ordering (topo sort).

[📖 Lesson](materials/learning/13-advanced-graphs.md)

- [x] **332** · Hard *(stretch)* · Reconstruct Itinerary · [LeetCode](https://leetcode.com/problems/reconstruct-itinerary/) · [Solution](problems/0001-0499/332.py) · [Walkthrough](materials/walkthroughs/332-reconstruct-itinerary.md)
- [x] **1584** · Med · Min Cost to Connect All Points · [LeetCode](https://leetcode.com/problems/min-cost-to-connect-all-points/) · [Solution](problems/1500-1999/1584.py) · [Walkthrough](materials/walkthroughs/1584-min-cost-to-connect-all-points.md)
- [x] **743** · Med · Network Delay Time · [LeetCode](https://leetcode.com/problems/network-delay-time/) · [Solution](problems/0500-0999/743.py) · [Walkthrough](materials/walkthroughs/743-network-delay-time.md)
- [x] **778** · Hard *(stretch)* · Swim in Rising Water · [LeetCode](https://leetcode.com/problems/swim-in-rising-water/) · [Solution](problems/0500-0999/778.py) · [Walkthrough](materials/walkthroughs/778-swim-in-rising-water.md)
- [x] **269** · Hard *(stretch)* · Alien Dictionary · [LeetCode](https://leetcode.com/problems/alien-dictionary/) · [Solution](problems/0001-0499/269.py) · [Walkthrough](materials/walkthroughs/269-alien-dictionary.md)
- [x] **787** · Med · Cheapest Flights Within K Stops · [LeetCode](https://leetcode.com/problems/cheapest-flights-within-k-stops/) · [Solution](problems/0500-0999/787.py) · [Walkthrough](materials/walkthroughs/787-cheapest-flights-within-k-stops.md)

</details>

<details>
<summary><b>14 · 1-D Dynamic Programming</b> — 12 core · ≈14 h · ✅</summary>

State + transition + base case over one axis.

Feeling lost here almost always means a recursion gap, not a DP gap. Re-do [Unit 05](materials/rmap-practice/05-recursion.md) before you grind this one.

[📖 Lesson](materials/learning/14-dp-1d.md)

- [x] **70** · Easy · Climbing Stairs · [LeetCode](https://leetcode.com/problems/climbing-stairs/) · [Solution](problems/0001-0499/70.py) · [Walkthrough](materials/walkthroughs/70-climbing-stairs.md)
- [x] **746** · Easy · Min Cost Climbing Stairs · [LeetCode](https://leetcode.com/problems/min-cost-climbing-stairs/) · [Solution](problems/0500-0999/746.py) · [Walkthrough](materials/walkthroughs/746-min-cost-climbing-stairs.md)
- [x] **198** · Med · House Robber · [LeetCode](https://leetcode.com/problems/house-robber/) · [Solution](problems/0001-0499/198.py) · [Walkthrough](materials/walkthroughs/198-house-robber.md)
- [x] **213** · Med · House Robber II · [LeetCode](https://leetcode.com/problems/house-robber-ii/) · [Solution](problems/0001-0499/213.py) · [Walkthrough](materials/walkthroughs/213-house-robber-ii.md)
- [x] **5** · Med · Longest Palindromic Substring · [LeetCode](https://leetcode.com/problems/longest-palindromic-substring/) · [Solution](problems/0001-0499/5.py) · [Walkthrough](materials/walkthroughs/5-longest-palindromic-substring.md)
- [x] **647** · Med · Palindromic Substrings · [LeetCode](https://leetcode.com/problems/palindromic-substrings/) · [Solution](problems/0500-0999/647.py) · [Walkthrough](materials/walkthroughs/647-palindromic-substrings.md)
- [x] **91** · Med · Decode Ways · [LeetCode](https://leetcode.com/problems/decode-ways/) · [Solution](problems/0001-0499/91.py) · [Walkthrough](materials/walkthroughs/91-decode-ways.md)
- [x] **322** · Med · Coin Change · [LeetCode](https://leetcode.com/problems/coin-change/) · [Solution](problems/0001-0499/322.py) · [Walkthrough](materials/walkthroughs/322-coin-change.md)
- [x] **152** · Med · Maximum Product Subarray · [LeetCode](https://leetcode.com/problems/maximum-product-subarray/) · [Solution](problems/0001-0499/152.py) · [Walkthrough](materials/walkthroughs/152-maximum-product-subarray.md)
- [x] **139** · Med · Word Break · [LeetCode](https://leetcode.com/problems/word-break/) · [Solution](problems/0001-0499/139.py) · [Walkthrough](materials/walkthroughs/139-word-break.md)
- [x] **300** · Med · Longest Increasing Subsequence · [LeetCode](https://leetcode.com/problems/longest-increasing-subsequence/) · [Solution](problems/0001-0499/300.py) · [Walkthrough](materials/walkthroughs/300-longest-increasing-subsequence.md)
- [x] **416** · Med · Partition Equal Subset Sum · [LeetCode](https://leetcode.com/problems/partition-equal-subset-sum/) · [Solution](problems/0001-0499/416.py) · [Walkthrough](materials/walkthroughs/416-partition-equal-subset-sum.md)

</details>

<details>
<summary><b>15 · 2-D Dynamic Programming</b> — 6 core + 5 stretch · ≈14 h · ✅</summary>

Same engine, two indices: grids and sequence pairs.

[📖 Lesson](materials/learning/15-dp-2d.md)

- [x] **62** · Med · Unique Paths · [LeetCode](https://leetcode.com/problems/unique-paths/) · [Solution](problems/0001-0499/62.py) · [Walkthrough](materials/walkthroughs/62-unique-paths.md)
- [x] **1143** · Med · Longest Common Subsequence · [LeetCode](https://leetcode.com/problems/longest-common-subsequence/) · [Solution](problems/1000-1499/1143.py) · [Walkthrough](materials/walkthroughs/1143-longest-common-subsequence.md)
- [x] **309** · Med · Best Time to Buy and Sell Stock with Cooldown · [LeetCode](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/) · [Solution](problems/0001-0499/309.py) · [Walkthrough](materials/walkthroughs/309-best-time-to-buy-and-sell-stock-with-cooldown.md)
- [x] **518** · Med · Coin Change II · [LeetCode](https://leetcode.com/problems/coin-change-ii/) · [Solution](problems/0500-0999/518.py) · [Walkthrough](materials/walkthroughs/518-coin-change-ii.md)
- [x] **494** · Med · Target Sum · [LeetCode](https://leetcode.com/problems/target-sum/) · [Solution](problems/0001-0499/494.py) · [Walkthrough](materials/walkthroughs/494-target-sum.md)
- [x] **97** · Med · Interleaving String · [LeetCode](https://leetcode.com/problems/interleaving-string/) · [Solution](problems/0001-0499/97.py) · [Walkthrough](materials/walkthroughs/97-interleaving-string.md)
- [x] **329** · Hard *(stretch)* · Longest Increasing Path in a Matrix · [LeetCode](https://leetcode.com/problems/longest-increasing-path-in-a-matrix/) · [Solution](problems/0001-0499/329.py) · [Walkthrough](materials/walkthroughs/329-longest-increasing-path-in-a-matrix.md)
- [x] **115** · Hard *(stretch)* · Distinct Subsequences · [LeetCode](https://leetcode.com/problems/distinct-subsequences/) · [Solution](problems/0001-0499/115.py) · [Walkthrough](materials/walkthroughs/115-distinct-subsequences.md)
- [x] **72** · Hard *(stretch)* · Edit Distance · [LeetCode](https://leetcode.com/problems/edit-distance/) · [Solution](problems/0001-0499/72.py) · [Walkthrough](materials/walkthroughs/72-edit-distance.md)
- [x] **312** · Hard *(stretch)* · Burst Balloons · [LeetCode](https://leetcode.com/problems/burst-balloons/) · [Solution](problems/0001-0499/312.py) · [Walkthrough](materials/walkthroughs/312-burst-balloons.md)
- [x] **10** · Hard *(stretch)* · Regular Expression Matching · [LeetCode](https://leetcode.com/problems/regular-expression-matching/) · [Solution](problems/0001-0499/10.py) · [Walkthrough](materials/walkthroughs/10-regular-expression-matching.md)

</details>


<a id="phase-4"></a>

## Phase 4 · Rounding out

*Units 16–19 · 28 core + 1 stretch · ≈27 h*

The long tail. Greedy and Intervals are common enough that you should do them before calling prep finished. Math & Geometry and Bit Manipulation are the lowest-yield units on this page — do them last, or skip them if a date is looming.

<details>
<summary><b>16 · Greedy</b> — 8 core · ≈8 h · ✅</summary>

Take the locally best choice; the proof is the hard part.

[📖 Lesson](materials/learning/16-greedy.md)

- [x] **53** · Med · Maximum Subarray · [LeetCode](https://leetcode.com/problems/maximum-subarray/) · [Solution](problems/0001-0499/53.py) · [Walkthrough](materials/walkthroughs/53-maximum-subarray.md)
- [x] **55** · Med · Jump Game · [LeetCode](https://leetcode.com/problems/jump-game/) · [Solution](problems/0001-0499/55.py) · [Walkthrough](materials/walkthroughs/55-jump-game.md)
- [x] **45** · Med · Jump Game II · [LeetCode](https://leetcode.com/problems/jump-game-ii/) · [Solution](problems/0001-0499/45.py) · [Walkthrough](materials/walkthroughs/45-jump-game-ii.md)
- [x] **134** · Med · Gas Station · [LeetCode](https://leetcode.com/problems/gas-station/) · [Solution](problems/0001-0499/134.py) · [Walkthrough](materials/walkthroughs/134-gas-station.md)
- [x] **846** · Med · Hand of Straights · [LeetCode](https://leetcode.com/problems/hand-of-straights/) · [Solution](problems/0500-0999/846.py) · [Walkthrough](materials/walkthroughs/846-hand-of-straights.md)
- [x] **1899** · Med · Merge Triplets to Form Target Triplet · [LeetCode](https://leetcode.com/problems/merge-triplets-to-form-target-triplet/) · [Solution](problems/1500-1999/1899.py) · [Walkthrough](materials/walkthroughs/1899-merge-triplets-to-form-target-triplet.md)
- [x] **763** · Med · Partition Labels · [LeetCode](https://leetcode.com/problems/partition-labels/) · [Solution](problems/0500-0999/763.py) · [Walkthrough](materials/walkthroughs/763-partition-labels.md)
- [x] **678** · Med · Valid Parenthesis String · [LeetCode](https://leetcode.com/problems/valid-parenthesis-string/) · [Solution](problems/0500-0999/678.py) · [Walkthrough](materials/walkthroughs/678-valid-parenthesis-string.md)

</details>

<details>
<summary><b>17 · Intervals</b> — 5 core + 1 stretch · ≈6 h · ✅</summary>

Sort first, then one linear sweep to merge / count.

[📖 Lesson](materials/learning/17-intervals.md)

- [x] **57** · Med · Insert Interval · [LeetCode](https://leetcode.com/problems/insert-interval/) · [Solution](problems/0001-0499/57.py) · [Walkthrough](materials/walkthroughs/57-insert-interval.md)
- [x] **56** · Med · Merge Intervals · [LeetCode](https://leetcode.com/problems/merge-intervals/) · [Solution](problems/0001-0499/56.py) · [Walkthrough](materials/walkthroughs/56-merge-intervals.md)
- [x] **435** · Med · Non-overlapping Intervals · [LeetCode](https://leetcode.com/problems/non-overlapping-intervals/) · [Solution](problems/0001-0499/435.py) · [Walkthrough](materials/walkthroughs/435-non-overlapping-intervals.md)
- [x] **252** · Easy · Meeting Rooms · [LeetCode](https://leetcode.com/problems/meeting-rooms/) · [Solution](problems/0001-0499/252.py) · [Walkthrough](materials/walkthroughs/252-meeting-rooms.md)
- [x] **253** · Med · Meeting Rooms II · [LeetCode](https://leetcode.com/problems/meeting-rooms-ii/) · [Solution](problems/0001-0499/253.py) · [Walkthrough](materials/walkthroughs/253-meeting-rooms-ii.md)
- [x] **1851** · Hard *(stretch)* · Minimum Interval to Include Each Query · [LeetCode](https://leetcode.com/problems/minimum-interval-to-include-each-query/) · [Solution](problems/1500-1999/1851.py) · [Walkthrough](materials/walkthroughs/1851-minimum-interval-to-include-each-query.md)

</details>

<details>
<summary><b>18 · Math & Geometry</b> — 8 core · ≈7 h · ✅</summary>

GCD, fast power, in-place matrix transforms.

[📖 Lesson](materials/learning/18-math-geometry.md)

- [x] **48** · Med · Rotate Image · [LeetCode](https://leetcode.com/problems/rotate-image/) · [Solution](problems/0001-0499/48.py) · [Walkthrough](materials/walkthroughs/48-rotate-image.md)
- [x] **54** · Med · Spiral Matrix · [LeetCode](https://leetcode.com/problems/spiral-matrix/) · [Solution](problems/0001-0499/54.py) · [Walkthrough](materials/walkthroughs/54-spiral-matrix.md)
- [x] **73** · Med · Set Matrix Zeroes · [LeetCode](https://leetcode.com/problems/set-matrix-zeroes/) · [Solution](problems/0001-0499/73.py) · [Walkthrough](materials/walkthroughs/73-set-matrix-zeroes.md)
- [x] **202** · Easy · Happy Number · [LeetCode](https://leetcode.com/problems/happy-number/) · [Solution](problems/0001-0499/202.py) · [Walkthrough](materials/walkthroughs/202-happy-number.md)
- [x] **66** · Easy · Plus One · [LeetCode](https://leetcode.com/problems/plus-one/) · [Solution](problems/0001-0499/66.py) · [Walkthrough](materials/walkthroughs/66-plus-one.md)
- [x] **50** · Med · Pow(x, n) · [LeetCode](https://leetcode.com/problems/powx-n/) · [Solution](problems/0001-0499/50.py) · [Walkthrough](materials/walkthroughs/50-pow-x-n.md)
- [x] **43** · Med · Multiply Strings · [LeetCode](https://leetcode.com/problems/multiply-strings/) · [Solution](problems/0001-0499/43.py) · [Walkthrough](materials/walkthroughs/43-multiply-strings.md)
- [x] **2013** · Med · Detect Squares · [LeetCode](https://leetcode.com/problems/detect-squares/) · [Solution](problems/2000-2499/2013.py) · [Walkthrough](materials/walkthroughs/2013-detect-squares.md)

</details>

<details>
<summary><b>19 · Bit Manipulation</b> — 7 core · ≈6 h · ✅</summary>

Masks, shifts, and XOR cancellation in O(1).

[📖 Lesson](materials/learning/19-bit-manipulation.md)

- [x] **136** · Easy · Single Number · [LeetCode](https://leetcode.com/problems/single-number/) · [Solution](problems/0001-0499/136.py) · [Walkthrough](materials/walkthroughs/136-single-number.md)
- [x] **191** · Easy · Number of 1 Bits · [LeetCode](https://leetcode.com/problems/number-of-1-bits/) · [Solution](problems/0001-0499/191.py) · [Walkthrough](materials/walkthroughs/191-number-of-1-bits.md)
- [x] **338** · Easy · Counting Bits · [LeetCode](https://leetcode.com/problems/counting-bits/) · [Solution](problems/0001-0499/338.py) · [Walkthrough](materials/walkthroughs/338-counting-bits.md)
- [x] **190** · Easy · Reverse Bits · [LeetCode](https://leetcode.com/problems/reverse-bits/) · [Solution](problems/0001-0499/190.py) · [Walkthrough](materials/walkthroughs/190-reverse-bits.md)
- [x] **268** · Easy · Missing Number · [LeetCode](https://leetcode.com/problems/missing-number/) · [Solution](problems/0001-0499/268.py) · [Walkthrough](materials/walkthroughs/268-missing-number.md)
- [x] **371** · Med · Sum of Two Integers · [LeetCode](https://leetcode.com/problems/sum-of-two-integers/) · [Solution](problems/0001-0499/371.py) · [Walkthrough](materials/walkthroughs/371-sum-of-two-integers.md)
- [x] **7** · Med · Reverse Integer · [LeetCode](https://leetcode.com/problems/reverse-integer/) · [Solution](problems/0001-0499/7.py) · [Walkthrough](materials/walkthroughs/7-reverse-integer.md)

</details>

---

## Materials

| Hub | What's inside |
|-----|---------------|
| [🎯 Interview Roadmap](interview.md) | Behavioral, the interview loop, and system design — paced against these units |
| [📋 Blank tracker](blank-roadmap.md) | This page with every box unticked — start here if the repo isn't yours |
| [Guides](materials/guides/_index.md) | Installing Python, editor/terminal/git setup, using LeetCode, debugging, study strategy |
| [Data Structures](materials/data-structures/_index.md) | One-structure-per-file reference pages (array → segment tree) |
| [Algorithms](materials/algorithms/_index.md) | One-algorithm-per-file reference pages (binary search → Dijkstra) |
| [Python Syntax Cookbook](materials/syntax/_index.md) | Every construct the solutions lean on |
| [Code Templates](materials/appendix/templates/README.md) | Per-pattern `template.py` skeletons to memorize |
| [Segment Trees](materials/learning/20-segment-trees.md) | Optional — beyond the NeetCode 150 |

**Other lists:** [Rushed 40](lists/rushed40.md) (fast pass) · [Blind 75](lists/neetcodeblind75.md) · [NeetCode 150](lists/neetcode150.md) (the spine of this page) · [NeetCode 250](lists/neetcode250.md) · [Recommended 300](lists/recommended.md)
