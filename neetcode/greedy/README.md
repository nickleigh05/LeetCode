# Greedy

## 15. Greedy (8 problems)

| Problem # | Difficulty | Problem Name | LeetCode Link |
|-----------|------------|--------------|---------------|
| 53 | Medium | Maximum Subarray | [Link](https://leetcode.com/problems/maximum-subarray/) |
| 55 | Medium | Jump Game | [Link](https://leetcode.com/problems/jump-game/) |
| 45 | Medium | Jump Game II | [Link](https://leetcode.com/problems/jump-game-ii/) |
| 134 | Medium | Gas Station | [Link](https://leetcode.com/problems/gas-station/) |
| 846 | Medium | Hand of Straights | [Link](https://leetcode.com/problems/hand-of-straights/) |
| 1899 | Medium | Merge Triplets to Form Target Triplet | [Link](https://leetcode.com/problems/merge-triplets-to-form-target-triplet/) |
| 763 | Medium | Partition Labels | [Link](https://leetcode.com/problems/partition-labels/) |
| 678 | Medium | Valid Parenthesis String | [Link](https://leetcode.com/problems/valid-parenthesis-string/) |

---

## Data Structures

### No special data structure
Greedy algorithms typically work with simple variables (a running max, a counter, a range). The key insight is that a locally optimal choice at each step leads to a globally optimal solution. This is not always true — proving it requires identifying the greedy invariant.

### Sorted Order / Min-Heap
Some greedy problems require sorting first or processing in a specific order. Used in Hand of Straights (sort card values) and Gas Station (find the optimal starting point).

---

## Core Patterns

### Kadane's Algorithm (Maximum Subarray)
Track the maximum subarray sum ending at the current position. `curr = max(nums[i], curr + nums[i])` — reset to the current element alone if the running sum goes negative (a negative prefix only hurts). Update the global best each step.

### Greedy Reachability (Jump Game)
Track the farthest index reachable so far. For each position, update `max_reach = max(max_reach, i + nums[i])`. If you ever reach a position `i > max_reach`, you're stuck. For Jump Game II, count jumps only when you're forced to jump (you've exhausted the current jump's reach).

### Circular Array — Find Valid Start (Gas Station)
If the total gas ≥ total cost, a valid start always exists. Find it by scanning left to right: whenever your running tank goes negative, reset the tank to 0 and move the candidate start to the next station.

### Sort + Greedy Processing (Hand of Straights)
Sort the cards. Use a frequency map. For the smallest available card, try to form a consecutive group of size `k` starting from it. If any card in the group is missing, return false. Process from smallest to largest to ensure each group starts at the right place.

### Last Occurrence Map (Partition Labels)
Record the last index where each character appears. Scan left to right, extending the current partition's end to `max(end, last[char])`. When you reach `i == end`, the current partition is complete — cut here.

### Track Range of Possibilities (Valid Parenthesis String)
Instead of trying all possibilities, track the range `[min_open, max_open]` — the minimum and maximum number of open parentheses that are valid at each step. `*` can be `(`, `)`, or empty, so it shifts the range. If `max_open < 0` at any point, it's invalid. At the end, check if `min_open == 0`.
