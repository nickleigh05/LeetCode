# DSA Roadmap

`█████████████████████░░░` **263/301** · walkthroughs written for 263 of 301 problems

Tap a unit → read the lesson → solve its problems → tick the box.

[🎯 Interview prep](interview.md) · [📚 Materials](#materials)

---

<details>
<summary><b>00 · Foundations</b> — the vocabulary everything else assumes</summary>

No problems here. Read these once, then never guess at a complexity again.

- [ ] [Data Structures](materials/learning/00a-data-structures.md) — What a data structure *is*, and matching structure to operation.
- [ ] [Algorithms](materials/learning/00b-algorithms.md) — Why two correct recipes differ wildly in speed.
- [ ] [Big O Notation](materials/learning/00c-big-o-notation.md) — The growth classes, O(1) → O(2ⁿ).
- [ ] [Time Complexity](materials/learning/00d-time-complexity.md) — Add sequential, multiply nested, halving = log.
- [ ] [Space Complexity](materials/learning/00e-space-complexity.md) — Counting extra memory, recursion depth included.
- [ ] [Foundations Practice](materials/learning/00f-foundations-practice.md) — Drills that make Phase 0 stick.
- [ ] [Pattern Recognition](materials/learning/00g-pattern-recognition.md) — How to read a cold problem statement and decide which data structure or algorithm it wants.

</details>

<details>
<summary><b>01 · Arrays & Hashing</b> — 24/24 ▓▓▓▓▓▓▓▓ ✅</summary>

Trade memory for O(1) lookups; kill brute-force double loops.

[📖 Lesson](materials/learning/01-arrays-hashing.md) · [📖 Prefix sums](materials/learning/01b-prefix-sums.md)

- [x] **1** · Easy · Two Sum · [LeetCode](https://leetcode.com/problems/two-sum/) · [Solution](problems/0001-0499/1.py) · [Walkthrough](materials/walkthroughs/1-two-sum.md)
- [x] **217** · Easy · Contains Duplicate · [LeetCode](https://leetcode.com/problems/contains-duplicate/) · [Solution](problems/0001-0499/217.py) · [Walkthrough](materials/walkthroughs/217-contains-duplicate.md)
- [x] **242** · Easy · Valid Anagram · [LeetCode](https://leetcode.com/problems/valid-anagram/) · [Solution](problems/0001-0499/242.py) · [Walkthrough](materials/walkthroughs/242-valid-anagram.md)
- [x] **14** · Easy · Longest Common Prefix · [LeetCode](https://leetcode.com/problems/longest-common-prefix/) · [Solution](problems/0001-0499/14.py) · [Walkthrough](materials/walkthroughs/14-longest-common-prefix.md)
- [x] **169** · Easy · Majority Element · [LeetCode](https://leetcode.com/problems/majority-element/) · [Solution](problems/0001-0499/169.py) · [Walkthrough](materials/walkthroughs/169-majority-element.md)
- [x] **26** · Easy · Remove Duplicates from Sorted Array · [LeetCode](https://leetcode.com/problems/remove-duplicates-from-sorted-array/) · [Solution](problems/0001-0499/26.py) · [Walkthrough](materials/walkthroughs/26-remove-duplicates-from-sorted-array.md)
- [x] **27** · Easy · Remove Element · [LeetCode](https://leetcode.com/problems/remove-element/) · [Solution](problems/0001-0499/27.py) · [Walkthrough](materials/walkthroughs/27-remove-element.md)
- [x] **66** · Easy · Plus One · [LeetCode](https://leetcode.com/problems/plus-one/) · [Solution](problems/0001-0499/66.py) · [Walkthrough](materials/walkthroughs/66-plus-one.md)
- [x] **88** · Easy · Merge Sorted Array · [LeetCode](https://leetcode.com/problems/merge-sorted-array/) · [Solution](problems/0001-0499/88.py) · [Walkthrough](materials/walkthroughs/88-merge-sorted-array.md)
- [x] **268** · Easy · Missing Number · [LeetCode](https://leetcode.com/problems/missing-number/) · [Solution](problems/0001-0499/268.py) · [Walkthrough](materials/walkthroughs/268-missing-number.md)
- [x] **448** · Easy · Find All Numbers Disappeared in an Array · [LeetCode](https://leetcode.com/problems/find-all-numbers-disappeared-in-an-array/) · [Solution](problems/0001-0499/448.py) · [Walkthrough](materials/walkthroughs/448-find-all-numbers-disappeared-in-an-array.md)
- [x] **1929** · Easy · Concatenation of Array · [LeetCode](https://leetcode.com/problems/concatenation-of-array/) · [Solution](problems/1500-1999/1929.py) · [Walkthrough](materials/walkthroughs/1929-concatenation-of-array.md)
- [x] **303** · Easy · Range Sum Query - Immutable · [LeetCode](https://leetcode.com/problems/range-sum-query-immutable/) · [Solution](problems/0001-0499/303.py) · [Walkthrough](materials/walkthroughs/303-range-sum-query-immutable.md)
- [x] **49** · Med · Group Anagrams · [LeetCode](https://leetcode.com/problems/group-anagrams/) · [Solution](problems/0001-0499/49.py) · [Walkthrough](materials/walkthroughs/49-group-anagrams.md)
- [x] **347** · Med · Top K Frequent Elements · [LeetCode](https://leetcode.com/problems/top-k-frequent-elements/) · [Solution](problems/0001-0499/347.py) · [Walkthrough](materials/walkthroughs/347-top-k-frequent-elements.md)
- [x] **238** · Med · Product of Array Except Self · [LeetCode](https://leetcode.com/problems/product-of-array-except-self/) · [Solution](problems/0001-0499/238.py) · [Walkthrough](materials/walkthroughs/238-product-of-array-except-self.md)
- [x] **271** · Med · Encode and Decode Strings · [LeetCode](https://leetcode.com/problems/encode-and-decode-strings/) · [Solution](problems/0001-0499/271.py) · [Walkthrough](materials/walkthroughs/271-encode-and-decode-strings.md)
- [x] **36** · Med · Valid Sudoku · [LeetCode](https://leetcode.com/problems/valid-sudoku/) · [Solution](problems/0001-0499/36.py) · [Walkthrough](materials/walkthroughs/36-valid-sudoku.md)
- [x] **380** · Med · Insert Delete GetRandom O(1) · [LeetCode](https://leetcode.com/problems/insert-delete-getrandom-o1/) · [Solution](problems/0001-0499/380.py) · [Walkthrough](materials/walkthroughs/380-insert-delete-getrandom-o1.md)
- [x] **128** · Med · Longest Consecutive Sequence · [LeetCode](https://leetcode.com/problems/longest-consecutive-sequence/) · [Solution](problems/0001-0499/128.py) · [Walkthrough](materials/walkthroughs/128-longest-consecutive-sequence.md)
- [x] **560** · Med · Subarray Sum Equals K · [LeetCode](https://leetcode.com/problems/subarray-sum-equals-k/) · [Solution](problems/0500-0999/560.py) · [Walkthrough](materials/walkthroughs/560-subarray-sum-equals-k.md)
- [x] **525** · Med · Contiguous Array · [LeetCode](https://leetcode.com/problems/contiguous-array/) · [Solution](problems/0500-0999/525.py) · [Walkthrough](materials/walkthroughs/525-contiguous-array.md)
- [x] **274** · Med · H-Index · [LeetCode](https://leetcode.com/problems/h-index/) · [Solution](problems/0001-0499/274.py) · [Walkthrough](materials/walkthroughs/274-h-index.md)
- [x] **41** · Hard · First Missing Positive · [LeetCode](https://leetcode.com/problems/first-missing-positive/) · [Solution](problems/0001-0499/41.py) · [Walkthrough](materials/walkthroughs/41-first-missing-positive.md)

</details>

<details>
<summary><b>02 · Two Pointers</b> — 14/14 ▓▓▓▓▓▓▓▓ ✅</summary>

Two cursors on a sorted array drop the O(n²).

[📖 Lesson](materials/learning/02-two-pointers.md)

- [x] **125** · Easy · Valid Palindrome · [LeetCode](https://leetcode.com/problems/valid-palindrome/) · [Solution](problems/0001-0499/125.py) · [Walkthrough](materials/walkthroughs/125-valid-palindrome.md)
- [x] **680** · Easy · Valid Palindrome II · [LeetCode](https://leetcode.com/problems/valid-palindrome-ii/) · [Solution](problems/0500-0999/680.py) · [Walkthrough](materials/walkthroughs/680-valid-palindrome-ii.md)
- [x] **283** · Easy · Move Zeroes · [LeetCode](https://leetcode.com/problems/move-zeroes/) · [Solution](problems/0001-0499/283.py) · [Walkthrough](materials/walkthroughs/283-move-zeroes.md)
- [x] **977** · Easy · Squares of a Sorted Array · [LeetCode](https://leetcode.com/problems/squares-of-a-sorted-array/) · [Solution](problems/0500-0999/977.py) · [Walkthrough](materials/walkthroughs/977-squares-of-a-sorted-array.md)
- [x] **344** · Easy · Reverse String · [LeetCode](https://leetcode.com/problems/reverse-string/) · [Solution](problems/0001-0499/344.py) · [Walkthrough](materials/walkthroughs/344-reverse-string.md)
- [x] **392** · Easy · Is Subsequence · [LeetCode](https://leetcode.com/problems/is-subsequence/) · [Solution](problems/0001-0499/392.py) · [Walkthrough](materials/walkthroughs/392-is-subsequence.md)
- [x] **1768** · Easy · Merge Strings Alternately · [LeetCode](https://leetcode.com/problems/merge-strings-alternately/) · [Solution](problems/1500-1999/1768.py) · [Walkthrough](materials/walkthroughs/1768-merge-strings-alternately.md)
- [x] **167** · Med · Two Sum II - Input Array Is Sorted · [LeetCode](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) · [Solution](problems/0001-0499/167.py) · [Walkthrough](materials/walkthroughs/167-two-sum-ii-input-array-is-sorted.md)
- [x] **15** · Med · 3Sum · [LeetCode](https://leetcode.com/problems/3sum/) · [Solution](problems/0001-0499/15.py) · [Walkthrough](materials/walkthroughs/15-3sum.md)
- [x] **16** · Med · 3Sum Closest · [LeetCode](https://leetcode.com/problems/3sum-closest/) · [Solution](problems/0001-0499/16.py) · [Walkthrough](materials/walkthroughs/16-3sum-closest.md)
- [x] **18** · Med · 4Sum · [LeetCode](https://leetcode.com/problems/4sum/) · [Solution](problems/0001-0499/18.py) · [Walkthrough](materials/walkthroughs/18-4sum.md)
- [x] **11** · Med · Container With Most Water · [LeetCode](https://leetcode.com/problems/container-with-most-water/) · [Solution](problems/0001-0499/11.py) · [Walkthrough](materials/walkthroughs/11-container-with-most-water.md)
- [x] **75** · Med · Sort Colors · [LeetCode](https://leetcode.com/problems/sort-colors/) · [Solution](problems/0001-0499/75.py) · [Walkthrough](materials/walkthroughs/75-sort-colors.md)
- [x] **42** · Hard · Trapping Rain Water · [LeetCode](https://leetcode.com/problems/trapping-rain-water/) · [Solution](problems/0001-0499/42.py) · [Walkthrough](materials/walkthroughs/42-trapping-rain-water.md)

</details>

<details>
<summary><b>03 · Sliding Window</b> — 14/14 ▓▓▓▓▓▓▓▓ ✅</summary>

A moving boundary over contiguous ranges; O(n).

[📖 Lesson](materials/learning/03-sliding-window.md)

- [x] **121** · Easy · Best Time to Buy and Sell Stock · [LeetCode](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) · [Solution](problems/0001-0499/121.py) · [Walkthrough](materials/walkthroughs/121-best-time-to-buy-and-sell-stock.md)
- [x] **219** · Easy · Contains Duplicate II · [LeetCode](https://leetcode.com/problems/contains-duplicate-ii/) · [Solution](problems/0001-0499/219.py) · [Walkthrough](materials/walkthroughs/219-contains-duplicate-ii.md)
- [x] **643** · Easy · Maximum Average Subarray I · [LeetCode](https://leetcode.com/problems/maximum-average-subarray-i/) · [Solution](problems/0500-0999/643.py) · [Walkthrough](materials/walkthroughs/643-maximum-average-subarray-i.md)
- [x] **3** · Med · Longest Substring Without Repeating Characters · [LeetCode](https://leetcode.com/problems/longest-substring-without-repeating-characters/) · [Solution](problems/0001-0499/3.py) · [Walkthrough](materials/walkthroughs/3-longest-substring-without-repeating-characters.md)
- [x] **424** · Med · Longest Repeating Character Replacement · [LeetCode](https://leetcode.com/problems/longest-repeating-character-replacement/) · [Solution](problems/0001-0499/424.py) · [Walkthrough](materials/walkthroughs/424-longest-repeating-character-replacement.md)
- [x] **567** · Med · Permutation in String · [LeetCode](https://leetcode.com/problems/permutation-in-string/) · [Solution](problems/0500-0999/567.py) · [Walkthrough](materials/walkthroughs/567-permutation-in-string.md)
- [x] **438** · Med · Find All Anagrams in a String · [LeetCode](https://leetcode.com/problems/find-all-anagrams-in-a-string/) · [Solution](problems/0001-0499/438.py) · [Walkthrough](materials/walkthroughs/438-find-all-anagrams-in-a-string.md)
- [x] **209** · Med · Minimum Size Subarray Sum · [LeetCode](https://leetcode.com/problems/minimum-size-subarray-sum/) · [Solution](problems/0001-0499/209.py) · [Walkthrough](materials/walkthroughs/209-minimum-size-subarray-sum.md)
- [x] **904** · Med · Fruit Into Baskets · [LeetCode](https://leetcode.com/problems/fruit-into-baskets/) · [Solution](problems/0500-0999/904.py) · [Walkthrough](materials/walkthroughs/904-fruit-into-baskets.md)
- [x] **1456** · Med · Maximum Number of Vowels in a Substring of Given Length · [LeetCode](https://leetcode.com/problems/maximum-number-of-vowels-in-a-substring-of-given-length/) · [Solution](problems/1000-1499/1456.py) · [Walkthrough](materials/walkthroughs/1456-maximum-number-of-vowels-in-a-substring-of-given-length.md)
- [x] **1004** · Med · Max Consecutive Ones III · [LeetCode](https://leetcode.com/problems/max-consecutive-ones-iii/) · [Solution](problems/1000-1499/1004.py) · [Walkthrough](materials/walkthroughs/1004-max-consecutive-ones-iii.md)
- [x] **1493** · Med · Longest Subarray of 1's After Deleting One Element · [LeetCode](https://leetcode.com/problems/longest-subarray-of-1s-after-deleting-one-element/) · [Solution](problems/1000-1499/1493.py) · [Walkthrough](materials/walkthroughs/1493-longest-subarray-of-1s-after-deleting-one-element.md)
- [x] **76** · Hard · Minimum Window Substring · [LeetCode](https://leetcode.com/problems/minimum-window-substring/) · [Solution](problems/0001-0499/76.py) · [Walkthrough](materials/walkthroughs/76-minimum-window-substring.md)
- [x] **239** · Hard · Sliding Window Maximum · [LeetCode](https://leetcode.com/problems/sliding-window-maximum/) · [Solution](problems/0001-0499/239.py) · [Walkthrough](materials/walkthroughs/239-sliding-window-maximum.md)

</details>

<details>
<summary><b>04 · Stack</b> — 16/16 ▓▓▓▓▓▓▓▓ ✅</summary>

LIFO/FIFO for order-sensitive work; monotonic stack for next-greater.

[📖 Lesson](materials/learning/04-stack.md) · [📖 Recursion](materials/learning/04b-recursion.md)

- [x] **20** · Easy · Valid Parentheses · [LeetCode](https://leetcode.com/problems/valid-parentheses/) · [Solution](problems/0001-0499/20.py) · [Walkthrough](materials/walkthroughs/20-valid-parentheses.md)
- [x] **682** · Easy · Baseball Game · [LeetCode](https://leetcode.com/problems/baseball-game/) · [Solution](problems/0500-0999/682.py) · [Walkthrough](materials/walkthroughs/682-baseball-game.md)
- [x] **496** · Easy · Next Greater Element I · [LeetCode](https://leetcode.com/problems/next-greater-element-i/) · [Solution](problems/0001-0499/496.py) · [Walkthrough](materials/walkthroughs/496-next-greater-element-i.md)
- [x] **225** · Easy · Implement Stack using Queues · [LeetCode](https://leetcode.com/problems/implement-stack-using-queues/) · [Solution](problems/0001-0499/225.py) · [Walkthrough](materials/walkthroughs/225-implement-stack-using-queues.md)
- [x] **232** · Easy · Implement Queue using Stacks · [LeetCode](https://leetcode.com/problems/implement-queue-using-stacks/) · [Solution](problems/0001-0499/232.py) · [Walkthrough](materials/walkthroughs/232-implement-queue-using-stacks.md)
- [x] **155** · Med · Min Stack · [LeetCode](https://leetcode.com/problems/min-stack/) · [Solution](problems/0001-0499/155.py) · [Walkthrough](materials/walkthroughs/155-min-stack.md)
- [x] **150** · Med · Evaluate Reverse Polish Notation · [LeetCode](https://leetcode.com/problems/evaluate-reverse-polish-notation/) · [Solution](problems/0001-0499/150.py) · [Walkthrough](materials/walkthroughs/150-evaluate-reverse-polish-notation.md)
- [x] **22** · Med · Generate Parentheses · [LeetCode](https://leetcode.com/problems/generate-parentheses/) · [Solution](problems/0001-0499/22.py) · [Walkthrough](materials/walkthroughs/22-generate-parentheses.md)
- [x] **739** · Med · Daily Temperatures · [LeetCode](https://leetcode.com/problems/daily-temperatures/) · [Solution](problems/0500-0999/739.py) · [Walkthrough](materials/walkthroughs/739-daily-temperatures.md)
- [x] **853** · Med · Car Fleet · [LeetCode](https://leetcode.com/problems/car-fleet/) · [Solution](problems/0500-0999/853.py) · [Walkthrough](materials/walkthroughs/853-car-fleet.md)
- [x] **901** · Med · Online Stock Span · [LeetCode](https://leetcode.com/problems/online-stock-span/) · [Solution](problems/0500-0999/901.py) · [Walkthrough](materials/walkthroughs/901-online-stock-span.md)
- [x] **71** · Med · Simplify Path · [LeetCode](https://leetcode.com/problems/simplify-path/) · [Solution](problems/0001-0499/71.py) · [Walkthrough](materials/walkthroughs/71-simplify-path.md)
- [x] **394** · Med · Decode String · [LeetCode](https://leetcode.com/problems/decode-string/) · [Solution](problems/0001-0499/394.py) · [Walkthrough](materials/walkthroughs/394-decode-string.md)
- [x] **503** · Med · Next Greater Element II · [LeetCode](https://leetcode.com/problems/next-greater-element-ii/) · [Solution](problems/0500-0999/503.py) · [Walkthrough](materials/walkthroughs/503-next-greater-element-ii.md)
- [x] **84** · Hard · Largest Rectangle in Histogram · [LeetCode](https://leetcode.com/problems/largest-rectangle-in-histogram/) · [Solution](problems/0001-0499/84.py) · [Walkthrough](materials/walkthroughs/84-largest-rectangle-in-histogram.md)
- [x] **85** · Hard · Maximal Rectangle · [LeetCode](https://leetcode.com/problems/maximal-rectangle/) · [Solution](problems/0001-0499/85.py) · [Walkthrough](materials/walkthroughs/85-maximal-rectangle.md)

</details>

<details>
<summary><b>05 · Binary Search</b> — 18/18 ▓▓▓▓▓▓▓▓ ✅</summary>

Halve any ordered search space — including the answer.

[📖 Lesson](materials/learning/05-binary-search.md) · [📖 Sorting](materials/learning/05b-sorting.md)

- [x] **704** · Easy · Binary Search · [LeetCode](https://leetcode.com/problems/binary-search/) · [Solution](problems/0500-0999/704.py) · [Walkthrough](materials/walkthroughs/704-binary-search.md)
- [x] **374** · Easy · Guess Number Higher or Lower · [LeetCode](https://leetcode.com/problems/guess-number-higher-or-lower/) · [Solution](problems/0001-0499/374.py) · [Walkthrough](materials/walkthroughs/374-guess-number-higher-or-lower.md)
- [x] **35** · Easy · Search Insert Position · [LeetCode](https://leetcode.com/problems/search-insert-position/) · [Solution](problems/0001-0499/35.py) · [Walkthrough](materials/walkthroughs/35-search-insert-position.md)
- [x] **278** · Easy · First Bad Version · [LeetCode](https://leetcode.com/problems/first-bad-version/) · [Solution](problems/0001-0499/278.py) · [Walkthrough](materials/walkthroughs/278-first-bad-version.md)
- [x] **69** · Easy · Sqrt(x) · [LeetCode](https://leetcode.com/problems/sqrtx/) · [Solution](problems/0001-0499/69.py) · [Walkthrough](materials/walkthroughs/69-sqrtx.md)
- [x] **367** · Easy · Valid Perfect Square · [LeetCode](https://leetcode.com/problems/valid-perfect-square/) · [Solution](problems/0001-0499/367.py) · [Walkthrough](materials/walkthroughs/367-valid-perfect-square.md)
- [x] **74** · Med · Search a 2D Matrix · [LeetCode](https://leetcode.com/problems/search-a-2d-matrix/) · [Solution](problems/0001-0499/74.py) · [Walkthrough](materials/walkthroughs/74-search-a-2d-matrix.md)
- [x] **875** · Med · Koko Eating Bananas · [LeetCode](https://leetcode.com/problems/koko-eating-bananas/) · [Solution](problems/0500-0999/875.py) · [Walkthrough](materials/walkthroughs/875-koko-eating-bananas.md)
- [x] **153** · Med · Find Minimum in Rotated Sorted Array · [LeetCode](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/) · [Solution](problems/0001-0499/153.py) · [Walkthrough](materials/walkthroughs/153-find-minimum-in-rotated-sorted-array.md)
- [x] **33** · Med · Search in Rotated Sorted Array · [LeetCode](https://leetcode.com/problems/search-in-rotated-sorted-array/) · [Solution](problems/0001-0499/33.py) · [Walkthrough](materials/walkthroughs/33-search-in-rotated-sorted-array.md)
- [x] **34** · Med · Find First and Last Position of Element in Sorted Array · [LeetCode](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/) · [Solution](problems/0001-0499/34.py) · [Walkthrough](materials/walkthroughs/34-find-first-and-last-position-of-element-in-sorted-array.md)
- [x] **162** · Med · Find Peak Element · [LeetCode](https://leetcode.com/problems/find-peak-element/) · [Solution](problems/0001-0499/162.py) · [Walkthrough](materials/walkthroughs/162-find-peak-element.md)
- [x] **540** · Med · Single Element in a Sorted Array · [LeetCode](https://leetcode.com/problems/single-element-in-a-sorted-array/) · [Solution](problems/0500-0999/540.py) · [Walkthrough](materials/walkthroughs/540-single-element-in-a-sorted-array.md)
- [x] **1011** · Med · Capacity To Ship Packages Within D Days · [LeetCode](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/) · [Solution](problems/1000-1499/1011.py) · [Walkthrough](materials/walkthroughs/1011-capacity-to-ship-packages-within-d-days.md)
- [x] **658** · Med · Find K Closest Elements · [LeetCode](https://leetcode.com/problems/find-k-closest-elements/) · [Solution](problems/0500-0999/658.py) · [Walkthrough](materials/walkthroughs/658-find-k-closest-elements.md)
- [x] **981** · Med · Time Based Key-Value Store · [LeetCode](https://leetcode.com/problems/time-based-key-value-store/) · [Solution](problems/0500-0999/981.py) · [Walkthrough](materials/walkthroughs/981-time-based-key-value-store.md)
- [x] **4** · Hard · Median of Two Sorted Arrays · [LeetCode](https://leetcode.com/problems/median-of-two-sorted-arrays/) · [Solution](problems/0001-0499/4.py) · [Walkthrough](materials/walkthroughs/4-median-of-two-sorted-arrays.md)
- [x] **410** · Hard · Split Array Largest Sum · [LeetCode](https://leetcode.com/problems/split-array-largest-sum/) · [Solution](problems/0001-0499/410.py) · [Walkthrough](materials/walkthroughs/410-split-array-largest-sum.md)

</details>

<details>
<summary><b>06 · Linked List</b> — 20/20 ▓▓▓▓▓▓▓▓ ✅</summary>

Pointer surgery: reverse, dummy head, fast/slow.

[📖 Lesson](materials/learning/06-linked-list.md)

- [x] **206** · Easy · Reverse Linked List · [LeetCode](https://leetcode.com/problems/reverse-linked-list/) · [Solution](problems/0001-0499/206.py) · [Walkthrough](materials/walkthroughs/206-reverse-linked-list.md)
- [x] **21** · Easy · Merge Two Sorted Lists · [LeetCode](https://leetcode.com/problems/merge-two-sorted-lists/) · [Solution](problems/0001-0499/21.py) · [Walkthrough](materials/walkthroughs/21-merge-two-sorted-lists.md)
- [x] **876** · Easy · Middle of the Linked List · [LeetCode](https://leetcode.com/problems/middle-of-the-linked-list/) · [Solution](problems/0500-0999/876.py) · [Walkthrough](materials/walkthroughs/876-middle-of-the-linked-list.md)
- [x] **141** · Easy · Linked List Cycle · [LeetCode](https://leetcode.com/problems/linked-list-cycle/) · [Solution](problems/0001-0499/141.py) · [Walkthrough](materials/walkthroughs/141-linked-list-cycle.md)
- [x] **234** · Easy · Palindrome Linked List · [LeetCode](https://leetcode.com/problems/palindrome-linked-list/) · [Solution](problems/0001-0499/234.py) · [Walkthrough](materials/walkthroughs/234-palindrome-linked-list.md)
- [x] **203** · Easy · Remove Linked List Elements · [LeetCode](https://leetcode.com/problems/remove-linked-list-elements/) · [Solution](problems/0001-0499/203.py) · [Walkthrough](materials/walkthroughs/203-remove-linked-list-elements.md)
- [x] **83** · Easy · Remove Duplicates from Sorted List · [LeetCode](https://leetcode.com/problems/remove-duplicates-from-sorted-list/) · [Solution](problems/0001-0499/83.py) · [Walkthrough](materials/walkthroughs/83-remove-duplicates-from-sorted-list.md)
- [x] **160** · Easy · Intersection of Two Linked Lists · [LeetCode](https://leetcode.com/problems/intersection-of-two-linked-lists/) · [Solution](problems/0001-0499/160.py) · [Walkthrough](materials/walkthroughs/160-intersection-of-two-linked-lists.md)
- [x] **143** · Med · Reorder List · [LeetCode](https://leetcode.com/problems/reorder-list/) · [Solution](problems/0001-0499/143.py) · [Walkthrough](materials/walkthroughs/143-reorder-list.md)
- [x] **19** · Med · Remove Nth Node From End of List · [LeetCode](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) · [Solution](problems/0001-0499/19.py) · [Walkthrough](materials/walkthroughs/19-remove-nth-node-from-end-of-list.md)
- [x] **92** · Med · Reverse Linked List II · [LeetCode](https://leetcode.com/problems/reverse-linked-list-ii/) · [Solution](problems/0001-0499/92.py) · [Walkthrough](materials/walkthroughs/92-reverse-linked-list-ii.md)
- [x] **24** · Med · Swap Nodes in Pairs · [LeetCode](https://leetcode.com/problems/swap-nodes-in-pairs/) · [Solution](problems/0001-0499/24.py) · [Walkthrough](materials/walkthroughs/24-swap-nodes-in-pairs.md)
- [x] **2** · Med · Add Two Numbers · [LeetCode](https://leetcode.com/problems/add-two-numbers/) · [Solution](problems/0001-0499/2.py) · [Walkthrough](materials/walkthroughs/2-add-two-numbers.md)
- [x] **138** · Med · Copy List with Random Pointer · [LeetCode](https://leetcode.com/problems/copy-list-with-random-pointer/) · [Solution](problems/0001-0499/138.py) · [Walkthrough](materials/walkthroughs/138-copy-list-with-random-pointer.md)
- [x] **287** · Med · Find the Duplicate Number · [LeetCode](https://leetcode.com/problems/find-the-duplicate-number/) · [Solution](problems/0001-0499/287.py) · [Walkthrough](materials/walkthroughs/287-find-the-duplicate-number.md)
- [x] **146** · Med · LRU Cache · [LeetCode](https://leetcode.com/problems/lru-cache/) · [Solution](problems/0001-0499/146.py) · [Walkthrough](materials/walkthroughs/146-lru-cache.md)
- [x] **61** · Med · Rotate List · [LeetCode](https://leetcode.com/problems/rotate-list/) · [Solution](problems/0001-0499/61.py) · [Walkthrough](materials/walkthroughs/61-rotate-list.md)
- [x] **86** · Med · Partition List · [LeetCode](https://leetcode.com/problems/partition-list/) · [Solution](problems/0001-0499/86.py) · [Walkthrough](materials/walkthroughs/86-partition-list.md)
- [x] **23** · Hard · Merge k Sorted Lists · [LeetCode](https://leetcode.com/problems/merge-k-sorted-lists/) · [Solution](problems/0001-0499/23.py) · [Walkthrough](materials/walkthroughs/23-merge-k-sorted-lists.md)
- [x] **25** · Hard · Reverse Nodes in k-Group · [LeetCode](https://leetcode.com/problems/reverse-nodes-in-k-group/) · [Solution](problems/0001-0499/25.py) · [Walkthrough](materials/walkthroughs/25-reverse-nodes-in-k-group.md)

</details>

<details>
<summary><b>07 · Trees & BSTs</b> — 29/29 ▓▓▓▓▓▓▓▓ ✅</summary>

DFS base→recurse→combine, or BFS level-by-level.

[📖 Lesson](materials/learning/07-trees.md)

- [x] **226** · Easy · Invert Binary Tree · [LeetCode](https://leetcode.com/problems/invert-binary-tree/) · [Solution](problems/0001-0499/226.py) · [Walkthrough](materials/walkthroughs/226-invert-binary-tree.md)
- [x] **104** · Easy · Maximum Depth of Binary Tree · [LeetCode](https://leetcode.com/problems/maximum-depth-of-binary-tree/) · [Solution](problems/0001-0499/104.py) · [Walkthrough](materials/walkthroughs/104-maximum-depth-of-binary-tree.md)
- [x] **543** · Easy · Diameter of Binary Tree · [LeetCode](https://leetcode.com/problems/diameter-of-binary-tree/) · [Solution](problems/0500-0999/543.py) · [Walkthrough](materials/walkthroughs/543-diameter-of-binary-tree.md)
- [x] **110** · Easy · Balanced Binary Tree · [LeetCode](https://leetcode.com/problems/balanced-binary-tree/) · [Solution](problems/0001-0499/110.py) · [Walkthrough](materials/walkthroughs/110-balanced-binary-tree.md)
- [x] **100** · Easy · Same Tree · [LeetCode](https://leetcode.com/problems/same-tree/) · [Solution](problems/0001-0499/100.py) · [Walkthrough](materials/walkthroughs/100-same-tree.md)
- [x] **572** · Easy · Subtree of Another Tree · [LeetCode](https://leetcode.com/problems/subtree-of-another-tree/) · [Solution](problems/0500-0999/572.py) · [Walkthrough](materials/walkthroughs/572-subtree-of-another-tree.md)
- [x] **112** · Easy · Path Sum · [LeetCode](https://leetcode.com/problems/path-sum/) · [Solution](problems/0001-0499/112.py) · [Walkthrough](materials/walkthroughs/112-path-sum.md)
- [x] **111** · Easy · Minimum Depth of Binary Tree · [LeetCode](https://leetcode.com/problems/minimum-depth-of-binary-tree/) · [Solution](problems/0001-0499/111.py) · [Walkthrough](materials/walkthroughs/111-minimum-depth-of-binary-tree.md)
- [x] **101** · Easy · Symmetric Tree · [LeetCode](https://leetcode.com/problems/symmetric-tree/) · [Solution](problems/0001-0499/101.py) · [Walkthrough](materials/walkthroughs/101-symmetric-tree.md)
- [x] **108** · Easy · Convert Sorted Array to Binary Search Tree · [LeetCode](https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/) · [Solution](problems/0001-0499/108.py) · [Walkthrough](materials/walkthroughs/108-convert-sorted-array-to-binary-search-tree.md)
- [x] **700** · Easy · Search in a Binary Search Tree · [LeetCode](https://leetcode.com/problems/search-in-a-binary-search-tree/) · [Solution](problems/0500-0999/700.py) · [Walkthrough](materials/walkthroughs/700-search-in-a-binary-search-tree.md)
- [x] **94** · Easy · Binary Tree Inorder Traversal · [LeetCode](https://leetcode.com/problems/binary-tree-inorder-traversal/) · [Solution](problems/0001-0499/94.py) · [Walkthrough](materials/walkthroughs/94-binary-tree-inorder-traversal.md)
- [x] **144** · Easy · Binary Tree Preorder Traversal · [LeetCode](https://leetcode.com/problems/binary-tree-preorder-traversal/) · [Solution](problems/0001-0499/144.py) · [Walkthrough](materials/walkthroughs/144-binary-tree-preorder-traversal.md)
- [x] **145** · Easy · Binary Tree Postorder Traversal · [LeetCode](https://leetcode.com/problems/binary-tree-postorder-traversal/) · [Solution](problems/0001-0499/145.py) · [Walkthrough](materials/walkthroughs/145-binary-tree-postorder-traversal.md)
- [x] **257** · Easy · Binary Tree Paths · [LeetCode](https://leetcode.com/problems/binary-tree-paths/) · [Solution](problems/0001-0499/257.py) · [Walkthrough](materials/walkthroughs/257-binary-tree-paths.md)
- [x] **235** · Med · Lowest Common Ancestor of a Binary Search Tree · [LeetCode](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/) · [Solution](problems/0001-0499/235.py) · [Walkthrough](materials/walkthroughs/235-lowest-common-ancestor-of-a-binary-search-tree.md)
- [x] **102** · Med · Binary Tree Level Order Traversal · [LeetCode](https://leetcode.com/problems/binary-tree-level-order-traversal/) · [Solution](problems/0001-0499/102.py) · [Walkthrough](materials/walkthroughs/102-binary-tree-level-order-traversal.md)
- [x] **199** · Med · Binary Tree Right Side View · [LeetCode](https://leetcode.com/problems/binary-tree-right-side-view/) · [Solution](problems/0001-0499/199.py) · [Walkthrough](materials/walkthroughs/199-binary-tree-right-side-view.md)
- [x] **1448** · Med · Count Good Nodes in Binary Tree · [LeetCode](https://leetcode.com/problems/count-good-nodes-in-binary-tree/) · [Solution](problems/1000-1499/1448.py) · [Walkthrough](materials/walkthroughs/1448-count-good-nodes-in-binary-tree.md)
- [x] **98** · Med · Validate Binary Search Tree · [LeetCode](https://leetcode.com/problems/validate-binary-search-tree/) · [Solution](problems/0001-0499/98.py) · [Walkthrough](materials/walkthroughs/98-validate-binary-search-tree.md)
- [x] **230** · Med · Kth Smallest Element in a BST · [LeetCode](https://leetcode.com/problems/kth-smallest-element-in-a-bst/) · [Solution](problems/0001-0499/230.py) · [Walkthrough](materials/walkthroughs/230-kth-smallest-element-in-a-bst.md)
- [x] **105** · Med · Construct Binary Tree from Preorder and Inorder Traversal · [LeetCode](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/) · [Solution](problems/0001-0499/105.py) · [Walkthrough](materials/walkthroughs/105-construct-binary-tree-from-preorder-and-inorder-traversal.md)
- [x] **701** · Med · Insert into a Binary Search Tree · [LeetCode](https://leetcode.com/problems/insert-into-a-binary-search-tree/) · [Solution](problems/0500-0999/701.py) · [Walkthrough](materials/walkthroughs/701-insert-into-a-binary-search-tree.md)
- [x] **450** · Med · Delete Node in a BST · [LeetCode](https://leetcode.com/problems/delete-node-in-a-bst/) · [Solution](problems/0001-0499/450.py) · [Walkthrough](materials/walkthroughs/450-delete-node-in-a-bst.md)
- [x] **116** · Med · Populating Next Right Pointers in Each Node · [LeetCode](https://leetcode.com/problems/populating-next-right-pointers-in-each-node/) · [Solution](problems/0001-0499/116.py) · [Walkthrough](materials/walkthroughs/116-populating-next-right-pointers-in-each-node.md)
- [x] **103** · Med · Binary Tree Zigzag Level Order Traversal · [LeetCode](https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/) · [Solution](problems/0001-0499/103.py) · [Walkthrough](materials/walkthroughs/103-binary-tree-zigzag-level-order-traversal.md)
- [x] **236** · Med · Lowest Common Ancestor of a Binary Tree · [LeetCode](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) · [Solution](problems/0001-0499/236.py) · [Walkthrough](materials/walkthroughs/236-lowest-common-ancestor-of-a-binary-tree.md)
- [x] **124** · Hard · Binary Tree Maximum Path Sum · [LeetCode](https://leetcode.com/problems/binary-tree-maximum-path-sum/) · [Solution](problems/0001-0499/124.py) · [Walkthrough](materials/walkthroughs/124-binary-tree-maximum-path-sum.md)
- [x] **297** · Hard · Serialize and Deserialize Binary Tree · [LeetCode](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) · [Solution](problems/0001-0499/297.py) · [Walkthrough](materials/walkthroughs/297-serialize-and-deserialize-binary-tree.md)

</details>

<details>
<summary><b>08 · Tries</b> — 6/6 ▓▓▓▓▓▓▓▓ ✅</summary>

Prefix trees: O(k) prefix queries.

[📖 Lesson](materials/learning/08-tries.md)

- [x] **208** · Med · Implement Trie (Prefix Tree) · [LeetCode](https://leetcode.com/problems/implement-trie-prefix-tree/) · [Solution](problems/0001-0499/208.py) · [Walkthrough](materials/walkthroughs/208-implement-trie-prefix-tree.md)
- [x] **211** · Med · Design Add and Search Words Data Structure · [LeetCode](https://leetcode.com/problems/design-add-and-search-words-data-structure/) · [Solution](problems/0001-0499/211.py) · [Walkthrough](materials/walkthroughs/211-design-add-and-search-words-data-structure.md)
- [x] **648** · Med · Replace Words · [LeetCode](https://leetcode.com/problems/replace-words/) · [Solution](problems/0500-0999/648.py) · [Walkthrough](materials/walkthroughs/648-replace-words.md)
- [x] **677** · Med · Map Sum Pairs · [LeetCode](https://leetcode.com/problems/map-sum-pairs/) · [Solution](problems/0500-0999/677.py) · [Walkthrough](materials/walkthroughs/677-map-sum-pairs.md)
- [x] **1268** · Med · Search Suggestions System · [LeetCode](https://leetcode.com/problems/search-suggestions-system/) · [Solution](problems/1000-1499/1268.py) · [Walkthrough](materials/walkthroughs/1268-search-suggestions-system.md)
- [x] **212** · Hard · Word Search II · [LeetCode](https://leetcode.com/problems/word-search-ii/) · [Solution](problems/0001-0499/212.py) · [Walkthrough](materials/walkthroughs/212-word-search-ii.md)

</details>

<details>
<summary><b>09 · Heap / Priority Queue</b> — 14/14 ▓▓▓▓▓▓▓▓ ✅</summary>

The always-available extreme element; top-K & streaming.

[📖 Lesson](materials/learning/09-heap-priority-queue.md)

- [x] **703** · Easy · Kth Largest Element in a Stream · [LeetCode](https://leetcode.com/problems/kth-largest-element-in-a-stream/) · [Solution](problems/0500-0999/703.py) · [Walkthrough](materials/walkthroughs/703-kth-largest-element-in-a-stream.md)
- [x] **1046** · Easy · Last Stone Weight · [LeetCode](https://leetcode.com/problems/last-stone-weight/) · [Solution](problems/1000-1499/1046.py) · [Walkthrough](materials/walkthroughs/1046-last-stone-weight.md)
- [x] **215** · Med · Kth Largest Element in an Array · [LeetCode](https://leetcode.com/problems/kth-largest-element-in-an-array/) · [Solution](problems/0001-0499/215.py) · [Walkthrough](materials/walkthroughs/215-kth-largest-element-in-an-array.md)
- [x] **973** · Med · K Closest Points to Origin · [LeetCode](https://leetcode.com/problems/k-closest-points-to-origin/) · [Solution](problems/0500-0999/973.py) · [Walkthrough](materials/walkthroughs/973-k-closest-points-to-origin.md)
- [x] **621** · Med · Task Scheduler · [LeetCode](https://leetcode.com/problems/task-scheduler/) · [Solution](problems/0500-0999/621.py) · [Walkthrough](materials/walkthroughs/621-task-scheduler.md)
- [x] **355** · Med · Design Twitter · [LeetCode](https://leetcode.com/problems/design-twitter/) · [Solution](problems/0001-0499/355.py) · [Walkthrough](materials/walkthroughs/355-design-twitter.md)
- [x] **692** · Med · Top K Frequent Words · [LeetCode](https://leetcode.com/problems/top-k-frequent-words/) · [Solution](problems/0500-0999/692.py) · [Walkthrough](materials/walkthroughs/692-top-k-frequent-words.md)
- [x] **767** · Med · Reorganize String · [LeetCode](https://leetcode.com/problems/reorganize-string/) · [Solution](problems/0500-0999/767.py) · [Walkthrough](materials/walkthroughs/767-reorganize-string.md)
- [x] **1834** · Med · Single-Threaded CPU · [LeetCode](https://leetcode.com/problems/single-threaded-cpu/) · [Solution](problems/1500-1999/1834.py) · [Walkthrough](materials/walkthroughs/1834-single-threaded-cpu.md)
- [x] **1985** · Med · Find the Kth Largest Integer in the Array · [LeetCode](https://leetcode.com/problems/find-the-kth-largest-integer-in-the-array/) · [Solution](problems/1500-1999/1985.py) · [Walkthrough](materials/walkthroughs/1985-find-the-kth-largest-integer-in-the-array.md)
- [x] **2542** · Med · Maximum Subsequence Score · [LeetCode](https://leetcode.com/problems/maximum-subsequence-score/) · [Solution](problems/2500-2999/2542.py) · [Walkthrough](materials/walkthroughs/2542-maximum-subsequence-score.md)
- [x] **1962** · Med · Remove Stones to Minimize the Total · [LeetCode](https://leetcode.com/problems/remove-stones-to-minimize-the-total/) · [Solution](problems/1500-1999/1962.py) · [Walkthrough](materials/walkthroughs/1962-remove-stones-to-minimize-the-total.md)
- [x] **295** · Hard · Find Median from Data Stream · [LeetCode](https://leetcode.com/problems/find-median-from-data-stream/) · [Solution](problems/0001-0499/295.py) · [Walkthrough](materials/walkthroughs/295-find-median-from-data-stream.md)
- [x] **502** · Hard · IPO · [LeetCode](https://leetcode.com/problems/ipo/) · [Solution](problems/0500-0999/502.py) · [Walkthrough](materials/walkthroughs/502-ipo.md)

</details>

<details>
<summary><b>10 · Backtracking</b> — 16/16 ▓▓▓▓▓▓▓▓ ✅</summary>

Choose → explore → un-choose over partial solutions.

[📖 Lesson](materials/learning/10-backtracking.md)

- [x] **78** · Med · Subsets · [LeetCode](https://leetcode.com/problems/subsets/) · [Solution](problems/0001-0499/78.py) · [Walkthrough](materials/walkthroughs/78-subsets.md)
- [x] **90** · Med · Subsets II · [LeetCode](https://leetcode.com/problems/subsets-ii/) · [Solution](problems/0001-0499/90.py) · [Walkthrough](materials/walkthroughs/90-subsets-ii.md)
- [x] **39** · Med · Combination Sum · [LeetCode](https://leetcode.com/problems/combination-sum/) · [Solution](problems/0001-0499/39.py) · [Walkthrough](materials/walkthroughs/39-combination-sum.md)
- [x] **40** · Med · Combination Sum II · [LeetCode](https://leetcode.com/problems/combination-sum-ii/) · [Solution](problems/0001-0499/40.py) · [Walkthrough](materials/walkthroughs/40-combination-sum-ii.md)
- [x] **216** · Med · Combination Sum III · [LeetCode](https://leetcode.com/problems/combination-sum-iii/) · [Solution](problems/0001-0499/216.py) · [Walkthrough](materials/walkthroughs/216-combination-sum-iii.md)
- [x] **46** · Med · Permutations · [LeetCode](https://leetcode.com/problems/permutations/) · [Solution](problems/0001-0499/46.py) · [Walkthrough](materials/walkthroughs/46-permutations.md)
- [x] **47** · Med · Permutations II · [LeetCode](https://leetcode.com/problems/permutations-ii/) · [Solution](problems/0001-0499/47.py) · [Walkthrough](materials/walkthroughs/47-permutations-ii.md)
- [x] **77** · Med · Combinations · [LeetCode](https://leetcode.com/problems/combinations/) · [Solution](problems/0001-0499/77.py) · [Walkthrough](materials/walkthroughs/77-combinations.md)
- [x] **17** · Med · Letter Combinations of a Phone Number · [LeetCode](https://leetcode.com/problems/letter-combinations-of-a-phone-number/) · [Solution](problems/0001-0499/17.py) · [Walkthrough](materials/walkthroughs/17-letter-combinations-of-a-phone-number.md)
- [x] **79** · Med · Word Search · [LeetCode](https://leetcode.com/problems/word-search/) · [Solution](problems/0001-0499/79.py) · [Walkthrough](materials/walkthroughs/79-word-search.md)
- [x] **131** · Med · Palindrome Partitioning · [LeetCode](https://leetcode.com/problems/palindrome-partitioning/) · [Solution](problems/0001-0499/131.py) · [Walkthrough](materials/walkthroughs/131-palindrome-partitioning.md)
- [x] **93** · Med · Restore IP Addresses · [LeetCode](https://leetcode.com/problems/restore-ip-addresses/) · [Solution](problems/0001-0499/93.py) · [Walkthrough](materials/walkthroughs/93-restore-ip-addresses.md)
- [x] **698** · Med · Partition to K Equal Sum Subsets · [LeetCode](https://leetcode.com/problems/partition-to-k-equal-sum-subsets/) · [Solution](problems/0500-0999/698.py) · [Walkthrough](materials/walkthroughs/698-partition-to-k-equal-sum-subsets.md)
- [x] **526** · Med · Beautiful Arrangement · [LeetCode](https://leetcode.com/problems/beautiful-arrangement/) · [Solution](problems/0500-0999/526.py) · [Walkthrough](materials/walkthroughs/526-beautiful-arrangement.md)
- [x] **51** · Hard · N-Queens · [LeetCode](https://leetcode.com/problems/n-queens/) · [Solution](problems/0001-0499/51.py) · [Walkthrough](materials/walkthroughs/51-n-queens.md)
- [x] **52** · Hard · N-Queens II · [LeetCode](https://leetcode.com/problems/n-queens-ii/) · [Solution](problems/0001-0499/52.py) · [Walkthrough](materials/walkthroughs/52-n-queens-ii.md)

</details>

<details>
<summary><b>11 · Graphs</b> — 23/23 ▓▓▓▓▓▓▓▓ ✅</summary>

BFS for shortest unweighted paths, DFS for connectivity.

[📖 Lesson](materials/learning/11-graphs.md) · [📖 Grids primer](materials/learning/10b-grids-primer.md) · [📖 Union-Find](materials/learning/12-union-find.md)

- [x] **733** · Easy · Flood Fill · [LeetCode](https://leetcode.com/problems/flood-fill/) · [Solution](problems/0500-0999/733.py) · [Walkthrough](materials/walkthroughs/733-flood-fill.md)
- [x] **463** · Easy · Island Perimeter · [LeetCode](https://leetcode.com/problems/island-perimeter/) · [Solution](problems/0001-0499/463.py) · [Walkthrough](materials/walkthroughs/463-island-perimeter.md)
- [x] **1971** · Easy · Find if Path Exists in Graph · [LeetCode](https://leetcode.com/problems/find-if-path-exists-in-graph/) · [Solution](problems/1500-1999/1971.py) · [Walkthrough](materials/walkthroughs/1971-find-if-path-exists-in-graph.md)
- [x] **200** · Med · Number of Islands · [LeetCode](https://leetcode.com/problems/number-of-islands/) · [Solution](problems/0001-0499/200.py) · [Walkthrough](materials/walkthroughs/200-number-of-islands.md)
- [x] **695** · Med · Max Area of Island · [LeetCode](https://leetcode.com/problems/max-area-of-island/) · [Solution](problems/0500-0999/695.py) · [Walkthrough](materials/walkthroughs/695-max-area-of-island.md)
- [x] **133** · Med · Clone Graph · [LeetCode](https://leetcode.com/problems/clone-graph/) · [Solution](problems/0001-0499/133.py) · [Walkthrough](materials/walkthroughs/133-clone-graph.md)
- [x] **994** · Med · Rotting Oranges · [LeetCode](https://leetcode.com/problems/rotting-oranges/) · [Solution](problems/0500-0999/994.py) · [Walkthrough](materials/walkthroughs/994-rotting-oranges.md)
- [x] **286** · Med · Walls and Gates · [LeetCode](https://leetcode.com/problems/walls-and-gates/) · [Solution](problems/0001-0499/286.py) · [Walkthrough](materials/walkthroughs/286-walls-and-gates.md)
- [x] **417** · Med · Pacific Atlantic Water Flow · [LeetCode](https://leetcode.com/problems/pacific-atlantic-water-flow/) · [Solution](problems/0001-0499/417.py) · [Walkthrough](materials/walkthroughs/417-pacific-atlantic-water-flow.md)
- [x] **130** · Med · Surrounded Regions · [LeetCode](https://leetcode.com/problems/surrounded-regions/) · [Solution](problems/0001-0499/130.py) · [Walkthrough](materials/walkthroughs/130-surrounded-regions.md)
- [x] **207** · Med · Course Schedule · [LeetCode](https://leetcode.com/problems/course-schedule/) · [Solution](problems/0001-0499/207.py) · [Walkthrough](materials/walkthroughs/207-course-schedule.md)
- [x] **210** · Med · Course Schedule II · [LeetCode](https://leetcode.com/problems/course-schedule-ii/) · [Solution](problems/0001-0499/210.py) · [Walkthrough](materials/walkthroughs/210-course-schedule-ii.md)
- [x] **261** · Med · Graph Valid Tree · [LeetCode](https://leetcode.com/problems/graph-valid-tree/) · [Solution](problems/0001-0499/261.py) · [Walkthrough](materials/walkthroughs/261-graph-valid-tree.md)
- [x] **323** · Med · Number of Connected Components in an Undirected Graph · [LeetCode](https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/) · [Solution](problems/0001-0499/323.py) · [Walkthrough](materials/walkthroughs/323-number-of-connected-components-in-an-undirected-graph.md)
- [x] **684** · Med · Redundant Connection · [LeetCode](https://leetcode.com/problems/redundant-connection/) · [Solution](problems/0500-0999/684.py) · [Walkthrough](materials/walkthroughs/684-redundant-connection.md)
- [x] **547** · Med · Number of Provinces · [LeetCode](https://leetcode.com/problems/number-of-provinces/) · [Solution](problems/0500-0999/547.py) · [Walkthrough](materials/walkthroughs/547-number-of-provinces.md)
- [x] **785** · Med · Is Graph Bipartite? · [LeetCode](https://leetcode.com/problems/is-graph-bipartite/) · [Solution](problems/0500-0999/785.py) · [Walkthrough](materials/walkthroughs/785-is-graph-bipartite.md)
- [x] **802** · Med · Find Eventual Safe States · [LeetCode](https://leetcode.com/problems/find-eventual-safe-states/) · [Solution](problems/0500-0999/802.py) · [Walkthrough](materials/walkthroughs/802-find-eventual-safe-states.md)
- [x] **1466** · Med · Reorder Routes to Make All Paths Lead to the City Zero · [LeetCode](https://leetcode.com/problems/reorder-routes-to-make-all-paths-lead-to-the-city-zero/) · [Solution](problems/1000-1499/1466.py) · [Walkthrough](materials/walkthroughs/1466-reorder-routes-to-make-all-paths-lead-to-the-city-zero.md)
- [x] **841** · Med · Keys and Rooms · [LeetCode](https://leetcode.com/problems/keys-and-rooms/) · [Solution](problems/0500-0999/841.py) · [Walkthrough](materials/walkthroughs/841-keys-and-rooms.md)
- [x] **1020** · Med · Number of Enclaves · [LeetCode](https://leetcode.com/problems/number-of-enclaves/) · [Solution](problems/1000-1499/1020.py) · [Walkthrough](materials/walkthroughs/1020-number-of-enclaves.md)
- [x] **127** · Hard · Word Ladder · [LeetCode](https://leetcode.com/problems/word-ladder/) · [Solution](problems/0001-0499/127.py) · [Walkthrough](materials/walkthroughs/127-word-ladder.md)
- [x] **269** · Hard · Alien Dictionary · [LeetCode](https://leetcode.com/problems/alien-dictionary/) · [Solution](problems/0001-0499/269.py) · [Walkthrough](materials/walkthroughs/269-alien-dictionary.md)

</details>

<details>
<summary><b>12 · Advanced Graphs</b> — 11/11 ▓▓▓▓▓▓▓▓ ✅</summary>

Weighted shortest paths (Dijkstra), ordering (topo sort).

[📖 Lesson](materials/learning/13-advanced-graphs.md)

- [x] **743** · Med · Network Delay Time · [LeetCode](https://leetcode.com/problems/network-delay-time/) · [Solution](problems/0500-0999/743.py) · [Walkthrough](materials/walkthroughs/743-network-delay-time.md)
- [x] **1584** · Med · Min Cost to Connect All Points · [LeetCode](https://leetcode.com/problems/min-cost-to-connect-all-points/) · [Solution](problems/1500-1999/1584.py) · [Walkthrough](materials/walkthroughs/1584-min-cost-to-connect-all-points.md)
- [x] **787** · Med · Cheapest Flights Within K Stops · [LeetCode](https://leetcode.com/problems/cheapest-flights-within-k-stops/) · [Solution](problems/0500-0999/787.py) · [Walkthrough](materials/walkthroughs/787-cheapest-flights-within-k-stops.md)
- [x] **1631** · Med · Path With Minimum Effort · [LeetCode](https://leetcode.com/problems/path-with-minimum-effort/) · [Solution](problems/1500-1999/1631.py) · [Walkthrough](materials/walkthroughs/1631-path-with-minimum-effort.md)
- [x] **1976** · Med · Number of Ways to Arrive at Destination · [LeetCode](https://leetcode.com/problems/number-of-ways-to-arrive-at-destination/) · [Solution](problems/1500-1999/1976.py) · [Walkthrough](materials/walkthroughs/1976-number-of-ways-to-arrive-at-destination.md)
- [x] **2492** · Med · Minimum Score of a Path Between Two Cities · [LeetCode](https://leetcode.com/problems/minimum-score-of-a-path-between-two-cities/) · [Solution](problems/2000-2499/2492.py) · [Walkthrough](materials/walkthroughs/2492-minimum-score-of-a-path-between-two-cities.md)
- [x] **1462** · Med · Course Schedule IV · [LeetCode](https://leetcode.com/problems/course-schedule-iv/) · [Solution](problems/1000-1499/1462.py) · [Walkthrough](materials/walkthroughs/1462-course-schedule-iv.md)
- [x] **332** · Hard · Reconstruct Itinerary · [LeetCode](https://leetcode.com/problems/reconstruct-itinerary/) · [Solution](problems/0001-0499/332.py) · [Walkthrough](materials/walkthroughs/332-reconstruct-itinerary.md)
- [x] **778** · Hard · Swim in Rising Water · [LeetCode](https://leetcode.com/problems/swim-in-rising-water/) · [Solution](problems/0500-0999/778.py) · [Walkthrough](materials/walkthroughs/778-swim-in-rising-water.md)
- [x] **685** · Hard · Redundant Connection II · [LeetCode](https://leetcode.com/problems/redundant-connection-ii/) · [Solution](problems/0500-0999/685.py) · [Walkthrough](materials/walkthroughs/685-redundant-connection-ii.md)
- [x] **847** · Hard · Shortest Path Visiting All Nodes · [LeetCode](https://leetcode.com/problems/shortest-path-visiting-all-nodes/) · [Solution](problems/0500-0999/847.py) · [Walkthrough](materials/walkthroughs/847-shortest-path-visiting-all-nodes.md)

</details>

<details>
<summary><b>13 · 1-D Dynamic Programming</b> — 22/22 ▓▓▓▓▓▓▓▓ ✅</summary>

State + transition + base case over one axis.

[📖 Lesson](materials/learning/14-dp-1d.md)

- [x] **70** · Easy · Climbing Stairs · [LeetCode](https://leetcode.com/problems/climbing-stairs/) · [Solution](problems/0001-0499/70.py) · [Walkthrough](materials/walkthroughs/70-climbing-stairs.md)
- [x] **746** · Easy · Min Cost Climbing Stairs · [LeetCode](https://leetcode.com/problems/min-cost-climbing-stairs/) · [Solution](problems/0500-0999/746.py) · [Walkthrough](materials/walkthroughs/746-min-cost-climbing-stairs.md)
- [x] **1137** · Easy · N-th Tribonacci Number · [LeetCode](https://leetcode.com/problems/n-th-tribonacci-number/) · [Solution](problems/1000-1499/1137.py) · [Walkthrough](materials/walkthroughs/1137-n-th-tribonacci-number.md)
- [x] **198** · Med · House Robber · [LeetCode](https://leetcode.com/problems/house-robber/) · [Solution](problems/0001-0499/198.py) · [Walkthrough](materials/walkthroughs/198-house-robber.md)
- [x] **213** · Med · House Robber II · [LeetCode](https://leetcode.com/problems/house-robber-ii/) · [Solution](problems/0001-0499/213.py) · [Walkthrough](materials/walkthroughs/213-house-robber-ii.md)
- [x] **5** · Med · Longest Palindromic Substring · [LeetCode](https://leetcode.com/problems/longest-palindromic-substring/) · [Solution](problems/0001-0499/5.py) · [Walkthrough](materials/walkthroughs/5-longest-palindromic-substring.md)
- [x] **647** · Med · Palindromic Substrings · [LeetCode](https://leetcode.com/problems/palindromic-substrings/) · [Solution](problems/0500-0999/647.py) · [Walkthrough](materials/walkthroughs/647-palindromic-substrings.md)
- [x] **91** · Med · Decode Ways · [LeetCode](https://leetcode.com/problems/decode-ways/) · [Solution](problems/0001-0499/91.py) · [Walkthrough](materials/walkthroughs/91-decode-ways.md)
- [x] **322** · Med · Coin Change · [LeetCode](https://leetcode.com/problems/coin-change/) · [Solution](problems/0001-0499/322.py) · [Walkthrough](materials/walkthroughs/322-coin-change.md)
- [x] **518** · Med · Coin Change II · [LeetCode](https://leetcode.com/problems/coin-change-ii/) · [Solution](problems/0500-0999/518.py) · [Walkthrough](materials/walkthroughs/518-coin-change-ii.md)
- [x] **152** · Med · Maximum Product Subarray · [LeetCode](https://leetcode.com/problems/maximum-product-subarray/) · [Solution](problems/0001-0499/152.py) · [Walkthrough](materials/walkthroughs/152-maximum-product-subarray.md)
- [x] **139** · Med · Word Break · [LeetCode](https://leetcode.com/problems/word-break/) · [Solution](problems/0001-0499/139.py) · [Walkthrough](materials/walkthroughs/139-word-break.md)
- [x] **300** · Med · Longest Increasing Subsequence · [LeetCode](https://leetcode.com/problems/longest-increasing-subsequence/) · [Solution](problems/0001-0499/300.py) · [Walkthrough](materials/walkthroughs/300-longest-increasing-subsequence.md)
- [x] **377** · Med · Combination Sum IV · [LeetCode](https://leetcode.com/problems/combination-sum-iv/) · [Solution](problems/0001-0499/377.py) · [Walkthrough](materials/walkthroughs/377-combination-sum-iv.md)
- [x] **416** · Med · Partition Equal Subset Sum · [LeetCode](https://leetcode.com/problems/partition-equal-subset-sum/) · [Solution](problems/0001-0499/416.py) · [Walkthrough](materials/walkthroughs/416-partition-equal-subset-sum.md)
- [x] **740** · Med · Delete and Earn · [LeetCode](https://leetcode.com/problems/delete-and-earn/) · [Solution](problems/0500-0999/740.py) · [Walkthrough](materials/walkthroughs/740-delete-and-earn.md)
- [x] **279** · Med · Perfect Squares · [LeetCode](https://leetcode.com/problems/perfect-squares/) · [Solution](problems/0001-0499/279.py) · [Walkthrough](materials/walkthroughs/279-perfect-squares.md)
- [x] **343** · Med · Integer Break · [LeetCode](https://leetcode.com/problems/integer-break/) · [Solution](problems/0001-0499/343.py) · [Walkthrough](materials/walkthroughs/343-integer-break.md)
- [x] **309** · Med · Best Time to Buy and Sell Stock with Cooldown · [LeetCode](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/) · [Solution](problems/0001-0499/309.py) · [Walkthrough](materials/walkthroughs/309-best-time-to-buy-and-sell-stock-with-cooldown.md)
- [x] **96** · Med · Unique Binary Search Trees · [LeetCode](https://leetcode.com/problems/unique-binary-search-trees/) · [Solution](problems/0001-0499/96.py) · [Walkthrough](materials/walkthroughs/96-unique-binary-search-trees.md)
- [x] **1027** · Med · Longest Arithmetic Subsequence · [LeetCode](https://leetcode.com/problems/longest-arithmetic-subsequence/) · [Solution](problems/1000-1499/1027.py) · [Walkthrough](materials/walkthroughs/1027-longest-arithmetic-subsequence.md)
- [x] **132** · Hard · Palindrome Partitioning II · [LeetCode](https://leetcode.com/problems/palindrome-partitioning-ii/) · [Solution](problems/0001-0499/132.py) · [Walkthrough](materials/walkthroughs/132-palindrome-partitioning-ii.md)

</details>

<details>
<summary><b>14 · 2-D Dynamic Programming</b> — 9/21 ▓▓▓░░░░░</summary>

Same engine, two indices: grids and sequence pairs.

[📖 Lesson](materials/learning/15-dp-2d.md)

- [x] **62** · Med · Unique Paths · [LeetCode](https://leetcode.com/problems/unique-paths/) · [Solution](problems/0001-0499/62.py) · [Walkthrough](materials/walkthroughs/62-unique-paths.md)
- [ ] **63** · Med · Unique Paths II · [LeetCode](https://leetcode.com/problems/unique-paths-ii/)
- [ ] **64** · Med · Minimum Path Sum · [LeetCode](https://leetcode.com/problems/minimum-path-sum/)
- [ ] **120** · Med · Triangle · [LeetCode](https://leetcode.com/problems/triangle/)
- [ ] **931** · Med · Minimum Falling Path Sum · [LeetCode](https://leetcode.com/problems/minimum-falling-path-sum/)
- [ ] **221** · Med · Maximal Square · [LeetCode](https://leetcode.com/problems/maximal-square/)
- [x] **1143** · Med · Longest Common Subsequence · [LeetCode](https://leetcode.com/problems/longest-common-subsequence/) · [Solution](problems/1000-1499/1143.py) · [Walkthrough](materials/walkthroughs/1143-longest-common-subsequence.md)
- [ ] **1035** · Med · Uncrossed Lines · [LeetCode](https://leetcode.com/problems/uncrossed-lines/)
- [ ] **516** · Med · Longest Palindromic Subsequence · [LeetCode](https://leetcode.com/problems/longest-palindromic-subsequence/)
- [x] **494** · Med · Target Sum · [LeetCode](https://leetcode.com/problems/target-sum/) · [Solution](problems/0001-0499/494.py) · [Walkthrough](materials/walkthroughs/494-target-sum.md)
- [ ] **1049** · Med · Last Stone Weight II · [LeetCode](https://leetcode.com/problems/last-stone-weight-ii/)
- [x] **72** · Med · Edit Distance · [LeetCode](https://leetcode.com/problems/edit-distance/) · [Solution](problems/0001-0499/72.py) · [Walkthrough](materials/walkthroughs/72-edit-distance.md)
- [x] **97** · Med · Interleaving String · [LeetCode](https://leetcode.com/problems/interleaving-string/) · [Solution](problems/0001-0499/97.py) · [Walkthrough](materials/walkthroughs/97-interleaving-string.md)
- [ ] **718** · Med · Maximum Length of Repeated Subarray · [LeetCode](https://leetcode.com/problems/maximum-length-of-repeated-subarray/)
- [x] **115** · Hard · Distinct Subsequences · [LeetCode](https://leetcode.com/problems/distinct-subsequences/) · [Solution](problems/0001-0499/115.py) · [Walkthrough](materials/walkthroughs/115-distinct-subsequences.md)
- [x] **312** · Hard · Burst Balloons · [LeetCode](https://leetcode.com/problems/burst-balloons/) · [Solution](problems/0001-0499/312.py) · [Walkthrough](materials/walkthroughs/312-burst-balloons.md)
- [x] **10** · Hard · Regular Expression Matching · [LeetCode](https://leetcode.com/problems/regular-expression-matching/) · [Solution](problems/0001-0499/10.py) · [Walkthrough](materials/walkthroughs/10-regular-expression-matching.md)
- [x] **329** · Hard · Longest Increasing Path in a Matrix · [LeetCode](https://leetcode.com/problems/longest-increasing-path-in-a-matrix/) · [Solution](problems/0001-0499/329.py) · [Walkthrough](materials/walkthroughs/329-longest-increasing-path-in-a-matrix.md)
- [ ] **174** · Hard · Dungeon Game · [LeetCode](https://leetcode.com/problems/dungeon-game/)
- [ ] **123** · Hard · Best Time to Buy and Sell Stock III · [LeetCode](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iii/)
- [ ] **188** · Hard · Best Time to Buy and Sell Stock IV · [LeetCode](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/)

</details>

<details>
<summary><b>15 · Greedy</b> — 8/14 ▓▓▓▓▓░░░</summary>

Take the locally best choice; the proof is the hard part.

[📖 Lesson](materials/learning/16-greedy.md)

- [ ] **561** · Easy · Array Partition · [LeetCode](https://leetcode.com/problems/array-partition/)
- [ ] **1005** · Easy · Maximize Sum Of Array After K Negations · [LeetCode](https://leetcode.com/problems/maximize-sum-of-array-after-k-negations/)
- [x] **53** · Med · Maximum Subarray · [LeetCode](https://leetcode.com/problems/maximum-subarray/) · [Solution](problems/0001-0499/53.py) · [Walkthrough](materials/walkthroughs/53-maximum-subarray.md)
- [x] **55** · Med · Jump Game · [LeetCode](https://leetcode.com/problems/jump-game/) · [Solution](problems/0001-0499/55.py) · [Walkthrough](materials/walkthroughs/55-jump-game.md)
- [x] **45** · Med · Jump Game II · [LeetCode](https://leetcode.com/problems/jump-game-ii/) · [Solution](problems/0001-0499/45.py) · [Walkthrough](materials/walkthroughs/45-jump-game-ii.md)
- [ ] **122** · Med · Best Time to Buy and Sell Stock II · [LeetCode](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/) · [Solution](problems/0001-0499/122.py)
- [x] **134** · Med · Gas Station · [LeetCode](https://leetcode.com/problems/gas-station/) · [Solution](problems/0001-0499/134.py) · [Walkthrough](materials/walkthroughs/134-gas-station.md)
- [x] **846** · Med · Hand of Straights · [LeetCode](https://leetcode.com/problems/hand-of-straights/) · [Solution](problems/0500-0999/846.py) · [Walkthrough](materials/walkthroughs/846-hand-of-straights.md)
- [x] **1899** · Med · Merge Triplets to Form Target Triplet · [LeetCode](https://leetcode.com/problems/merge-triplets-to-form-target-triplet/) · [Solution](problems/1500-1999/1899.py) · [Walkthrough](materials/walkthroughs/1899-merge-triplets-to-form-target-triplet.md)
- [x] **763** · Med · Partition Labels · [LeetCode](https://leetcode.com/problems/partition-labels/) · [Solution](problems/0500-0999/763.py) · [Walkthrough](materials/walkthroughs/763-partition-labels.md)
- [x] **678** · Med · Valid Parenthesis String · [LeetCode](https://leetcode.com/problems/valid-parenthesis-string/) · [Solution](problems/0500-0999/678.py) · [Walkthrough](materials/walkthroughs/678-valid-parenthesis-string.md)
- [ ] **1647** · Med · Minimum Deletions to Make Character Frequencies Unique · [LeetCode](https://leetcode.com/problems/minimum-deletions-to-make-character-frequencies-unique/)
- [ ] **738** · Med · Monotone Increasing Digits · [LeetCode](https://leetcode.com/problems/monotone-increasing-digits/)
- [ ] **376** · Med · Wiggle Subsequence · [LeetCode](https://leetcode.com/problems/wiggle-subsequence/)

</details>

<details>
<summary><b>16 · Intervals</b> — 6/10 ▓▓▓▓▓░░░</summary>

Sort first, then one linear sweep to merge / count.

[📖 Lesson](materials/learning/17-intervals.md)

- [x] **252** · Easy · Meeting Rooms · [LeetCode](https://leetcode.com/problems/meeting-rooms/) · [Solution](problems/0001-0499/252.py) · [Walkthrough](materials/walkthroughs/252-meeting-rooms.md)
- [x] **56** · Med · Merge Intervals · [LeetCode](https://leetcode.com/problems/merge-intervals/) · [Solution](problems/0001-0499/56.py) · [Walkthrough](materials/walkthroughs/56-merge-intervals.md)
- [x] **57** · Med · Insert Interval · [LeetCode](https://leetcode.com/problems/insert-interval/) · [Solution](problems/0001-0499/57.py) · [Walkthrough](materials/walkthroughs/57-insert-interval.md)
- [x] **435** · Med · Non-overlapping Intervals · [LeetCode](https://leetcode.com/problems/non-overlapping-intervals/) · [Solution](problems/0001-0499/435.py) · [Walkthrough](materials/walkthroughs/435-non-overlapping-intervals.md)
- [x] **253** · Med · Meeting Rooms II · [LeetCode](https://leetcode.com/problems/meeting-rooms-ii/) · [Solution](problems/0001-0499/253.py) · [Walkthrough](materials/walkthroughs/253-meeting-rooms-ii.md)
- [ ] **986** · Med · Interval List Intersections · [LeetCode](https://leetcode.com/problems/interval-list-intersections/)
- [ ] **1288** · Med · Remove Covered Intervals · [LeetCode](https://leetcode.com/problems/remove-covered-intervals/)
- [ ] **452** · Med · Minimum Number of Arrows to Burst Balloons · [LeetCode](https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/)
- [ ] **731** · Med · My Calendar II · [LeetCode](https://leetcode.com/problems/my-calendar-ii/)
- [x] **1851** · Hard · Minimum Interval to Include Each Query · [LeetCode](https://leetcode.com/problems/minimum-interval-to-include-each-query/) · [Solution](problems/1500-1999/1851.py) · [Walkthrough](materials/walkthroughs/1851-minimum-interval-to-include-each-query.md)

</details>

<details>
<summary><b>17 · Math & Geometry</b> — 8/16 ▓▓▓▓░░░░</summary>

GCD, fast power, in-place matrix transforms.

[📖 Lesson](materials/learning/19-math-geometry.md)

- [ ] **9** · Easy · Palindrome Number · [LeetCode](https://leetcode.com/problems/palindrome-number/) · [Solution](problems/0001-0499/9.py)
- [ ] **13** · Easy · Roman to Integer · [LeetCode](https://leetcode.com/problems/roman-to-integer/) · [Solution](problems/0001-0499/13.py)
- [x] **202** · Easy · Happy Number · [LeetCode](https://leetcode.com/problems/happy-number/) · [Solution](problems/0001-0499/202.py) · [Walkthrough](materials/walkthroughs/202-happy-number.md)
- [ ] **263** · Easy · Ugly Number · [LeetCode](https://leetcode.com/problems/ugly-number/)
- [ ] **1071** · Easy · Greatest Common Divisor of Strings · [LeetCode](https://leetcode.com/problems/greatest-common-divisor-of-strings/) · [Solution](problems/1000-1499/1071.py)
- [ ] **415** · Easy · Add Strings · [LeetCode](https://leetcode.com/problems/add-strings/) · [Solution](problems/0001-0499/415.py)
- [ ] **168** · Easy · Excel Sheet Column Title · [LeetCode](https://leetcode.com/problems/excel-sheet-column-title/) · [Solution](problems/0001-0499/168.py)
- [x] **7** · Med · Reverse Integer · [LeetCode](https://leetcode.com/problems/reverse-integer/) · [Solution](problems/0001-0499/7.py) · [Walkthrough](materials/walkthroughs/7-reverse-integer.md)
- [ ] **12** · Med · Integer to Roman · [LeetCode](https://leetcode.com/problems/integer-to-roman/)
- [x] **50** · Med · Pow(x, n) · [LeetCode](https://leetcode.com/problems/powx-n/) · [Solution](problems/0001-0499/50.py) · [Walkthrough](materials/walkthroughs/50-pow-x-n.md)
- [x] **43** · Med · Multiply Strings · [LeetCode](https://leetcode.com/problems/multiply-strings/) · [Solution](problems/0001-0499/43.py) · [Walkthrough](materials/walkthroughs/43-multiply-strings.md)
- [x] **73** · Med · Set Matrix Zeroes · [LeetCode](https://leetcode.com/problems/set-matrix-zeroes/) · [Solution](problems/0001-0499/73.py) · [Walkthrough](materials/walkthroughs/73-set-matrix-zeroes.md)
- [x] **54** · Med · Spiral Matrix · [LeetCode](https://leetcode.com/problems/spiral-matrix/) · [Solution](problems/0001-0499/54.py) · [Walkthrough](materials/walkthroughs/54-spiral-matrix.md)
- [x] **48** · Med · Rotate Image · [LeetCode](https://leetcode.com/problems/rotate-image/) · [Solution](problems/0001-0499/48.py) · [Walkthrough](materials/walkthroughs/48-rotate-image.md)
- [x] **2013** · Med · Detect Squares · [LeetCode](https://leetcode.com/problems/detect-squares/) · [Solution](problems/2000-2499/2013.py) · [Walkthrough](materials/walkthroughs/2013-detect-squares.md)
- [ ] **149** · Hard · Max Points on a Line · [LeetCode](https://leetcode.com/problems/max-points-on-a-line/)

</details>

<details>
<summary><b>18 · Bit Manipulation</b> — 5/13 ▓▓▓░░░░░</summary>

Masks, shifts, and XOR cancellation in O(1).

[📖 Lesson](materials/learning/18-bit-manipulation.md)

- [x] **136** · Easy · Single Number · [LeetCode](https://leetcode.com/problems/single-number/) · [Solution](problems/0001-0499/136.py) · [Walkthrough](materials/walkthroughs/136-single-number.md)
- [x] **191** · Easy · Number of 1 Bits · [LeetCode](https://leetcode.com/problems/number-of-1-bits/) · [Solution](problems/0001-0499/191.py) · [Walkthrough](materials/walkthroughs/191-number-of-1-bits.md)
- [x] **338** · Easy · Counting Bits · [LeetCode](https://leetcode.com/problems/counting-bits/) · [Solution](problems/0001-0499/338.py) · [Walkthrough](materials/walkthroughs/338-counting-bits.md)
- [x] **190** · Easy · Reverse Bits · [LeetCode](https://leetcode.com/problems/reverse-bits/) · [Solution](problems/0001-0499/190.py) · [Walkthrough](materials/walkthroughs/190-reverse-bits.md)
- [ ] **67** · Easy · Add Binary · [LeetCode](https://leetcode.com/problems/add-binary/) · [Solution](problems/0001-0499/67.py)
- [ ] **461** · Easy · Hamming Distance · [LeetCode](https://leetcode.com/problems/hamming-distance/) · [Solution](problems/0001-0499/461.py)
- [x] **371** · Med · Sum of Two Integers · [LeetCode](https://leetcode.com/problems/sum-of-two-integers/) · [Solution](problems/0001-0499/371.py) · [Walkthrough](materials/walkthroughs/371-sum-of-two-integers.md)
- [ ] **137** · Med · Single Number II · [LeetCode](https://leetcode.com/problems/single-number-ii/)
- [ ] **260** · Med · Single Number III · [LeetCode](https://leetcode.com/problems/single-number-iii/)
- [ ] **201** · Med · Bitwise AND of Numbers Range · [LeetCode](https://leetcode.com/problems/bitwise-and-of-numbers-range/)
- [ ] **318** · Med · Maximum Product of Word Lengths · [LeetCode](https://leetcode.com/problems/maximum-product-of-word-lengths/)
- [ ] **1318** · Med · Minimum Flips to Make a OR b Equal to c · [LeetCode](https://leetcode.com/problems/minimum-flips-to-make-a-or-b-equal-to-c/)
- [ ] **89** · Med · Gray Code · [LeetCode](https://leetcode.com/problems/gray-code/)

</details>

---

## Materials

| Hub | What's inside |
|-----|---------------|
| [🎯 Interview Roadmap](interview.md) | Behavioral, the interview loop, and system design — paced against these units |
| [Guides](materials/guides/_index.md) | Installing Python, editor/terminal/git setup, using LeetCode, debugging, study strategy |
| [Data Structures](materials/data-structures/_index.md) | One-structure-per-file reference pages (array → segment tree) |
| [Algorithms](materials/algorithms/_index.md) | One-algorithm-per-file reference pages (binary search → Dijkstra) |
| [Python Syntax Cookbook](materials/syntax/_index.md) | Every construct the solutions lean on |
| [Code Templates](materials/appendix/templates/README.md) | Per-pattern `template.py` skeletons to memorize |
| [Segment Trees](materials/learning/20-segment-trees.md) | Optional — beyond the NeetCode 150 |

**Other lists:** [Rushed 40](lists/rushed40.md) (fast pass) · [Blind 75](lists/neetcodeblind75.md) · [NeetCode 150](lists/neetcode150.md) · [NeetCode 250](lists/neetcode250.md) · [Recommended 300](lists/recommended.md) (this page)
