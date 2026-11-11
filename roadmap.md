```
 /$$$$$$$                            /$$
| $$__  $$                          | $$
| $$  \ $$  /$$$$$$   /$$$$$$   /$$$$$$$ /$$$$$$/$$$$   /$$$$$$   /$$$$$$
| $$$$$$$/ /$$__  $$ |____  $$ /$$__  $$| $$_  $$_  $$ |____  $$ /$$__  $$
| $$__  $$| $$  \ $$  /$$$$$$$| $$  | $$| $$ \ $$ \ $$  /$$$$$$$| $$  \ $$
| $$  \ $$| $$  | $$ /$$__  $$| $$  | $$| $$ | $$ | $$ /$$__  $$| $$  | $$
| $$  | $$|  $$$$$$/|  $$$$$$$|  $$$$$$$| $$ | $$ | $$|  $$$$$$$| $$$$$$$/
|__/  |__/ \______/  \_______/ \_______/|__/ |__/ |__/ \_______/| $$____/
                                                                | $$
                                                                |__/
```

```
             ┌─ LeetCode link
 ┌─ Checkbox │                       ┌─ Walkthrough link
 ▼           ▼                       ▼
[ ] ▰▱▱▱ 1 Two Sum · Solution · Walkthrough
     ▲                   ▲
     └─ List             └─ Solution link

▰▱▱▱ Blind 75 · ▰▰▱▱ NeetCode 150 · ▰▰▰▱ NeetCode 250 · ▰▰▰▰ Extra 301
```

`░░░░░░░░░░░░░░░░░░░░░░░░` **0/301**

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
<summary><b>01 · Arrays & Hashing</b> — 0/24 ░░░░░░░░</summary>

Trade memory for O(1) lookups; kill brute-force double loops.

[📖 Lesson](materials/learning/01-arrays-hashing.md) · [📖 Prefix sums](materials/learning/01b-prefix-sums.md)

$\color{#2da44e}{\textbf{Easy}}$

- [ ] ▰▱▱▱ [**1** Two Sum](https://leetcode.com/problems/two-sum/) · [Solution](problems/0001-0499/1.py) · [Walkthrough](materials/walkthroughs/1-two-sum.md)
- [ ] ▰▱▱▱ [**217** Contains Duplicate](https://leetcode.com/problems/contains-duplicate/) · [Solution](problems/0001-0499/217.py) · [Walkthrough](materials/walkthroughs/217-contains-duplicate.md)
- [ ] ▰▱▱▱ [**242** Valid Anagram](https://leetcode.com/problems/valid-anagram/) · [Solution](problems/0001-0499/242.py) · [Walkthrough](materials/walkthroughs/242-valid-anagram.md)
- [ ] ▰▰▰▱ [**14** Longest Common Prefix](https://leetcode.com/problems/longest-common-prefix/) · [Solution](problems/0001-0499/14.py) · [Walkthrough](materials/walkthroughs/14-longest-common-prefix.md)
- [ ] ▰▰▰▱ [**169** Majority Element](https://leetcode.com/problems/majority-element/) · [Solution](problems/0001-0499/169.py) · [Walkthrough](materials/walkthroughs/169-majority-element.md)
- [ ] ▰▰▰▱ [**26** Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/) · [Solution](problems/0001-0499/26.py) · [Walkthrough](materials/walkthroughs/26-remove-duplicates-from-sorted-array.md)
- [ ] ▰▰▰▱ [**27** Remove Element](https://leetcode.com/problems/remove-element/) · [Solution](problems/0001-0499/27.py) · [Walkthrough](materials/walkthroughs/27-remove-element.md)
- [ ] ▰▰▱▱ [**66** Plus One](https://leetcode.com/problems/plus-one/) · [Solution](problems/0001-0499/66.py) · [Walkthrough](materials/walkthroughs/66-plus-one.md)
- [ ] ▰▰▰▱ [**88** Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/) · [Solution](problems/0001-0499/88.py) · [Walkthrough](materials/walkthroughs/88-merge-sorted-array.md)
- [ ] ▰▱▱▱ [**268** Missing Number](https://leetcode.com/problems/missing-number/) · [Solution](problems/0001-0499/268.py) · [Walkthrough](materials/walkthroughs/268-missing-number.md)
- [ ] ▰▰▰▰ [**448** Find All Numbers Disappeared in an Array](https://leetcode.com/problems/find-all-numbers-disappeared-in-an-array/) · [Solution](problems/0001-0499/448.py) · [Walkthrough](materials/walkthroughs/448-find-all-numbers-disappeared-in-an-array.md)
- [ ] ▰▰▰▱ [**1929** Concatenation of Array](https://leetcode.com/problems/concatenation-of-array/) · [Solution](problems/1500-1999/1929.py) · [Walkthrough](materials/walkthroughs/1929-concatenation-of-array.md)
- [ ] ▰▰▰▰ [**303** Range Sum Query - Immutable](https://leetcode.com/problems/range-sum-query-immutable/) · [Solution](problems/0001-0499/303.py) · [Walkthrough](materials/walkthroughs/303-range-sum-query-immutable.md)

$\color{#e67e22}{\textbf{Medium}}$

- [ ] ▰▱▱▱ [**49** Group Anagrams](https://leetcode.com/problems/group-anagrams/) · [Solution](problems/0001-0499/49.py) · [Walkthrough](materials/walkthroughs/49-group-anagrams.md)
- [ ] ▰▱▱▱ [**347** Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) · [Solution](problems/0001-0499/347.py) · [Walkthrough](materials/walkthroughs/347-top-k-frequent-elements.md)
- [ ] ▰▱▱▱ [**238** Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) · [Solution](problems/0001-0499/238.py) · [Walkthrough](materials/walkthroughs/238-product-of-array-except-self.md)
- [ ] ▰▱▱▱ [**271** Encode and Decode Strings](https://leetcode.com/problems/encode-and-decode-strings/) · [Solution](problems/0001-0499/271.py) · [Walkthrough](materials/walkthroughs/271-encode-and-decode-strings.md)
- [ ] ▰▰▱▱ [**36** Valid Sudoku](https://leetcode.com/problems/valid-sudoku/) · [Solution](problems/0001-0499/36.py) · [Walkthrough](materials/walkthroughs/36-valid-sudoku.md)
- [ ] ▰▰▰▰ [**380** Insert Delete GetRandom O(1)](https://leetcode.com/problems/insert-delete-getrandom-o1/) · [Solution](problems/0001-0499/380.py) · [Walkthrough](materials/walkthroughs/380-insert-delete-getrandom-o1.md)
- [ ] ▰▱▱▱ [**128** Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/) · [Solution](problems/0001-0499/128.py) · [Walkthrough](materials/walkthroughs/128-longest-consecutive-sequence.md)
- [ ] ▰▰▰▱ [**560** Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) · [Solution](problems/0500-0999/560.py) · [Walkthrough](materials/walkthroughs/560-subarray-sum-equals-k.md)
- [ ] ▰▰▰▰ [**525** Contiguous Array](https://leetcode.com/problems/contiguous-array/) · [Solution](problems/0500-0999/525.py) · [Walkthrough](materials/walkthroughs/525-contiguous-array.md)
- [ ] ▰▰▰▰ [**274** H-Index](https://leetcode.com/problems/h-index/) · [Solution](problems/0001-0499/274.py) · [Walkthrough](materials/walkthroughs/274-h-index.md)

$\color{#cf222e}{\textbf{Hard}}$

- [ ] ▰▰▰▱ [**41** First Missing Positive](https://leetcode.com/problems/first-missing-positive/) · [Solution](problems/0001-0499/41.py) · [Walkthrough](materials/walkthroughs/41-first-missing-positive.md)

</details>

<details>
<summary><b>02 · Two Pointers</b> — 0/14 ░░░░░░░░</summary>

Two cursors on a sorted array drop the O(n²).

[📖 Lesson](materials/learning/02-two-pointers.md)

$\color{#2da44e}{\textbf{Easy}}$

- [ ] ▰▱▱▱ [**125** Valid Palindrome](https://leetcode.com/problems/valid-palindrome/) · [Solution](problems/0001-0499/125.py) · [Walkthrough](materials/walkthroughs/125-valid-palindrome.md)
- [ ] ▰▰▰▱ [**680** Valid Palindrome II](https://leetcode.com/problems/valid-palindrome-ii/) · [Solution](problems/0500-0999/680.py) · [Walkthrough](materials/walkthroughs/680-valid-palindrome-ii.md)
- [ ] ▰▰▰▰ [**283** Move Zeroes](https://leetcode.com/problems/move-zeroes/) · [Solution](problems/0001-0499/283.py) · [Walkthrough](materials/walkthroughs/283-move-zeroes.md)
- [ ] ▰▰▰▰ [**977** Squares of a Sorted Array](https://leetcode.com/problems/squares-of-a-sorted-array/) · [Solution](problems/0500-0999/977.py) · [Walkthrough](materials/walkthroughs/977-squares-of-a-sorted-array.md)
- [ ] ▰▰▰▱ [**344** Reverse String](https://leetcode.com/problems/reverse-string/) · [Solution](problems/0001-0499/344.py) · [Walkthrough](materials/walkthroughs/344-reverse-string.md)
- [ ] ▰▰▰▰ [**392** Is Subsequence](https://leetcode.com/problems/is-subsequence/) · [Solution](problems/0001-0499/392.py) · [Walkthrough](materials/walkthroughs/392-is-subsequence.md)
- [ ] ▰▰▰▱ [**1768** Merge Strings Alternately](https://leetcode.com/problems/merge-strings-alternately/) · [Solution](problems/1500-1999/1768.py) · [Walkthrough](materials/walkthroughs/1768-merge-strings-alternately.md)

$\color{#e67e22}{\textbf{Medium}}$

- [ ] ▰▰▱▱ [**167** Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) · [Solution](problems/0001-0499/167.py) · [Walkthrough](materials/walkthroughs/167-two-sum-ii-input-array-is-sorted.md)
- [ ] ▰▱▱▱ [**15** 3Sum](https://leetcode.com/problems/3sum/) · [Solution](problems/0001-0499/15.py) · [Walkthrough](materials/walkthroughs/15-3sum.md)
- [ ] ▰▰▰▰ [**16** 3Sum Closest](https://leetcode.com/problems/3sum-closest/) · [Solution](problems/0001-0499/16.py) · [Walkthrough](materials/walkthroughs/16-3sum-closest.md)
- [ ] ▰▰▰▱ [**18** 4Sum](https://leetcode.com/problems/4sum/) · [Solution](problems/0001-0499/18.py) · [Walkthrough](materials/walkthroughs/18-4sum.md)
- [ ] ▰▱▱▱ [**11** Container With Most Water](https://leetcode.com/problems/container-with-most-water/) · [Solution](problems/0001-0499/11.py) · [Walkthrough](materials/walkthroughs/11-container-with-most-water.md)
- [ ] ▰▰▰▱ [**75** Sort Colors](https://leetcode.com/problems/sort-colors/) · [Solution](problems/0001-0499/75.py) · [Walkthrough](materials/walkthroughs/75-sort-colors.md)

$\color{#cf222e}{\textbf{Hard}}$

- [ ] ▰▰▱▱ [**42** Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) · [Solution](problems/0001-0499/42.py) · [Walkthrough](materials/walkthroughs/42-trapping-rain-water.md)

</details>

<details>
<summary><b>03 · Sliding Window</b> — 0/14 ░░░░░░░░</summary>

A moving boundary over contiguous ranges; O(n).

[📖 Lesson](materials/learning/03-sliding-window.md)

$\color{#2da44e}{\textbf{Easy}}$

- [ ] ▰▱▱▱ [**121** Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) · [Solution](problems/0001-0499/121.py) · [Walkthrough](materials/walkthroughs/121-best-time-to-buy-and-sell-stock.md)
- [ ] ▰▰▰▱ [**219** Contains Duplicate II](https://leetcode.com/problems/contains-duplicate-ii/) · [Solution](problems/0001-0499/219.py) · [Walkthrough](materials/walkthroughs/219-contains-duplicate-ii.md)
- [ ] ▰▰▰▰ [**643** Maximum Average Subarray I](https://leetcode.com/problems/maximum-average-subarray-i/) · [Solution](problems/0500-0999/643.py) · [Walkthrough](materials/walkthroughs/643-maximum-average-subarray-i.md)

$\color{#e67e22}{\textbf{Medium}}$

- [ ] ▰▱▱▱ [**3** Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) · [Solution](problems/0001-0499/3.py) · [Walkthrough](materials/walkthroughs/3-longest-substring-without-repeating-characters.md)
- [ ] ▰▱▱▱ [**424** Longest Repeating Character Replacement](https://leetcode.com/problems/longest-repeating-character-replacement/) · [Solution](problems/0001-0499/424.py) · [Walkthrough](materials/walkthroughs/424-longest-repeating-character-replacement.md)
- [ ] ▰▰▱▱ [**567** Permutation in String](https://leetcode.com/problems/permutation-in-string/) · [Solution](problems/0500-0999/567.py) · [Walkthrough](materials/walkthroughs/567-permutation-in-string.md)
- [ ] ▰▰▰▰ [**438** Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/) · [Solution](problems/0001-0499/438.py) · [Walkthrough](materials/walkthroughs/438-find-all-anagrams-in-a-string.md)
- [ ] ▰▰▰▱ [**209** Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/) · [Solution](problems/0001-0499/209.py) · [Walkthrough](materials/walkthroughs/209-minimum-size-subarray-sum.md)
- [ ] ▰▰▰▰ [**904** Fruit Into Baskets](https://leetcode.com/problems/fruit-into-baskets/) · [Solution](problems/0500-0999/904.py) · [Walkthrough](materials/walkthroughs/904-fruit-into-baskets.md)
- [ ] ▰▰▰▰ [**1456** Maximum Number of Vowels in a Substring of Given Length](https://leetcode.com/problems/maximum-number-of-vowels-in-a-substring-of-given-length/) · [Solution](problems/1000-1499/1456.py) · [Walkthrough](materials/walkthroughs/1456-maximum-number-of-vowels-in-a-substring-of-given-length.md)
- [ ] ▰▰▰▰ [**1004** Max Consecutive Ones III](https://leetcode.com/problems/max-consecutive-ones-iii/) · [Solution](problems/1000-1499/1004.py) · [Walkthrough](materials/walkthroughs/1004-max-consecutive-ones-iii.md)
- [ ] ▰▰▰▰ [**1493** Longest Subarray of 1's After Deleting One Element](https://leetcode.com/problems/longest-subarray-of-1s-after-deleting-one-element/) · [Solution](problems/1000-1499/1493.py) · [Walkthrough](materials/walkthroughs/1493-longest-subarray-of-1s-after-deleting-one-element.md)

$\color{#cf222e}{\textbf{Hard}}$

- [ ] ▰▱▱▱ [**76** Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/) · [Solution](problems/0001-0499/76.py) · [Walkthrough](materials/walkthroughs/76-minimum-window-substring.md)
- [ ] ▰▰▱▱ [**239** Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) · [Solution](problems/0001-0499/239.py) · [Walkthrough](materials/walkthroughs/239-sliding-window-maximum.md)

</details>

<details>
<summary><b>04 · Stack</b> — 0/16 ░░░░░░░░</summary>

LIFO/FIFO for order-sensitive work; monotonic stack for next-greater.

[📖 Lesson](materials/learning/04-stack.md) · [📖 Recursion](materials/learning/04b-recursion.md)

$\color{#2da44e}{\textbf{Easy}}$

- [ ] ▰▱▱▱ [**20** Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) · [Solution](problems/0001-0499/20.py) · [Walkthrough](materials/walkthroughs/20-valid-parentheses.md)
- [ ] ▰▰▰▱ [**682** Baseball Game](https://leetcode.com/problems/baseball-game/) · [Solution](problems/0500-0999/682.py) · [Walkthrough](materials/walkthroughs/682-baseball-game.md)
- [ ] ▰▰▰▰ [**496** Next Greater Element I](https://leetcode.com/problems/next-greater-element-i/) · [Solution](problems/0001-0499/496.py) · [Walkthrough](materials/walkthroughs/496-next-greater-element-i.md)
- [ ] ▰▰▰▱ [**225** Implement Stack using Queues](https://leetcode.com/problems/implement-stack-using-queues/) · [Solution](problems/0001-0499/225.py) · [Walkthrough](materials/walkthroughs/225-implement-stack-using-queues.md)
- [ ] ▰▰▰▱ [**232** Implement Queue using Stacks](https://leetcode.com/problems/implement-queue-using-stacks/) · [Solution](problems/0001-0499/232.py) · [Walkthrough](materials/walkthroughs/232-implement-queue-using-stacks.md)

$\color{#e67e22}{\textbf{Medium}}$

- [ ] ▰▰▱▱ [**155** Min Stack](https://leetcode.com/problems/min-stack/) · [Solution](problems/0001-0499/155.py) · [Walkthrough](materials/walkthroughs/155-min-stack.md)
- [ ] ▰▰▱▱ [**150** Evaluate Reverse Polish Notation](https://leetcode.com/problems/evaluate-reverse-polish-notation/) · [Solution](problems/0001-0499/150.py) · [Walkthrough](materials/walkthroughs/150-evaluate-reverse-polish-notation.md)
- [ ] ▰▰▱▱ [**22** Generate Parentheses](https://leetcode.com/problems/generate-parentheses/) · [Solution](problems/0001-0499/22.py) · [Walkthrough](materials/walkthroughs/22-generate-parentheses.md)
- [ ] ▰▰▱▱ [**739** Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) · [Solution](problems/0500-0999/739.py) · [Walkthrough](materials/walkthroughs/739-daily-temperatures.md)
- [ ] ▰▰▱▱ [**853** Car Fleet](https://leetcode.com/problems/car-fleet/) · [Solution](problems/0500-0999/853.py) · [Walkthrough](materials/walkthroughs/853-car-fleet.md)
- [ ] ▰▰▰▱ [**901** Online Stock Span](https://leetcode.com/problems/online-stock-span/) · [Solution](problems/0500-0999/901.py) · [Walkthrough](materials/walkthroughs/901-online-stock-span.md)
- [ ] ▰▰▰▱ [**71** Simplify Path](https://leetcode.com/problems/simplify-path/) · [Solution](problems/0001-0499/71.py) · [Walkthrough](materials/walkthroughs/71-simplify-path.md)
- [ ] ▰▰▰▱ [**394** Decode String](https://leetcode.com/problems/decode-string/) · [Solution](problems/0001-0499/394.py) · [Walkthrough](materials/walkthroughs/394-decode-string.md)
- [ ] ▰▰▰▰ [**503** Next Greater Element II](https://leetcode.com/problems/next-greater-element-ii/) · [Solution](problems/0500-0999/503.py) · [Walkthrough](materials/walkthroughs/503-next-greater-element-ii.md)

$\color{#cf222e}{\textbf{Hard}}$

- [ ] ▰▰▱▱ [**84** Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/) · [Solution](problems/0001-0499/84.py) · [Walkthrough](materials/walkthroughs/84-largest-rectangle-in-histogram.md)
- [ ] ▰▰▰▰ [**85** Maximal Rectangle](https://leetcode.com/problems/maximal-rectangle/) · [Solution](problems/0001-0499/85.py) · [Walkthrough](materials/walkthroughs/85-maximal-rectangle.md)

</details>

<details>
<summary><b>05 · Binary Search</b> — 0/18 ░░░░░░░░</summary>

Halve any ordered search space — including the answer.

[📖 Lesson](materials/learning/05-binary-search.md) · [📖 Sorting](materials/learning/05b-sorting.md)

$\color{#2da44e}{\textbf{Easy}}$

- [ ] ▰▰▱▱ [**704** Binary Search](https://leetcode.com/problems/binary-search/) · [Solution](problems/0500-0999/704.py) · [Walkthrough](materials/walkthroughs/704-binary-search.md)
- [ ] ▰▰▰▱ [**374** Guess Number Higher or Lower](https://leetcode.com/problems/guess-number-higher-or-lower/) · [Solution](problems/0001-0499/374.py) · [Walkthrough](materials/walkthroughs/374-guess-number-higher-or-lower.md)
- [ ] ▰▰▰▱ [**35** Search Insert Position](https://leetcode.com/problems/search-insert-position/) · [Solution](problems/0001-0499/35.py) · [Walkthrough](materials/walkthroughs/35-search-insert-position.md)
- [ ] ▰▰▰▰ [**278** First Bad Version](https://leetcode.com/problems/first-bad-version/) · [Solution](problems/0001-0499/278.py) · [Walkthrough](materials/walkthroughs/278-first-bad-version.md)
- [ ] ▰▰▰▱ [**69** Sqrt(x)](https://leetcode.com/problems/sqrtx/) · [Solution](problems/0001-0499/69.py) · [Walkthrough](materials/walkthroughs/69-sqrtx.md)
- [ ] ▰▰▰▰ [**367** Valid Perfect Square](https://leetcode.com/problems/valid-perfect-square/) · [Solution](problems/0001-0499/367.py) · [Walkthrough](materials/walkthroughs/367-valid-perfect-square.md)

$\color{#e67e22}{\textbf{Medium}}$

- [ ] ▰▰▱▱ [**74** Search a 2D Matrix](https://leetcode.com/problems/search-a-2d-matrix/) · [Solution](problems/0001-0499/74.py) · [Walkthrough](materials/walkthroughs/74-search-a-2d-matrix.md)
- [ ] ▰▰▱▱ [**875** Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/) · [Solution](problems/0500-0999/875.py) · [Walkthrough](materials/walkthroughs/875-koko-eating-bananas.md)
- [ ] ▰▱▱▱ [**153** Find Minimum in Rotated Sorted Array](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/) · [Solution](problems/0001-0499/153.py) · [Walkthrough](materials/walkthroughs/153-find-minimum-in-rotated-sorted-array.md)
- [ ] ▰▱▱▱ [**33** Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) · [Solution](problems/0001-0499/33.py) · [Walkthrough](materials/walkthroughs/33-search-in-rotated-sorted-array.md)
- [ ] ▰▰▰▰ [**34** Find First and Last Position of Element in Sorted Array](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/) · [Solution](problems/0001-0499/34.py) · [Walkthrough](materials/walkthroughs/34-find-first-and-last-position-of-element-in-sorted-array.md)
- [ ] ▰▰▰▰ [**162** Find Peak Element](https://leetcode.com/problems/find-peak-element/) · [Solution](problems/0001-0499/162.py) · [Walkthrough](materials/walkthroughs/162-find-peak-element.md)
- [ ] ▰▰▰▰ [**540** Single Element in a Sorted Array](https://leetcode.com/problems/single-element-in-a-sorted-array/) · [Solution](problems/0500-0999/540.py) · [Walkthrough](materials/walkthroughs/540-single-element-in-a-sorted-array.md)
- [ ] ▰▰▰▱ [**1011** Capacity To Ship Packages Within D Days](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/) · [Solution](problems/1000-1499/1011.py) · [Walkthrough](materials/walkthroughs/1011-capacity-to-ship-packages-within-d-days.md)
- [ ] ▰▰▰▱ [**658** Find K Closest Elements](https://leetcode.com/problems/find-k-closest-elements/) · [Solution](problems/0500-0999/658.py) · [Walkthrough](materials/walkthroughs/658-find-k-closest-elements.md)
- [ ] ▰▰▱▱ [**981** Time Based Key-Value Store](https://leetcode.com/problems/time-based-key-value-store/) · [Solution](problems/0500-0999/981.py) · [Walkthrough](materials/walkthroughs/981-time-based-key-value-store.md)

$\color{#cf222e}{\textbf{Hard}}$

- [ ] ▰▰▱▱ [**4** Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/) · [Solution](problems/0001-0499/4.py) · [Walkthrough](materials/walkthroughs/4-median-of-two-sorted-arrays.md)
- [ ] ▰▰▰▱ [**410** Split Array Largest Sum](https://leetcode.com/problems/split-array-largest-sum/) · [Solution](problems/0001-0499/410.py) · [Walkthrough](materials/walkthroughs/410-split-array-largest-sum.md)

</details>

<details>
<summary><b>06 · Linked List</b> — 0/20 ░░░░░░░░</summary>

Pointer surgery: reverse, dummy head, fast/slow.

[📖 Lesson](materials/learning/06-linked-list.md)

$\color{#2da44e}{\textbf{Easy}}$

- [ ] ▰▱▱▱ [**206** Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) · [Solution](problems/0001-0499/206.py) · [Walkthrough](materials/walkthroughs/206-reverse-linked-list.md)
- [ ] ▰▱▱▱ [**21** Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) · [Solution](problems/0001-0499/21.py) · [Walkthrough](materials/walkthroughs/21-merge-two-sorted-lists.md)
- [ ] ▰▰▰▰ [**876** Middle of the Linked List](https://leetcode.com/problems/middle-of-the-linked-list/) · [Solution](problems/0500-0999/876.py) · [Walkthrough](materials/walkthroughs/876-middle-of-the-linked-list.md)
- [ ] ▰▱▱▱ [**141** Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/) · [Solution](problems/0001-0499/141.py) · [Walkthrough](materials/walkthroughs/141-linked-list-cycle.md)
- [ ] ▰▰▰▰ [**234** Palindrome Linked List](https://leetcode.com/problems/palindrome-linked-list/) · [Solution](problems/0001-0499/234.py) · [Walkthrough](materials/walkthroughs/234-palindrome-linked-list.md)
- [ ] ▰▰▰▰ [**203** Remove Linked List Elements](https://leetcode.com/problems/remove-linked-list-elements/) · [Solution](problems/0001-0499/203.py) · [Walkthrough](materials/walkthroughs/203-remove-linked-list-elements.md)
- [ ] ▰▰▰▰ [**83** Remove Duplicates from Sorted List](https://leetcode.com/problems/remove-duplicates-from-sorted-list/) · [Solution](problems/0001-0499/83.py) · [Walkthrough](materials/walkthroughs/83-remove-duplicates-from-sorted-list.md)
- [ ] ▰▰▰▰ [**160** Intersection of Two Linked Lists](https://leetcode.com/problems/intersection-of-two-linked-lists/) · [Solution](problems/0001-0499/160.py) · [Walkthrough](materials/walkthroughs/160-intersection-of-two-linked-lists.md)

$\color{#e67e22}{\textbf{Medium}}$

- [ ] ▰▱▱▱ [**143** Reorder List](https://leetcode.com/problems/reorder-list/) · [Solution](problems/0001-0499/143.py) · [Walkthrough](materials/walkthroughs/143-reorder-list.md)
- [ ] ▰▱▱▱ [**19** Remove Nth Node From End of List](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) · [Solution](problems/0001-0499/19.py) · [Walkthrough](materials/walkthroughs/19-remove-nth-node-from-end-of-list.md)
- [ ] ▰▰▰▱ [**92** Reverse Linked List II](https://leetcode.com/problems/reverse-linked-list-ii/) · [Solution](problems/0001-0499/92.py) · [Walkthrough](materials/walkthroughs/92-reverse-linked-list-ii.md)
- [ ] ▰▰▰▰ [**24** Swap Nodes in Pairs](https://leetcode.com/problems/swap-nodes-in-pairs/) · [Solution](problems/0001-0499/24.py) · [Walkthrough](materials/walkthroughs/24-swap-nodes-in-pairs.md)
- [ ] ▰▰▱▱ [**2** Add Two Numbers](https://leetcode.com/problems/add-two-numbers/) · [Solution](problems/0001-0499/2.py) · [Walkthrough](materials/walkthroughs/2-add-two-numbers.md)
- [ ] ▰▰▱▱ [**138** Copy List with Random Pointer](https://leetcode.com/problems/copy-list-with-random-pointer/) · [Solution](problems/0001-0499/138.py) · [Walkthrough](materials/walkthroughs/138-copy-list-with-random-pointer.md)
- [ ] ▰▰▱▱ [**287** Find the Duplicate Number](https://leetcode.com/problems/find-the-duplicate-number/) · [Solution](problems/0001-0499/287.py) · [Walkthrough](materials/walkthroughs/287-find-the-duplicate-number.md)
- [ ] ▰▰▱▱ [**146** LRU Cache](https://leetcode.com/problems/lru-cache/) · [Solution](problems/0001-0499/146.py) · [Walkthrough](materials/walkthroughs/146-lru-cache.md)
- [ ] ▰▰▰▰ [**61** Rotate List](https://leetcode.com/problems/rotate-list/) · [Solution](problems/0001-0499/61.py) · [Walkthrough](materials/walkthroughs/61-rotate-list.md)
- [ ] ▰▰▰▰ [**86** Partition List](https://leetcode.com/problems/partition-list/) · [Solution](problems/0001-0499/86.py) · [Walkthrough](materials/walkthroughs/86-partition-list.md)

$\color{#cf222e}{\textbf{Hard}}$

- [ ] ▰▱▱▱ [**23** Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/) · [Solution](problems/0001-0499/23.py) · [Walkthrough](materials/walkthroughs/23-merge-k-sorted-lists.md)
- [ ] ▰▰▱▱ [**25** Reverse Nodes in k-Group](https://leetcode.com/problems/reverse-nodes-in-k-group/) · [Solution](problems/0001-0499/25.py) · [Walkthrough](materials/walkthroughs/25-reverse-nodes-in-k-group.md)

</details>

<details>
<summary><b>07 · Trees & BSTs</b> — 0/29 ░░░░░░░░</summary>

DFS base→recurse→combine, or BFS level-by-level.

[📖 Lesson](materials/learning/07-trees.md)

$\color{#2da44e}{\textbf{Easy}}$

- [ ] ▰▱▱▱ [**226** Invert Binary Tree](https://leetcode.com/problems/invert-binary-tree/) · [Solution](problems/0001-0499/226.py) · [Walkthrough](materials/walkthroughs/226-invert-binary-tree.md)
- [ ] ▰▱▱▱ [**104** Maximum Depth of Binary Tree](https://leetcode.com/problems/maximum-depth-of-binary-tree/) · [Solution](problems/0001-0499/104.py) · [Walkthrough](materials/walkthroughs/104-maximum-depth-of-binary-tree.md)
- [ ] ▰▰▱▱ [**543** Diameter of Binary Tree](https://leetcode.com/problems/diameter-of-binary-tree/) · [Solution](problems/0500-0999/543.py) · [Walkthrough](materials/walkthroughs/543-diameter-of-binary-tree.md)
- [ ] ▰▰▱▱ [**110** Balanced Binary Tree](https://leetcode.com/problems/balanced-binary-tree/) · [Solution](problems/0001-0499/110.py) · [Walkthrough](materials/walkthroughs/110-balanced-binary-tree.md)
- [ ] ▰▱▱▱ [**100** Same Tree](https://leetcode.com/problems/same-tree/) · [Solution](problems/0001-0499/100.py) · [Walkthrough](materials/walkthroughs/100-same-tree.md)
- [ ] ▰▱▱▱ [**572** Subtree of Another Tree](https://leetcode.com/problems/subtree-of-another-tree/) · [Solution](problems/0500-0999/572.py) · [Walkthrough](materials/walkthroughs/572-subtree-of-another-tree.md)
- [ ] ▰▰▰▰ [**112** Path Sum](https://leetcode.com/problems/path-sum/) · [Solution](problems/0001-0499/112.py) · [Walkthrough](materials/walkthroughs/112-path-sum.md)
- [ ] ▰▰▰▰ [**111** Minimum Depth of Binary Tree](https://leetcode.com/problems/minimum-depth-of-binary-tree/) · [Solution](problems/0001-0499/111.py) · [Walkthrough](materials/walkthroughs/111-minimum-depth-of-binary-tree.md)
- [ ] ▰▰▰▰ [**101** Symmetric Tree](https://leetcode.com/problems/symmetric-tree/) · [Solution](problems/0001-0499/101.py) · [Walkthrough](materials/walkthroughs/101-symmetric-tree.md)
- [ ] ▰▰▰▰ [**108** Convert Sorted Array to Binary Search Tree](https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/) · [Solution](problems/0001-0499/108.py) · [Walkthrough](materials/walkthroughs/108-convert-sorted-array-to-binary-search-tree.md)
- [ ] ▰▰▰▰ [**700** Search in a Binary Search Tree](https://leetcode.com/problems/search-in-a-binary-search-tree/) · [Solution](problems/0500-0999/700.py) · [Walkthrough](materials/walkthroughs/700-search-in-a-binary-search-tree.md)
- [ ] ▰▰▰▱ [**94** Binary Tree Inorder Traversal](https://leetcode.com/problems/binary-tree-inorder-traversal/) · [Solution](problems/0001-0499/94.py) · [Walkthrough](materials/walkthroughs/94-binary-tree-inorder-traversal.md)
- [ ] ▰▰▰▱ [**144** Binary Tree Preorder Traversal](https://leetcode.com/problems/binary-tree-preorder-traversal/) · [Solution](problems/0001-0499/144.py) · [Walkthrough](materials/walkthroughs/144-binary-tree-preorder-traversal.md)
- [ ] ▰▰▰▱ [**145** Binary Tree Postorder Traversal](https://leetcode.com/problems/binary-tree-postorder-traversal/) · [Solution](problems/0001-0499/145.py) · [Walkthrough](materials/walkthroughs/145-binary-tree-postorder-traversal.md)
- [ ] ▰▰▰▰ [**257** Binary Tree Paths](https://leetcode.com/problems/binary-tree-paths/) · [Solution](problems/0001-0499/257.py) · [Walkthrough](materials/walkthroughs/257-binary-tree-paths.md)

$\color{#e67e22}{\textbf{Medium}}$

- [ ] ▰▱▱▱ [**235** Lowest Common Ancestor of a Binary Search Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/) · [Solution](problems/0001-0499/235.py) · [Walkthrough](materials/walkthroughs/235-lowest-common-ancestor-of-a-binary-search-tree.md)
- [ ] ▰▱▱▱ [**102** Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) · [Solution](problems/0001-0499/102.py) · [Walkthrough](materials/walkthroughs/102-binary-tree-level-order-traversal.md)
- [ ] ▰▰▱▱ [**199** Binary Tree Right Side View](https://leetcode.com/problems/binary-tree-right-side-view/) · [Solution](problems/0001-0499/199.py) · [Walkthrough](materials/walkthroughs/199-binary-tree-right-side-view.md)
- [ ] ▰▰▱▱ [**1448** Count Good Nodes in Binary Tree](https://leetcode.com/problems/count-good-nodes-in-binary-tree/) · [Solution](problems/1000-1499/1448.py) · [Walkthrough](materials/walkthroughs/1448-count-good-nodes-in-binary-tree.md)
- [ ] ▰▱▱▱ [**98** Validate Binary Search Tree](https://leetcode.com/problems/validate-binary-search-tree/) · [Solution](problems/0001-0499/98.py) · [Walkthrough](materials/walkthroughs/98-validate-binary-search-tree.md)
- [ ] ▰▱▱▱ [**230** Kth Smallest Element in a BST](https://leetcode.com/problems/kth-smallest-element-in-a-bst/) · [Solution](problems/0001-0499/230.py) · [Walkthrough](materials/walkthroughs/230-kth-smallest-element-in-a-bst.md)
- [ ] ▰▱▱▱ [**105** Construct Binary Tree from Preorder and Inorder Traversal](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/) · [Solution](problems/0001-0499/105.py) · [Walkthrough](materials/walkthroughs/105-construct-binary-tree-from-preorder-and-inorder-traversal.md)
- [ ] ▰▰▰▱ [**701** Insert into a Binary Search Tree](https://leetcode.com/problems/insert-into-a-binary-search-tree/) · [Solution](problems/0500-0999/701.py) · [Walkthrough](materials/walkthroughs/701-insert-into-a-binary-search-tree.md)
- [ ] ▰▰▰▱ [**450** Delete Node in a BST](https://leetcode.com/problems/delete-node-in-a-bst/) · [Solution](problems/0001-0499/450.py) · [Walkthrough](materials/walkthroughs/450-delete-node-in-a-bst.md)
- [ ] ▰▰▰▰ [**116** Populating Next Right Pointers in Each Node](https://leetcode.com/problems/populating-next-right-pointers-in-each-node/) · [Solution](problems/0001-0499/116.py) · [Walkthrough](materials/walkthroughs/116-populating-next-right-pointers-in-each-node.md)
- [ ] ▰▰▰▰ [**103** Binary Tree Zigzag Level Order Traversal](https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/) · [Solution](problems/0001-0499/103.py) · [Walkthrough](materials/walkthroughs/103-binary-tree-zigzag-level-order-traversal.md)
- [ ] ▰▰▰▰ [**236** Lowest Common Ancestor of a Binary Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) · [Solution](problems/0001-0499/236.py) · [Walkthrough](materials/walkthroughs/236-lowest-common-ancestor-of-a-binary-tree.md)

$\color{#cf222e}{\textbf{Hard}}$

- [ ] ▰▱▱▱ [**124** Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) · [Solution](problems/0001-0499/124.py) · [Walkthrough](materials/walkthroughs/124-binary-tree-maximum-path-sum.md)
- [ ] ▰▱▱▱ [**297** Serialize and Deserialize Binary Tree](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) · [Solution](problems/0001-0499/297.py) · [Walkthrough](materials/walkthroughs/297-serialize-and-deserialize-binary-tree.md)

</details>

<details>
<summary><b>08 · Tries</b> — 0/6 ░░░░░░░░</summary>

Prefix trees: O(k) prefix queries.

[📖 Lesson](materials/learning/08-tries.md)

$\color{#e67e22}{\textbf{Medium}}$

- [ ] ▰▱▱▱ [**208** Implement Trie (Prefix Tree)](https://leetcode.com/problems/implement-trie-prefix-tree/) · [Solution](problems/0001-0499/208.py) · [Walkthrough](materials/walkthroughs/208-implement-trie-prefix-tree.md)
- [ ] ▰▱▱▱ [**211** Design Add and Search Words Data Structure](https://leetcode.com/problems/design-add-and-search-words-data-structure/) · [Solution](problems/0001-0499/211.py) · [Walkthrough](materials/walkthroughs/211-design-add-and-search-words-data-structure.md)
- [ ] ▰▰▰▰ [**648** Replace Words](https://leetcode.com/problems/replace-words/) · [Solution](problems/0500-0999/648.py) · [Walkthrough](materials/walkthroughs/648-replace-words.md)
- [ ] ▰▰▰▰ [**677** Map Sum Pairs](https://leetcode.com/problems/map-sum-pairs/) · [Solution](problems/0500-0999/677.py) · [Walkthrough](materials/walkthroughs/677-map-sum-pairs.md)
- [ ] ▰▰▰▰ [**1268** Search Suggestions System](https://leetcode.com/problems/search-suggestions-system/) · [Solution](problems/1000-1499/1268.py) · [Walkthrough](materials/walkthroughs/1268-search-suggestions-system.md)

$\color{#cf222e}{\textbf{Hard}}$

- [ ] ▰▱▱▱ [**212** Word Search II](https://leetcode.com/problems/word-search-ii/) · [Solution](problems/0001-0499/212.py) · [Walkthrough](materials/walkthroughs/212-word-search-ii.md)

</details>

<details>
<summary><b>09 · Heap / Priority Queue</b> — 0/14 ░░░░░░░░</summary>

The always-available extreme element; top-K & streaming.

[📖 Lesson](materials/learning/09-heap-priority-queue.md)

$\color{#2da44e}{\textbf{Easy}}$

- [ ] ▰▰▱▱ [**703** Kth Largest Element in a Stream](https://leetcode.com/problems/kth-largest-element-in-a-stream/) · [Solution](problems/0500-0999/703.py) · [Walkthrough](materials/walkthroughs/703-kth-largest-element-in-a-stream.md)
- [ ] ▰▰▱▱ [**1046** Last Stone Weight](https://leetcode.com/problems/last-stone-weight/) · [Solution](problems/1000-1499/1046.py) · [Walkthrough](materials/walkthroughs/1046-last-stone-weight.md)

$\color{#e67e22}{\textbf{Medium}}$

- [ ] ▰▰▱▱ [**215** Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) · [Solution](problems/0001-0499/215.py) · [Walkthrough](materials/walkthroughs/215-kth-largest-element-in-an-array.md)
- [ ] ▰▰▱▱ [**973** K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/) · [Solution](problems/0500-0999/973.py) · [Walkthrough](materials/walkthroughs/973-k-closest-points-to-origin.md)
- [ ] ▰▰▱▱ [**621** Task Scheduler](https://leetcode.com/problems/task-scheduler/) · [Solution](problems/0500-0999/621.py) · [Walkthrough](materials/walkthroughs/621-task-scheduler.md)
- [ ] ▰▰▱▱ [**355** Design Twitter](https://leetcode.com/problems/design-twitter/) · [Solution](problems/0001-0499/355.py) · [Walkthrough](materials/walkthroughs/355-design-twitter.md)
- [ ] ▰▰▰▰ [**692** Top K Frequent Words](https://leetcode.com/problems/top-k-frequent-words/) · [Solution](problems/0500-0999/692.py) · [Walkthrough](materials/walkthroughs/692-top-k-frequent-words.md)
- [ ] ▰▰▰▱ [**767** Reorganize String](https://leetcode.com/problems/reorganize-string/) · [Solution](problems/0500-0999/767.py) · [Walkthrough](materials/walkthroughs/767-reorganize-string.md)
- [ ] ▰▰▰▱ [**1834** Single-Threaded CPU](https://leetcode.com/problems/single-threaded-cpu/) · [Solution](problems/1500-1999/1834.py) · [Walkthrough](materials/walkthroughs/1834-single-threaded-cpu.md)
- [ ] ▰▰▰▰ [**1985** Find the Kth Largest Integer in the Array](https://leetcode.com/problems/find-the-kth-largest-integer-in-the-array/) · [Solution](problems/1500-1999/1985.py) · [Walkthrough](materials/walkthroughs/1985-find-the-kth-largest-integer-in-the-array.md)
- [ ] ▰▰▰▰ [**2542** Maximum Subsequence Score](https://leetcode.com/problems/maximum-subsequence-score/) · [Solution](problems/2500-2999/2542.py) · [Walkthrough](materials/walkthroughs/2542-maximum-subsequence-score.md)
- [ ] ▰▰▰▰ [**1962** Remove Stones to Minimize the Total](https://leetcode.com/problems/remove-stones-to-minimize-the-total/) · [Solution](problems/1500-1999/1962.py) · [Walkthrough](materials/walkthroughs/1962-remove-stones-to-minimize-the-total.md)

$\color{#cf222e}{\textbf{Hard}}$

- [ ] ▰▱▱▱ [**295** Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/) · [Solution](problems/0001-0499/295.py) · [Walkthrough](materials/walkthroughs/295-find-median-from-data-stream.md)
- [ ] ▰▰▰▱ [**502** IPO](https://leetcode.com/problems/ipo/) · [Solution](problems/0500-0999/502.py) · [Walkthrough](materials/walkthroughs/502-ipo.md)

</details>

<details>
<summary><b>10 · Backtracking</b> — 0/16 ░░░░░░░░</summary>

Choose → explore → un-choose over partial solutions.

[📖 Lesson](materials/learning/10-backtracking.md)

$\color{#e67e22}{\textbf{Medium}}$

- [ ] ▰▰▱▱ [**78** Subsets](https://leetcode.com/problems/subsets/) · [Solution](problems/0001-0499/78.py) · [Walkthrough](materials/walkthroughs/78-subsets.md)
- [ ] ▰▰▱▱ [**90** Subsets II](https://leetcode.com/problems/subsets-ii/) · [Solution](problems/0001-0499/90.py) · [Walkthrough](materials/walkthroughs/90-subsets-ii.md)
- [ ] ▰▱▱▱ [**39** Combination Sum](https://leetcode.com/problems/combination-sum/) · [Solution](problems/0001-0499/39.py) · [Walkthrough](materials/walkthroughs/39-combination-sum.md)
- [ ] ▰▰▱▱ [**40** Combination Sum II](https://leetcode.com/problems/combination-sum-ii/) · [Solution](problems/0001-0499/40.py) · [Walkthrough](materials/walkthroughs/40-combination-sum-ii.md)
- [ ] ▰▰▰▰ [**216** Combination Sum III](https://leetcode.com/problems/combination-sum-iii/) · [Solution](problems/0001-0499/216.py) · [Walkthrough](materials/walkthroughs/216-combination-sum-iii.md)
- [ ] ▰▰▱▱ [**46** Permutations](https://leetcode.com/problems/permutations/) · [Solution](problems/0001-0499/46.py) · [Walkthrough](materials/walkthroughs/46-permutations.md)
- [ ] ▰▰▰▱ [**47** Permutations II](https://leetcode.com/problems/permutations-ii/) · [Solution](problems/0001-0499/47.py) · [Walkthrough](materials/walkthroughs/47-permutations-ii.md)
- [ ] ▰▰▰▱ [**77** Combinations](https://leetcode.com/problems/combinations/) · [Solution](problems/0001-0499/77.py) · [Walkthrough](materials/walkthroughs/77-combinations.md)
- [ ] ▰▰▱▱ [**17** Letter Combinations of a Phone Number](https://leetcode.com/problems/letter-combinations-of-a-phone-number/) · [Solution](problems/0001-0499/17.py) · [Walkthrough](materials/walkthroughs/17-letter-combinations-of-a-phone-number.md)
- [ ] ▰▱▱▱ [**79** Word Search](https://leetcode.com/problems/word-search/) · [Solution](problems/0001-0499/79.py) · [Walkthrough](materials/walkthroughs/79-word-search.md)
- [ ] ▰▰▱▱ [**131** Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/) · [Solution](problems/0001-0499/131.py) · [Walkthrough](materials/walkthroughs/131-palindrome-partitioning.md)
- [ ] ▰▰▰▰ [**93** Restore IP Addresses](https://leetcode.com/problems/restore-ip-addresses/) · [Solution](problems/0001-0499/93.py) · [Walkthrough](materials/walkthroughs/93-restore-ip-addresses.md)
- [ ] ▰▰▰▱ [**698** Partition to K Equal Sum Subsets](https://leetcode.com/problems/partition-to-k-equal-sum-subsets/) · [Solution](problems/0500-0999/698.py) · [Walkthrough](materials/walkthroughs/698-partition-to-k-equal-sum-subsets.md)
- [ ] ▰▰▰▰ [**526** Beautiful Arrangement](https://leetcode.com/problems/beautiful-arrangement/) · [Solution](problems/0500-0999/526.py) · [Walkthrough](materials/walkthroughs/526-beautiful-arrangement.md)

$\color{#cf222e}{\textbf{Hard}}$

- [ ] ▰▰▱▱ [**51** N-Queens](https://leetcode.com/problems/n-queens/) · [Solution](problems/0001-0499/51.py) · [Walkthrough](materials/walkthroughs/51-n-queens.md)
- [ ] ▰▰▰▱ [**52** N-Queens II](https://leetcode.com/problems/n-queens-ii/) · [Solution](problems/0001-0499/52.py) · [Walkthrough](materials/walkthroughs/52-n-queens-ii.md)

</details>

<details>
<summary><b>11 · Graphs</b> — 0/23 ░░░░░░░░</summary>

BFS for shortest unweighted paths, DFS for connectivity.

[📖 Lesson](materials/learning/11-graphs.md) · [📖 Grids primer](materials/learning/10b-grids-primer.md) · [📖 Union-Find](materials/learning/12-union-find.md)

$\color{#2da44e}{\textbf{Easy}}$

- [ ] ▰▰▰▰ [**733** Flood Fill](https://leetcode.com/problems/flood-fill/) · [Solution](problems/0500-0999/733.py) · [Walkthrough](materials/walkthroughs/733-flood-fill.md)
- [ ] ▰▰▰▱ [**463** Island Perimeter](https://leetcode.com/problems/island-perimeter/) · [Solution](problems/0001-0499/463.py) · [Walkthrough](materials/walkthroughs/463-island-perimeter.md)
- [ ] ▰▰▰▰ [**1971** Find if Path Exists in Graph](https://leetcode.com/problems/find-if-path-exists-in-graph/) · [Solution](problems/1500-1999/1971.py) · [Walkthrough](materials/walkthroughs/1971-find-if-path-exists-in-graph.md)

$\color{#e67e22}{\textbf{Medium}}$

- [ ] ▰▱▱▱ [**200** Number of Islands](https://leetcode.com/problems/number-of-islands/) · [Solution](problems/0001-0499/200.py) · [Walkthrough](materials/walkthroughs/200-number-of-islands.md)
- [ ] ▰▰▱▱ [**695** Max Area of Island](https://leetcode.com/problems/max-area-of-island/) · [Solution](problems/0500-0999/695.py) · [Walkthrough](materials/walkthroughs/695-max-area-of-island.md)
- [ ] ▰▱▱▱ [**133** Clone Graph](https://leetcode.com/problems/clone-graph/) · [Solution](problems/0001-0499/133.py) · [Walkthrough](materials/walkthroughs/133-clone-graph.md)
- [ ] ▰▰▱▱ [**994** Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) · [Solution](problems/0500-0999/994.py) · [Walkthrough](materials/walkthroughs/994-rotting-oranges.md)
- [ ] ▰▰▱▱ [**286** Walls and Gates](https://leetcode.com/problems/walls-and-gates/) · [Solution](problems/0001-0499/286.py) · [Walkthrough](materials/walkthroughs/286-walls-and-gates.md)
- [ ] ▰▱▱▱ [**417** Pacific Atlantic Water Flow](https://leetcode.com/problems/pacific-atlantic-water-flow/) · [Solution](problems/0001-0499/417.py) · [Walkthrough](materials/walkthroughs/417-pacific-atlantic-water-flow.md)
- [ ] ▰▰▱▱ [**130** Surrounded Regions](https://leetcode.com/problems/surrounded-regions/) · [Solution](problems/0001-0499/130.py) · [Walkthrough](materials/walkthroughs/130-surrounded-regions.md)
- [ ] ▰▱▱▱ [**207** Course Schedule](https://leetcode.com/problems/course-schedule/) · [Solution](problems/0001-0499/207.py) · [Walkthrough](materials/walkthroughs/207-course-schedule.md)
- [ ] ▰▰▱▱ [**210** Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) · [Solution](problems/0001-0499/210.py) · [Walkthrough](materials/walkthroughs/210-course-schedule-ii.md)
- [ ] ▰▱▱▱ [**261** Graph Valid Tree](https://leetcode.com/problems/graph-valid-tree/) · [Solution](problems/0001-0499/261.py) · [Walkthrough](materials/walkthroughs/261-graph-valid-tree.md)
- [ ] ▰▱▱▱ [**323** Number of Connected Components in an Undirected Graph](https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/) · [Solution](problems/0001-0499/323.py) · [Walkthrough](materials/walkthroughs/323-number-of-connected-components-in-an-undirected-graph.md)
- [ ] ▰▰▱▱ [**684** Redundant Connection](https://leetcode.com/problems/redundant-connection/) · [Solution](problems/0500-0999/684.py) · [Walkthrough](materials/walkthroughs/684-redundant-connection.md)
- [ ] ▰▰▰▰ [**547** Number of Provinces](https://leetcode.com/problems/number-of-provinces/) · [Solution](problems/0500-0999/547.py) · [Walkthrough](materials/walkthroughs/547-number-of-provinces.md)
- [ ] ▰▰▰▰ [**785** Is Graph Bipartite?](https://leetcode.com/problems/is-graph-bipartite/) · [Solution](problems/0500-0999/785.py) · [Walkthrough](materials/walkthroughs/785-is-graph-bipartite.md)
- [ ] ▰▰▰▰ [**802** Find Eventual Safe States](https://leetcode.com/problems/find-eventual-safe-states/) · [Solution](problems/0500-0999/802.py) · [Walkthrough](materials/walkthroughs/802-find-eventual-safe-states.md)
- [ ] ▰▰▰▰ [**1466** Reorder Routes to Make All Paths Lead to the City Zero](https://leetcode.com/problems/reorder-routes-to-make-all-paths-lead-to-the-city-zero/) · [Solution](problems/1000-1499/1466.py) · [Walkthrough](materials/walkthroughs/1466-reorder-routes-to-make-all-paths-lead-to-the-city-zero.md)
- [ ] ▰▰▰▰ [**841** Keys and Rooms](https://leetcode.com/problems/keys-and-rooms/) · [Solution](problems/0500-0999/841.py) · [Walkthrough](materials/walkthroughs/841-keys-and-rooms.md)
- [ ] ▰▰▰▰ [**1020** Number of Enclaves](https://leetcode.com/problems/number-of-enclaves/) · [Solution](problems/1000-1499/1020.py) · [Walkthrough](materials/walkthroughs/1020-number-of-enclaves.md)

$\color{#cf222e}{\textbf{Hard}}$

- [ ] ▰▰▱▱ [**127** Word Ladder](https://leetcode.com/problems/word-ladder/) · [Solution](problems/0001-0499/127.py) · [Walkthrough](materials/walkthroughs/127-word-ladder.md)
- [ ] ▰▱▱▱ [**269** Alien Dictionary](https://leetcode.com/problems/alien-dictionary/) · [Solution](problems/0001-0499/269.py) · [Walkthrough](materials/walkthroughs/269-alien-dictionary.md)

</details>

<details>
<summary><b>12 · Advanced Graphs</b> — 0/11 ░░░░░░░░</summary>

Weighted shortest paths (Dijkstra), ordering (topo sort).

[📖 Lesson](materials/learning/13-advanced-graphs.md)

$\color{#e67e22}{\textbf{Medium}}$

- [ ] ▰▰▱▱ [**743** Network Delay Time](https://leetcode.com/problems/network-delay-time/) · [Solution](problems/0500-0999/743.py) · [Walkthrough](materials/walkthroughs/743-network-delay-time.md)
- [ ] ▰▰▱▱ [**1584** Min Cost to Connect All Points](https://leetcode.com/problems/min-cost-to-connect-all-points/) · [Solution](problems/1500-1999/1584.py) · [Walkthrough](materials/walkthroughs/1584-min-cost-to-connect-all-points.md)
- [ ] ▰▰▱▱ [**787** Cheapest Flights Within K Stops](https://leetcode.com/problems/cheapest-flights-within-k-stops/) · [Solution](problems/0500-0999/787.py) · [Walkthrough](materials/walkthroughs/787-cheapest-flights-within-k-stops.md)
- [ ] ▰▰▰▱ [**1631** Path With Minimum Effort](https://leetcode.com/problems/path-with-minimum-effort/) · [Solution](problems/1500-1999/1631.py) · [Walkthrough](materials/walkthroughs/1631-path-with-minimum-effort.md)
- [ ] ▰▰▰▰ [**1976** Number of Ways to Arrive at Destination](https://leetcode.com/problems/number-of-ways-to-arrive-at-destination/) · [Solution](problems/1500-1999/1976.py) · [Walkthrough](materials/walkthroughs/1976-number-of-ways-to-arrive-at-destination.md)
- [ ] ▰▰▰▰ [**2492** Minimum Score of a Path Between Two Cities](https://leetcode.com/problems/minimum-score-of-a-path-between-two-cities/) · [Solution](problems/2000-2499/2492.py) · [Walkthrough](materials/walkthroughs/2492-minimum-score-of-a-path-between-two-cities.md)
- [ ] ▰▰▰▱ [**1462** Course Schedule IV](https://leetcode.com/problems/course-schedule-iv/) · [Solution](problems/1000-1499/1462.py) · [Walkthrough](materials/walkthroughs/1462-course-schedule-iv.md)

$\color{#cf222e}{\textbf{Hard}}$

- [ ] ▰▰▱▱ [**332** Reconstruct Itinerary](https://leetcode.com/problems/reconstruct-itinerary/) · [Solution](problems/0001-0499/332.py) · [Walkthrough](materials/walkthroughs/332-reconstruct-itinerary.md)
- [ ] ▰▰▱▱ [**778** Swim in Rising Water](https://leetcode.com/problems/swim-in-rising-water/) · [Solution](problems/0500-0999/778.py) · [Walkthrough](materials/walkthroughs/778-swim-in-rising-water.md)
- [ ] ▰▰▰▰ [**685** Redundant Connection II](https://leetcode.com/problems/redundant-connection-ii/) · [Solution](problems/0500-0999/685.py) · [Walkthrough](materials/walkthroughs/685-redundant-connection-ii.md)
- [ ] ▰▰▰▰ [**847** Shortest Path Visiting All Nodes](https://leetcode.com/problems/shortest-path-visiting-all-nodes/) · [Solution](problems/0500-0999/847.py) · [Walkthrough](materials/walkthroughs/847-shortest-path-visiting-all-nodes.md)

</details>

<details>
<summary><b>13 · 1-D Dynamic Programming</b> — 0/22 ░░░░░░░░</summary>

State + transition + base case over one axis.

[📖 Lesson](materials/learning/14-dp-1d.md)

$\color{#2da44e}{\textbf{Easy}}$

- [ ] ▰▱▱▱ [**70** Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) · [Solution](problems/0001-0499/70.py) · [Walkthrough](materials/walkthroughs/70-climbing-stairs.md)
- [ ] ▰▰▱▱ [**746** Min Cost Climbing Stairs](https://leetcode.com/problems/min-cost-climbing-stairs/) · [Solution](problems/0500-0999/746.py) · [Walkthrough](materials/walkthroughs/746-min-cost-climbing-stairs.md)
- [ ] ▰▰▰▱ [**1137** N-th Tribonacci Number](https://leetcode.com/problems/n-th-tribonacci-number/) · [Solution](problems/1000-1499/1137.py) · [Walkthrough](materials/walkthroughs/1137-n-th-tribonacci-number.md)

$\color{#e67e22}{\textbf{Medium}}$

- [ ] ▰▱▱▱ [**198** House Robber](https://leetcode.com/problems/house-robber/) · [Solution](problems/0001-0499/198.py) · [Walkthrough](materials/walkthroughs/198-house-robber.md)
- [ ] ▰▱▱▱ [**213** House Robber II](https://leetcode.com/problems/house-robber-ii/) · [Solution](problems/0001-0499/213.py) · [Walkthrough](materials/walkthroughs/213-house-robber-ii.md)
- [ ] ▰▱▱▱ [**5** Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/) · [Solution](problems/0001-0499/5.py) · [Walkthrough](materials/walkthroughs/5-longest-palindromic-substring.md)
- [ ] ▰▱▱▱ [**647** Palindromic Substrings](https://leetcode.com/problems/palindromic-substrings/) · [Solution](problems/0500-0999/647.py) · [Walkthrough](materials/walkthroughs/647-palindromic-substrings.md)
- [ ] ▰▱▱▱ [**91** Decode Ways](https://leetcode.com/problems/decode-ways/) · [Solution](problems/0001-0499/91.py) · [Walkthrough](materials/walkthroughs/91-decode-ways.md)
- [ ] ▰▱▱▱ [**322** Coin Change](https://leetcode.com/problems/coin-change/) · [Solution](problems/0001-0499/322.py) · [Walkthrough](materials/walkthroughs/322-coin-change.md)
- [ ] ▰▰▱▱ [**518** Coin Change II](https://leetcode.com/problems/coin-change-ii/) · [Solution](problems/0500-0999/518.py) · [Walkthrough](materials/walkthroughs/518-coin-change-ii.md)
- [ ] ▰▱▱▱ [**152** Maximum Product Subarray](https://leetcode.com/problems/maximum-product-subarray/) · [Solution](problems/0001-0499/152.py) · [Walkthrough](materials/walkthroughs/152-maximum-product-subarray.md)
- [ ] ▰▱▱▱ [**139** Word Break](https://leetcode.com/problems/word-break/) · [Solution](problems/0001-0499/139.py) · [Walkthrough](materials/walkthroughs/139-word-break.md)
- [ ] ▰▱▱▱ [**300** Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/) · [Solution](problems/0001-0499/300.py) · [Walkthrough](materials/walkthroughs/300-longest-increasing-subsequence.md)
- [ ] ▰▰▰▱ [**377** Combination Sum IV](https://leetcode.com/problems/combination-sum-iv/) · [Solution](problems/0001-0499/377.py) · [Walkthrough](materials/walkthroughs/377-combination-sum-iv.md)
- [ ] ▰▰▱▱ [**416** Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/) · [Solution](problems/0001-0499/416.py) · [Walkthrough](materials/walkthroughs/416-partition-equal-subset-sum.md)
- [ ] ▰▰▰▰ [**740** Delete and Earn](https://leetcode.com/problems/delete-and-earn/) · [Solution](problems/0500-0999/740.py) · [Walkthrough](materials/walkthroughs/740-delete-and-earn.md)
- [ ] ▰▰▰▱ [**279** Perfect Squares](https://leetcode.com/problems/perfect-squares/) · [Solution](problems/0001-0499/279.py) · [Walkthrough](materials/walkthroughs/279-perfect-squares.md)
- [ ] ▰▰▰▱ [**343** Integer Break](https://leetcode.com/problems/integer-break/) · [Solution](problems/0001-0499/343.py) · [Walkthrough](materials/walkthroughs/343-integer-break.md)
- [ ] ▰▰▱▱ [**309** Best Time to Buy and Sell Stock with Cooldown](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/) · [Solution](problems/0001-0499/309.py) · [Walkthrough](materials/walkthroughs/309-best-time-to-buy-and-sell-stock-with-cooldown.md)
- [ ] ▰▰▰▰ [**96** Unique Binary Search Trees](https://leetcode.com/problems/unique-binary-search-trees/) · [Solution](problems/0001-0499/96.py) · [Walkthrough](materials/walkthroughs/96-unique-binary-search-trees.md)
- [ ] ▰▰▰▰ [**1027** Longest Arithmetic Subsequence](https://leetcode.com/problems/longest-arithmetic-subsequence/) · [Solution](problems/1000-1499/1027.py) · [Walkthrough](materials/walkthroughs/1027-longest-arithmetic-subsequence.md)

$\color{#cf222e}{\textbf{Hard}}$

- [ ] ▰▰▰▰ [**132** Palindrome Partitioning II](https://leetcode.com/problems/palindrome-partitioning-ii/) · [Solution](problems/0001-0499/132.py) · [Walkthrough](materials/walkthroughs/132-palindrome-partitioning-ii.md)

</details>

<details>
<summary><b>14 · 2-D Dynamic Programming</b> — 0/21 ░░░░░░░░</summary>

Same engine, two indices: grids and sequence pairs.

[📖 Lesson](materials/learning/15-dp-2d.md)

$\color{#e67e22}{\textbf{Medium}}$

- [ ] ▰▱▱▱ [**62** Unique Paths](https://leetcode.com/problems/unique-paths/) · [Solution](problems/0001-0499/62.py) · [Walkthrough](materials/walkthroughs/62-unique-paths.md)
- [ ] ▰▰▰▱ [**63** Unique Paths II](https://leetcode.com/problems/unique-paths-ii/) · [Solution](problems/0001-0499/63.py) · [Walkthrough](materials/walkthroughs/63-unique-paths-ii.md)
- [ ] ▰▰▰▱ [**64** Minimum Path Sum](https://leetcode.com/problems/minimum-path-sum/) · [Solution](problems/0001-0499/64.py) · [Walkthrough](materials/walkthroughs/64-minimum-path-sum.md)
- [ ] ▰▰▰▰ [**120** Triangle](https://leetcode.com/problems/triangle/) · [Solution](problems/0001-0499/120.py) · [Walkthrough](materials/walkthroughs/120-triangle.md)
- [ ] ▰▰▰▰ [**931** Minimum Falling Path Sum](https://leetcode.com/problems/minimum-falling-path-sum/) · [Solution](problems/0500-0999/931.py) · [Walkthrough](materials/walkthroughs/931-minimum-falling-path-sum.md)
- [ ] ▰▰▰▰ [**221** Maximal Square](https://leetcode.com/problems/maximal-square/) · [Solution](problems/0001-0499/221.py) · [Walkthrough](materials/walkthroughs/221-maximal-square.md)
- [ ] ▰▱▱▱ [**1143** Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/) · [Solution](problems/1000-1499/1143.py) · [Walkthrough](materials/walkthroughs/1143-longest-common-subsequence.md)
- [ ] ▰▰▰▰ [**1035** Uncrossed Lines](https://leetcode.com/problems/uncrossed-lines/) · [Solution](problems/1000-1499/1035.py) · [Walkthrough](materials/walkthroughs/1035-uncrossed-lines.md)
- [ ] ▰▰▰▰ [**516** Longest Palindromic Subsequence](https://leetcode.com/problems/longest-palindromic-subsequence/) · [Solution](problems/0500-0999/516.py) · [Walkthrough](materials/walkthroughs/516-longest-palindromic-subsequence.md)
- [ ] ▰▰▱▱ [**494** Target Sum](https://leetcode.com/problems/target-sum/) · [Solution](problems/0001-0499/494.py) · [Walkthrough](materials/walkthroughs/494-target-sum.md)
- [ ] ▰▰▰▱ [**1049** Last Stone Weight II](https://leetcode.com/problems/last-stone-weight-ii/) · [Solution](problems/1000-1499/1049.py) · [Walkthrough](materials/walkthroughs/1049-last-stone-weight-ii.md)
- [ ] ▰▰▱▱ [**72** Edit Distance](https://leetcode.com/problems/edit-distance/) · [Solution](problems/0001-0499/72.py) · [Walkthrough](materials/walkthroughs/72-edit-distance.md)
- [ ] ▰▰▱▱ [**97** Interleaving String](https://leetcode.com/problems/interleaving-string/) · [Solution](problems/0001-0499/97.py) · [Walkthrough](materials/walkthroughs/97-interleaving-string.md)
- [ ] ▰▰▰▰ [**718** Maximum Length of Repeated Subarray](https://leetcode.com/problems/maximum-length-of-repeated-subarray/) · [Solution](problems/0500-0999/718.py) · [Walkthrough](materials/walkthroughs/718-maximum-length-of-repeated-subarray.md)

$\color{#cf222e}{\textbf{Hard}}$

- [ ] ▰▰▱▱ [**115** Distinct Subsequences](https://leetcode.com/problems/distinct-subsequences/) · [Solution](problems/0001-0499/115.py) · [Walkthrough](materials/walkthroughs/115-distinct-subsequences.md)
- [ ] ▰▰▱▱ [**312** Burst Balloons](https://leetcode.com/problems/burst-balloons/) · [Solution](problems/0001-0499/312.py) · [Walkthrough](materials/walkthroughs/312-burst-balloons.md)
- [ ] ▰▰▱▱ [**10** Regular Expression Matching](https://leetcode.com/problems/regular-expression-matching/) · [Solution](problems/0001-0499/10.py) · [Walkthrough](materials/walkthroughs/10-regular-expression-matching.md)
- [ ] ▰▰▱▱ [**329** Longest Increasing Path in a Matrix](https://leetcode.com/problems/longest-increasing-path-in-a-matrix/) · [Solution](problems/0001-0499/329.py) · [Walkthrough](materials/walkthroughs/329-longest-increasing-path-in-a-matrix.md)
- [ ] ▰▰▰▰ [**174** Dungeon Game](https://leetcode.com/problems/dungeon-game/) · [Solution](problems/0001-0499/174.py) · [Walkthrough](materials/walkthroughs/174-dungeon-game.md)
- [ ] ▰▰▰▰ [**123** Best Time to Buy and Sell Stock III](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iii/) · [Solution](problems/0001-0499/123.py) · [Walkthrough](materials/walkthroughs/123-best-time-to-buy-and-sell-stock-iii.md)
- [ ] ▰▰▰▰ [**188** Best Time to Buy and Sell Stock IV](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/) · [Solution](problems/0001-0499/188.py) · [Walkthrough](materials/walkthroughs/188-best-time-to-buy-and-sell-stock-iv.md)

</details>

<details>
<summary><b>15 · Greedy</b> — 0/14 ░░░░░░░░</summary>

Take the locally best choice; the proof is the hard part.

[📖 Lesson](materials/learning/16-greedy.md)

$\color{#2da44e}{\textbf{Easy}}$

- [ ] ▰▰▰▰ [**561** Array Partition](https://leetcode.com/problems/array-partition/) · [Solution](problems/0500-0999/561.py) · [Walkthrough](materials/walkthroughs/561-array-partition.md)
- [ ] ▰▰▰▰ [**1005** Maximize Sum Of Array After K Negations](https://leetcode.com/problems/maximize-sum-of-array-after-k-negations/) · [Solution](problems/1000-1499/1005.py) · [Walkthrough](materials/walkthroughs/1005-maximize-sum-of-array-after-k-negations.md)

$\color{#e67e22}{\textbf{Medium}}$

- [ ] ▰▱▱▱ [**53** Maximum Subarray](https://leetcode.com/problems/maximum-subarray/) · [Solution](problems/0001-0499/53.py) · [Walkthrough](materials/walkthroughs/53-maximum-subarray.md)
- [ ] ▰▱▱▱ [**55** Jump Game](https://leetcode.com/problems/jump-game/) · [Solution](problems/0001-0499/55.py) · [Walkthrough](materials/walkthroughs/55-jump-game.md)
- [ ] ▰▰▱▱ [**45** Jump Game II](https://leetcode.com/problems/jump-game-ii/) · [Solution](problems/0001-0499/45.py) · [Walkthrough](materials/walkthroughs/45-jump-game-ii.md)
- [ ] ▰▰▰▱ [**122** Best Time to Buy and Sell Stock II](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/) · [Solution](problems/0001-0499/122.py) · [Walkthrough](materials/walkthroughs/122-best-time-to-buy-and-sell-stock-ii.md)
- [ ] ▰▰▱▱ [**134** Gas Station](https://leetcode.com/problems/gas-station/) · [Solution](problems/0001-0499/134.py) · [Walkthrough](materials/walkthroughs/134-gas-station.md)
- [ ] ▰▰▱▱ [**846** Hand of Straights](https://leetcode.com/problems/hand-of-straights/) · [Solution](problems/0500-0999/846.py) · [Walkthrough](materials/walkthroughs/846-hand-of-straights.md)
- [ ] ▰▰▱▱ [**1899** Merge Triplets to Form Target Triplet](https://leetcode.com/problems/merge-triplets-to-form-target-triplet/) · [Solution](problems/1500-1999/1899.py) · [Walkthrough](materials/walkthroughs/1899-merge-triplets-to-form-target-triplet.md)
- [ ] ▰▰▱▱ [**763** Partition Labels](https://leetcode.com/problems/partition-labels/) · [Solution](problems/0500-0999/763.py) · [Walkthrough](materials/walkthroughs/763-partition-labels.md)
- [ ] ▰▰▱▱ [**678** Valid Parenthesis String](https://leetcode.com/problems/valid-parenthesis-string/) · [Solution](problems/0500-0999/678.py) · [Walkthrough](materials/walkthroughs/678-valid-parenthesis-string.md)
- [ ] ▰▰▰▰ [**1647** Minimum Deletions to Make Character Frequencies Unique](https://leetcode.com/problems/minimum-deletions-to-make-character-frequencies-unique/) · [Solution](problems/1500-1999/1647.py) · [Walkthrough](materials/walkthroughs/1647-minimum-deletions-to-make-character-frequencies-unique.md)
- [ ] ▰▰▰▰ [**738** Monotone Increasing Digits](https://leetcode.com/problems/monotone-increasing-digits/) · [Solution](problems/0500-0999/738.py) · [Walkthrough](materials/walkthroughs/738-monotone-increasing-digits.md)
- [ ] ▰▰▰▰ [**376** Wiggle Subsequence](https://leetcode.com/problems/wiggle-subsequence/) · [Solution](problems/0001-0499/376.py) · [Walkthrough](materials/walkthroughs/376-wiggle-subsequence.md)

</details>

<details>
<summary><b>16 · Intervals</b> — 0/10 ░░░░░░░░</summary>

Sort first, then one linear sweep to merge / count.

[📖 Lesson](materials/learning/17-intervals.md)

$\color{#2da44e}{\textbf{Easy}}$

- [ ] ▰▱▱▱ [**252** Meeting Rooms](https://leetcode.com/problems/meeting-rooms/) · [Solution](problems/0001-0499/252.py) · [Walkthrough](materials/walkthroughs/252-meeting-rooms.md)

$\color{#e67e22}{\textbf{Medium}}$

- [ ] ▰▱▱▱ [**56** Merge Intervals](https://leetcode.com/problems/merge-intervals/) · [Solution](problems/0001-0499/56.py) · [Walkthrough](materials/walkthroughs/56-merge-intervals.md)
- [ ] ▰▱▱▱ [**57** Insert Interval](https://leetcode.com/problems/insert-interval/) · [Solution](problems/0001-0499/57.py) · [Walkthrough](materials/walkthroughs/57-insert-interval.md)
- [ ] ▰▱▱▱ [**435** Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/) · [Solution](problems/0001-0499/435.py) · [Walkthrough](materials/walkthroughs/435-non-overlapping-intervals.md)
- [ ] ▰▱▱▱ [**253** Meeting Rooms II](https://leetcode.com/problems/meeting-rooms-ii/) · [Solution](problems/0001-0499/253.py) · [Walkthrough](materials/walkthroughs/253-meeting-rooms-ii.md)
- [ ] ▰▰▰▰ [**986** Interval List Intersections](https://leetcode.com/problems/interval-list-intersections/) · [Solution](problems/0500-0999/986.py) · [Walkthrough](materials/walkthroughs/986-interval-list-intersections.md)
- [ ] ▰▰▰▰ [**1288** Remove Covered Intervals](https://leetcode.com/problems/remove-covered-intervals/) · [Solution](problems/1000-1499/1288.py) · [Walkthrough](materials/walkthroughs/1288-remove-covered-intervals.md)
- [ ] ▰▰▰▰ [**452** Minimum Number of Arrows to Burst Balloons](https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/) · [Solution](problems/0001-0499/452.py) · [Walkthrough](materials/walkthroughs/452-minimum-number-of-arrows-to-burst-balloons.md)
- [ ] ▰▰▰▰ [**731** My Calendar II](https://leetcode.com/problems/my-calendar-ii/) · [Solution](problems/0500-0999/731.py) · [Walkthrough](materials/walkthroughs/731-my-calendar-ii.md)

$\color{#cf222e}{\textbf{Hard}}$

- [ ] ▰▰▱▱ [**1851** Minimum Interval to Include Each Query](https://leetcode.com/problems/minimum-interval-to-include-each-query/) · [Solution](problems/1500-1999/1851.py) · [Walkthrough](materials/walkthroughs/1851-minimum-interval-to-include-each-query.md)

</details>

<details>
<summary><b>17 · Math & Geometry</b> — 0/16 ░░░░░░░░</summary>

GCD, fast power, in-place matrix transforms.

[📖 Lesson](materials/learning/19-math-geometry.md)

$\color{#2da44e}{\textbf{Easy}}$

- [ ] ▰▰▰▰ [**9** Palindrome Number](https://leetcode.com/problems/palindrome-number/) · [Solution](problems/0001-0499/9.py) · [Walkthrough](materials/walkthroughs/9-palindrome-number.md)
- [ ] ▰▰▰▱ [**13** Roman to Integer](https://leetcode.com/problems/roman-to-integer/) · [Solution](problems/0001-0499/13.py) · [Walkthrough](materials/walkthroughs/13-roman-to-integer.md)
- [ ] ▰▰▱▱ [**202** Happy Number](https://leetcode.com/problems/happy-number/) · [Solution](problems/0001-0499/202.py) · [Walkthrough](materials/walkthroughs/202-happy-number.md)
- [ ] ▰▰▰▰ [**263** Ugly Number](https://leetcode.com/problems/ugly-number/) · [Solution](problems/0001-0499/263.py) · [Walkthrough](materials/walkthroughs/263-ugly-number.md)
- [ ] ▰▰▰▱ [**1071** Greatest Common Divisor of Strings](https://leetcode.com/problems/greatest-common-divisor-of-strings/) · [Solution](problems/1000-1499/1071.py) · [Walkthrough](materials/walkthroughs/1071-greatest-common-divisor-of-strings.md)
- [ ] ▰▰▰▰ [**415** Add Strings](https://leetcode.com/problems/add-strings/) · [Solution](problems/0001-0499/415.py) · [Walkthrough](materials/walkthroughs/415-add-strings.md)
- [ ] ▰▰▰▱ [**168** Excel Sheet Column Title](https://leetcode.com/problems/excel-sheet-column-title/) · [Solution](problems/0001-0499/168.py) · [Walkthrough](materials/walkthroughs/168-excel-sheet-column-title.md)

$\color{#e67e22}{\textbf{Medium}}$

- [ ] ▰▰▱▱ [**7** Reverse Integer](https://leetcode.com/problems/reverse-integer/) · [Solution](problems/0001-0499/7.py) · [Walkthrough](materials/walkthroughs/7-reverse-integer.md)
- [ ] ▰▰▰▰ [**12** Integer to Roman](https://leetcode.com/problems/integer-to-roman/) · [Solution](problems/0001-0499/12.py) · [Walkthrough](materials/walkthroughs/12-integer-to-roman.md)
- [ ] ▰▰▱▱ [**50** Pow(x, n)](https://leetcode.com/problems/powx-n/) · [Solution](problems/0001-0499/50.py) · [Walkthrough](materials/walkthroughs/50-pow-x-n.md)
- [ ] ▰▰▱▱ [**43** Multiply Strings](https://leetcode.com/problems/multiply-strings/) · [Solution](problems/0001-0499/43.py) · [Walkthrough](materials/walkthroughs/43-multiply-strings.md)
- [ ] ▰▱▱▱ [**73** Set Matrix Zeroes](https://leetcode.com/problems/set-matrix-zeroes/) · [Solution](problems/0001-0499/73.py) · [Walkthrough](materials/walkthroughs/73-set-matrix-zeroes.md)
- [ ] ▰▱▱▱ [**54** Spiral Matrix](https://leetcode.com/problems/spiral-matrix/) · [Solution](problems/0001-0499/54.py) · [Walkthrough](materials/walkthroughs/54-spiral-matrix.md)
- [ ] ▰▱▱▱ [**48** Rotate Image](https://leetcode.com/problems/rotate-image/) · [Solution](problems/0001-0499/48.py) · [Walkthrough](materials/walkthroughs/48-rotate-image.md)
- [ ] ▰▰▱▱ [**2013** Detect Squares](https://leetcode.com/problems/detect-squares/) · [Solution](problems/2000-2499/2013.py) · [Walkthrough](materials/walkthroughs/2013-detect-squares.md)

$\color{#cf222e}{\textbf{Hard}}$

- [ ] ▰▰▰▰ [**149** Max Points on a Line](https://leetcode.com/problems/max-points-on-a-line/) · [Solution](problems/0001-0499/149.py) · [Walkthrough](materials/walkthroughs/149-max-points-on-a-line.md)

</details>

<details>
<summary><b>18 · Bit Manipulation</b> — 0/13 ░░░░░░░░</summary>

Masks, shifts, and XOR cancellation in O(1).

[📖 Lesson](materials/learning/18-bit-manipulation.md)

$\color{#2da44e}{\textbf{Easy}}$

- [ ] ▰▰▱▱ [**136** Single Number](https://leetcode.com/problems/single-number/) · [Solution](problems/0001-0499/136.py) · [Walkthrough](materials/walkthroughs/136-single-number.md)
- [ ] ▰▱▱▱ [**191** Number of 1 Bits](https://leetcode.com/problems/number-of-1-bits/) · [Solution](problems/0001-0499/191.py) · [Walkthrough](materials/walkthroughs/191-number-of-1-bits.md)
- [ ] ▰▱▱▱ [**338** Counting Bits](https://leetcode.com/problems/counting-bits/) · [Solution](problems/0001-0499/338.py) · [Walkthrough](materials/walkthroughs/338-counting-bits.md)
- [ ] ▰▱▱▱ [**190** Reverse Bits](https://leetcode.com/problems/reverse-bits/) · [Solution](problems/0001-0499/190.py) · [Walkthrough](materials/walkthroughs/190-reverse-bits.md)
- [ ] ▰▰▰▱ [**67** Add Binary](https://leetcode.com/problems/add-binary/) · [Solution](problems/0001-0499/67.py) · [Walkthrough](materials/walkthroughs/67-add-binary.md)
- [ ] ▰▰▰▰ [**461** Hamming Distance](https://leetcode.com/problems/hamming-distance/) · [Solution](problems/0001-0499/461.py) · [Walkthrough](materials/walkthroughs/461-hamming-distance.md)

$\color{#e67e22}{\textbf{Medium}}$

- [ ] ▰▱▱▱ [**371** Sum of Two Integers](https://leetcode.com/problems/sum-of-two-integers/) · [Solution](problems/0001-0499/371.py) · [Walkthrough](materials/walkthroughs/371-sum-of-two-integers.md)
- [ ] ▰▰▰▰ [**137** Single Number II](https://leetcode.com/problems/single-number-ii/) · [Solution](problems/0001-0499/137.py) · [Walkthrough](materials/walkthroughs/137-single-number-ii.md)
- [ ] ▰▰▰▰ [**260** Single Number III](https://leetcode.com/problems/single-number-iii/) · [Solution](problems/0001-0499/260.py) · [Walkthrough](materials/walkthroughs/260-single-number-iii.md)
- [ ] ▰▰▰▱ [**201** Bitwise AND of Numbers Range](https://leetcode.com/problems/bitwise-and-of-numbers-range/) · [Solution](problems/0001-0499/201.py) · [Walkthrough](materials/walkthroughs/201-bitwise-and-of-numbers-range.md)
- [ ] ▰▰▰▰ [**318** Maximum Product of Word Lengths](https://leetcode.com/problems/maximum-product-of-word-lengths/) · [Solution](problems/0001-0499/318.py) · [Walkthrough](materials/walkthroughs/318-maximum-product-of-word-lengths.md)
- [ ] ▰▰▰▰ [**1318** Minimum Flips to Make a OR b Equal to c](https://leetcode.com/problems/minimum-flips-to-make-a-or-b-equal-to-c/) · [Solution](problems/1000-1499/1318.py) · [Walkthrough](materials/walkthroughs/1318-minimum-flips-to-make-a-or-b-equal-to-c.md)
- [ ] ▰▰▰▰ [**89** Gray Code](https://leetcode.com/problems/gray-code/) · [Solution](problems/0001-0499/89.py) · [Walkthrough](materials/walkthroughs/89-gray-code.md)

</details>

<details>

<summary><b>19 · SQL</b> — 0/56 ░░░░░░░░</summary>

[📖 SQL syntax](materials/sql/_index.md)
[📋 SQL list](lists/other/sql.md)

<details>

<summary><b>Phase 1 · Basic SELECT</b> — 0/5 ░░░░░░░░</summary>

`SELECT`, `WHERE`, `DISTINCT`, `LIKE`, `IS NULL`. Get comfortable reading a table and filtering rows.

$\color{#2da44e}{\textbf{Easy}}$

- [ ] [**1757** Recyclable and Low Fat Products](https://leetcode.com/problems/recyclable-and-low-fat-products/) · [Solution](problems/1500-1999/1757.sql) · [Walkthrough](materials/walkthroughs/1757-recyclable-and-low-fat-products.md)
- [ ] [**584** Find Customer Referee](https://leetcode.com/problems/find-customer-referee/) · [Solution](problems/0500-0999/584.sql) · [Walkthrough](materials/walkthroughs/584-find-customer-referee.md)
- [ ] [**595** Big Countries](https://leetcode.com/problems/big-countries/) · [Solution](problems/0500-0999/595.sql) · [Walkthrough](materials/walkthroughs/595-big-countries.md)
- [ ] [**1148** Article Views I](https://leetcode.com/problems/article-views-i/) · [Solution](problems/1000-1499/1148.sql) · [Walkthrough](materials/walkthroughs/1148-article-views-i.md)
- [ ] [**1683** Invalid Tweets](https://leetcode.com/problems/invalid-tweets/) · [Solution](problems/1500-1999/1683.sql) · [Walkthrough](materials/walkthroughs/1683-invalid-tweets.md)

</details>

<details>
<summary><b>Phase 2 · Joins</b> — 0/9 ░░░░░░░░</summary>

`INNER JOIN`, `LEFT JOIN`, self-joins, and the anti-join (`LEFT JOIN ... WHERE x IS NULL`).

$\color{#2da44e}{\textbf{Easy}}$

- [ ] [**1378** Replace Employee ID With The Unique Identifier](https://leetcode.com/problems/replace-employee-id-with-the-unique-identifier/) · [Solution](problems/1000-1499/1378.sql) · [Walkthrough](materials/walkthroughs/1378-replace-employee-id-with-the-unique-identifier.md)
- [ ] [**1068** Product Sales Analysis I](https://leetcode.com/problems/product-sales-analysis-i/) · [Solution](problems/1000-1499/1068.sql) · [Walkthrough](materials/walkthroughs/1068-product-sales-analysis-i.md)
- [ ] [**1581** Customer Who Visited but Did Not Make Any Transactions](https://leetcode.com/problems/customer-who-visited-but-did-not-make-any-transactions/) · [Solution](problems/1500-1999/1581.sql) · [Walkthrough](materials/walkthroughs/1581-customer-who-visited-but-did-not-make-any-transactions.md)
- [ ] [**197** Rising Temperature](https://leetcode.com/problems/rising-temperature/) · [Solution](problems/0001-0499/197.sql) · [Walkthrough](materials/walkthroughs/197-rising-temperature.md)
- [ ] [**1661** Average Time of Process per Machine](https://leetcode.com/problems/average-time-of-process-per-machine/) · [Solution](problems/1500-1999/1661.sql) · [Walkthrough](materials/walkthroughs/1661-average-time-of-process-per-machine.md)
- [ ] [**577** Employee Bonus](https://leetcode.com/problems/employee-bonus/) · [Solution](problems/0500-0999/577.sql) · [Walkthrough](materials/walkthroughs/577-employee-bonus.md)
- [ ] [**1280** Students and Examinations](https://leetcode.com/problems/students-and-examinations/) · [Solution](problems/1000-1499/1280.sql) · [Walkthrough](materials/walkthroughs/1280-students-and-examinations.md)

$\color{#e67e22}{\textbf{Medium}}$

- [ ] [**570** Managers with at Least 5 Direct Reports](https://leetcode.com/problems/managers-with-at-least-5-direct-reports/) · [Solution](problems/0500-0999/570.sql) · [Walkthrough](materials/walkthroughs/570-managers-with-at-least-5-direct-reports.md)
- [ ] [**1934** Confirmation Rate](https://leetcode.com/problems/confirmation-rate/) · [Solution](problems/1500-1999/1934.sql) · [Walkthrough](materials/walkthroughs/1934-confirmation-rate.md)

</details>

<details>
<summary><b>Phase 3 · Aggregate Functions</b> — 0/8 ░░░░░░░░</summary>

`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, `GROUP BY`, `HAVING`. `WHERE` filters rows before grouping; `HAVING` filters groups after.

$\color{#2da44e}{\textbf{Easy}}$

- [ ] [**620** Not Boring Movies](https://leetcode.com/problems/not-boring-movies/) · [Solution](problems/0500-0999/620.sql) · [Walkthrough](materials/walkthroughs/620-not-boring-movies.md)
- [ ] [**1251** Average Selling Price](https://leetcode.com/problems/average-selling-price/) · [Solution](problems/1000-1499/1251.sql) · [Walkthrough](materials/walkthroughs/1251-average-selling-price.md)
- [ ] [**1075** Project Employees I](https://leetcode.com/problems/project-employees-i/) · [Solution](problems/1000-1499/1075.sql) · [Walkthrough](materials/walkthroughs/1075-project-employees-i.md)
- [ ] [**1633** Percentage of Users Attended a Contest](https://leetcode.com/problems/percentage-of-users-attended-a-contest/) · [Solution](problems/1500-1999/1633.sql) · [Walkthrough](materials/walkthroughs/1633-percentage-of-users-attended-a-contest.md)
- [ ] [**1211** Queries Quality and Percentage](https://leetcode.com/problems/queries-quality-and-percentage/) · [Solution](problems/1000-1499/1211.sql) · [Walkthrough](materials/walkthroughs/1211-queries-quality-and-percentage.md)

$\color{#e67e22}{\textbf{Medium}}$

- [ ] [**1193** Monthly Transactions I](https://leetcode.com/problems/monthly-transactions-i/) · [Solution](problems/1000-1499/1193.sql) · [Walkthrough](materials/walkthroughs/1193-monthly-transactions-i.md)
- [ ] [**1174** Immediate Food Delivery II](https://leetcode.com/problems/immediate-food-delivery-ii/) · [Solution](problems/1000-1499/1174.sql) · [Walkthrough](materials/walkthroughs/1174-immediate-food-delivery-ii.md)
- [ ] [**550** Game Play Analysis IV](https://leetcode.com/problems/game-play-analysis-iv/) · [Solution](problems/0500-0999/550.sql) · [Walkthrough](materials/walkthroughs/550-game-play-analysis-iv.md)

</details>

<details>
<summary><b>Phase 4 · Sorting and Grouping</b> — 0/7 ░░░░░░░░</summary>

`ORDER BY`, `GROUP BY` with `DISTINCT` counts, and grouping conditions.

$\color{#2da44e}{\textbf{Easy}}$

- [ ] [**2356** Number of Unique Subjects Taught by Each Teacher](https://leetcode.com/problems/number-of-unique-subjects-taught-by-each-teacher/) · [Solution](problems/2000-2499/2356.sql) · [Walkthrough](materials/walkthroughs/2356-number-of-unique-subjects-taught-by-each-teacher.md)
- [ ] [**1141** User Activity for the Past 30 Days I](https://leetcode.com/problems/user-activity-for-the-past-30-days-i/) · [Solution](problems/1000-1499/1141.sql) · [Walkthrough](materials/walkthroughs/1141-user-activity-for-the-past-30-days-i.md)

$\color{#e67e22}{\textbf{Medium}}$

- [ ] [**1070** Product Sales Analysis III](https://leetcode.com/problems/product-sales-analysis-iii/) · [Solution](problems/1000-1499/1070.sql) · [Walkthrough](materials/walkthroughs/1070-product-sales-analysis-iii.md)

$\color{#2da44e}{\textbf{Easy}}$

- [ ] [**596** Classes With at Least 5 Students](https://leetcode.com/problems/classes-with-at-least-5-students/) · [Solution](problems/0500-0999/596.sql) · [Walkthrough](materials/walkthroughs/596-classes-with-at-least-5-students.md)
- [ ] [**1729** Find Followers Count](https://leetcode.com/problems/find-followers-count/) · [Solution](problems/1500-1999/1729.sql) · [Walkthrough](materials/walkthroughs/1729-find-followers-count.md)
- [ ] [**619** Biggest Single Number](https://leetcode.com/problems/biggest-single-number/) · [Solution](problems/0500-0999/619.sql) · [Walkthrough](materials/walkthroughs/619-biggest-single-number.md)

$\color{#e67e22}{\textbf{Medium}}$

- [ ] [**1045** Customers Who Bought All Products](https://leetcode.com/problems/customers-who-bought-all-products/) · [Solution](problems/1000-1499/1045.sql) · [Walkthrough](materials/walkthroughs/1045-customers-who-bought-all-products.md)

</details>

<details>
<summary><b>Phase 5 · Advanced Select and Joins</b> — 0/7 ░░░░░░░░</summary>

Self-joins, `CASE WHEN`, `UNION`, gap and consecutive detection, and last-value-as-of-date lookups.

$\color{#2da44e}{\textbf{Easy}}$

- [ ] [**1731** The Number of Employees Which Report to Each Employee](https://leetcode.com/problems/the-number-of-employees-which-report-to-each-employee/) · [Solution](problems/1500-1999/1731.sql) · [Walkthrough](materials/walkthroughs/1731-the-number-of-employees-which-report-to-each-employee.md)
- [ ] [**1789** Primary Department for Each Employee](https://leetcode.com/problems/primary-department-for-each-employee/) · [Solution](problems/1500-1999/1789.sql) · [Walkthrough](materials/walkthroughs/1789-primary-department-for-each-employee.md)
- [ ] [**610** Triangle Judgement](https://leetcode.com/problems/triangle-judgement/) · [Solution](problems/0500-0999/610.sql) · [Walkthrough](materials/walkthroughs/610-triangle-judgement.md)

$\color{#e67e22}{\textbf{Medium}}$

- [ ] [**180** Consecutive Numbers](https://leetcode.com/problems/consecutive-numbers/) · [Solution](problems/0001-0499/180.sql) · [Walkthrough](materials/walkthroughs/180-consecutive-numbers.md)
- [ ] [**1164** Product Price at a Given Date](https://leetcode.com/problems/product-price-at-a-given-date/) · [Solution](problems/1000-1499/1164.sql) · [Walkthrough](materials/walkthroughs/1164-product-price-at-a-given-date.md)
- [ ] [**1204** Last Person to Fit in the Bus](https://leetcode.com/problems/last-person-to-fit-in-the-bus/) · [Solution](problems/1000-1499/1204.sql) · [Walkthrough](materials/walkthroughs/1204-last-person-to-fit-in-the-bus.md)
- [ ] [**1907** Count Salary Categories](https://leetcode.com/problems/count-salary-categories/) · [Solution](problems/1500-1999/1907.sql) · [Walkthrough](materials/walkthroughs/1907-count-salary-categories.md)

</details>

<details>
<summary><b>Phase 6 · Subqueries and Window Functions</b> — 0/7 ░░░░░░░░</summary>

Subqueries in `WHERE` and `FROM`, CTEs, `ROW_NUMBER`, `RANK`, `DENSE_RANK`, `LAG`, running totals with `SUM() OVER`.

$\color{#2da44e}{\textbf{Easy}}$

- [ ] [**1978** Employees Whose Manager Left the Company](https://leetcode.com/problems/employees-whose-manager-left-the-company/) · [Solution](problems/1500-1999/1978.sql) · [Walkthrough](materials/walkthroughs/1978-employees-whose-manager-left-the-company.md)

$\color{#e67e22}{\textbf{Medium}}$

- [ ] [**626** Exchange Seats](https://leetcode.com/problems/exchange-seats/) · [Solution](problems/0500-0999/626.sql) · [Walkthrough](materials/walkthroughs/626-exchange-seats.md)
- [ ] [**1341** Movie Rating](https://leetcode.com/problems/movie-rating/) · [Solution](problems/1000-1499/1341.sql) · [Walkthrough](materials/walkthroughs/1341-movie-rating.md)
- [ ] [**1321** Restaurant Growth](https://leetcode.com/problems/restaurant-growth/) · [Solution](problems/1000-1499/1321.sql) · [Walkthrough](materials/walkthroughs/1321-restaurant-growth.md)
- [ ] [**602** Friend Requests II: Who Has the Most Friends](https://leetcode.com/problems/friend-requests-ii-who-has-the-most-friends/) · [Solution](problems/0500-0999/602.sql) · [Walkthrough](materials/walkthroughs/602-friend-requests-ii-who-has-the-most-friends.md)
- [ ] [**585** Investments in 2016](https://leetcode.com/problems/investments-in-2016/) · [Solution](problems/0500-0999/585.sql) · [Walkthrough](materials/walkthroughs/585-investments-in-2016.md)

$\color{#cf222e}{\textbf{Hard}}$

- [ ] [**185** Department Top Three Salaries](https://leetcode.com/problems/department-top-three-salaries/) · [Solution](problems/0001-0499/185.sql) · [Walkthrough](materials/walkthroughs/185-department-top-three-salaries.md)

</details>

<details>
<summary><b>Phase 7 · Strings and Cleanup</b> — 0/7 ░░░░░░░░</summary>

String functions, `LIKE`/`REGEXP`, `DELETE`, `GROUP_CONCAT`, and `LIMIT`/`OFFSET` tricks.

$\color{#2da44e}{\textbf{Easy}}$

- [ ] [**1667** Fix Names in a Table](https://leetcode.com/problems/fix-names-in-a-table/) · [Solution](problems/1500-1999/1667.sql) · [Walkthrough](materials/walkthroughs/1667-fix-names-in-a-table.md)
- [ ] [**1527** Patients With a Condition](https://leetcode.com/problems/patients-with-a-condition/) · [Solution](problems/1500-1999/1527.sql) · [Walkthrough](materials/walkthroughs/1527-patients-with-a-condition.md)
- [ ] [**196** Delete Duplicate Emails](https://leetcode.com/problems/delete-duplicate-emails/) · [Solution](problems/0001-0499/196.sql) · [Walkthrough](materials/walkthroughs/196-delete-duplicate-emails.md)

$\color{#e67e22}{\textbf{Medium}}$

- [ ] [**176** Second Highest Salary](https://leetcode.com/problems/second-highest-salary/) · [Solution](problems/0001-0499/176.sql) · [Walkthrough](materials/walkthroughs/176-second-highest-salary.md)

$\color{#2da44e}{\textbf{Easy}}$

- [ ] [**1484** Group Sold Products By The Date](https://leetcode.com/problems/group-sold-products-by-the-date/) · [Solution](problems/1000-1499/1484.sql) · [Walkthrough](materials/walkthroughs/1484-group-sold-products-by-the-date.md)
- [ ] [**1327** List the Products Ordered in a Period](https://leetcode.com/problems/list-the-products-ordered-in-a-period/) · [Solution](problems/1000-1499/1327.sql) · [Walkthrough](materials/walkthroughs/1327-list-the-products-ordered-in-a-period.md)
- [ ] [**1517** Find Users With Valid E-Mails](https://leetcode.com/problems/find-users-with-valid-e-mails/) · [Solution](problems/1500-1999/1517.sql) · [Walkthrough](materials/walkthroughs/1517-find-users-with-valid-e-mails.md)

</details>

<details>
<summary><b>Phase 8 · Bonus: Common OA Problems</b> — 0/6 ░░░░░░░░</summary>

Not in the SQL 50, but they show up again and again in online assessments. Do these after the 50.

$\color{#e67e22}{\textbf{Medium}}$

- [ ] [**178** Rank Scores](https://leetcode.com/problems/rank-scores/) · [Solution](problems/0001-0499/178.sql) · [Walkthrough](materials/walkthroughs/178-rank-scores.md)
- [ ] [**184** Department Highest Salary](https://leetcode.com/problems/department-highest-salary/) · [Solution](problems/0001-0499/184.sql) · [Walkthrough](materials/walkthroughs/184-department-highest-salary.md)
- [ ] [**177** Nth Highest Salary](https://leetcode.com/problems/nth-highest-salary/) · [Solution](problems/0001-0499/177.sql) · [Walkthrough](materials/walkthroughs/177-nth-highest-salary.md)

$\color{#cf222e}{\textbf{Hard}}$

- [ ] [**262** Trips and Users](https://leetcode.com/problems/trips-and-users/) · [Solution](problems/0001-0499/262.sql) · [Walkthrough](materials/walkthroughs/262-trips-and-users.md)

$\color{#e67e22}{\textbf{Medium}}$

- [ ] [**1393** Capital Gain/Loss](https://leetcode.com/problems/capital-gainloss/) · [Solution](problems/1000-1499/1393.sql) · [Walkthrough](materials/walkthroughs/1393-capital-gainloss.md)
- [ ] [**1158** Market Analysis I](https://leetcode.com/problems/market-analysis-i/) · [Solution](problems/1000-1499/1158.sql) · [Walkthrough](materials/walkthroughs/1158-market-analysis-i.md)

</details>

<details>
<summary><b>Patterns to know cold</b> — review before an OA</summary>

- **Top-N per group:** `DENSE_RANK() OVER (PARTITION BY ... ORDER BY ...)`
- **"Customers who never...":** `LEFT JOIN ... WHERE x IS NULL`
- **Running total:** `SUM(...) OVER (ORDER BY ...)`
- **Consecutive / gap detection:** `LAG`/`LEAD`, or a self-join on `id + 1`
- **Compare to a neighbor row or manager:** self-join
- **Conditional counts:** `SUM(CASE WHEN ... THEN 1 ELSE 0 END)`

</details>

</details>

## Leetcode Contests → [leetcode.com/contest](https://leetcode.com/contest/)
