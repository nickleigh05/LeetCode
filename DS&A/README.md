# Data Structures & Algorithms Guide

Welcome to the comprehensive DS&A guide! This directory contains detailed documentation for all major data structures and algorithms topics, complete with visual representations, examples, and implementations.

## Table of Contents

### Data Structures

1. **[Arrays & Hashing](01-arrays-and-hashing.md)**
   - Array fundamentals and operations
   - Hash tables, hash maps, and hash sets
   - Collision handling and time complexity
   - Common patterns: frequency counting, two sum, deduplication

2. **[Stack](04-stack.md)**
   - LIFO principle and operations
   - Monotonic stack patterns
   - Applications: balanced parentheses, next greater element
   - Min stack, largest rectangle in histogram

3. **[Linked List](06-linked-list.md)**
   - Singly, doubly, and circular linked lists
   - Common operations and patterns
   - Fast & slow pointer technique
   - Cycle detection, reversal, merge sorted lists

4. **[Trees](07-trees.md)**
   - Binary trees and binary search trees
   - Tree traversals: inorder, preorder, postorder, level-order
   - BST operations and validation
   - Common problems: LCA, path sum, serialize/deserialize

5. **[Tries](08-tries.md)**
   - Prefix tree structure and operations
   - Word search and autocomplete
   - Pattern matching applications
   - Time/space complexity analysis

6. **[Heap / Priority Queue](09-heap-priority-queue.md)**
   - Min heap and max heap
   - Heapify operations
   - Top K problems, merge K sorted lists
   - Running median, task scheduler

### Algorithmic Techniques

7. **[Two Pointers](02-two-pointers.md)**
   - Opposite direction (collision)
   - Same direction (fast & slow)
   - Applications: palindromes, two sum II, container with most water
   - Linked list problems with two pointers

8. **[Sliding Window](03-sliding-window.md)**
   - Fixed size windows
   - Variable size windows
   - Maximum/minimum in subarray
   - Longest substring without repeating characters

9. **[Binary Search](05-binary-search.md)**
   - Search in sorted arrays
   - Find first/last occurrence
   - Search in rotated arrays
   - Binary search on answer space

10. **[Backtracking](10-backtracking.md)**
    - Core backtracking template
    - Subsets, permutations, combinations
    - N-Queens, Sudoku solver
    - Pruning and optimization

11. **[Graphs](11-graphs.md)**
    - Graph representations
    - DFS and BFS traversals
    - Cycle detection and topological sort
    - Connected components and bipartite graphs

12. **[Advanced Graphs](12-advanced-graphs.md)**
    - Dijkstra's shortest path algorithm
    - Bellman-Ford and Floyd-Warshall
    - Minimum spanning trees (Kruskal, Prim)
    - Union-Find data structure

13. **[1-D Dynamic Programming](13-1d-dynamic-programming.md)**
    - Top-down vs bottom-up approaches
    - Classic problems: Fibonacci, climbing stairs, house robber
    - Coin change, longest increasing subsequence
    - Word break, decode ways

14. **[2-D Dynamic Programming](14-2d-dynamic-programming.md)**
    - 2D DP table visualization
    - Unique paths, longest common subsequence
    - Edit distance, minimum path sum
    - Space optimization techniques

15. **[Greedy Algorithms](15-greedy.md)**
    - Greedy choice property
    - Jump game, gas station
    - Meeting rooms, partition labels
    - Stock trading problems

16. **[Intervals](16-intervals.md)**
    - Merge and insert intervals
    - Non-overlapping intervals
    - Meeting rooms I & II
    - Interval intersections

### Mathematical & Bit Operations

17. **[Math & Geometry](17-math-geometry.md)**
    - Number theory: primes, GCD, LCM
    - Combinatorics and Pascal's triangle
    - Geometry: points, lines, rectangles
    - Distance calculations and rotations

18. **[Bit Manipulation](18-bit-manipulation.md)**
    - Binary representation and bitwise operators
    - Common bit tricks and patterns
    - Single number, missing number
    - Counting bits, Hamming distance

## How to Use This Guide

Each topic includes:
- **Visual Representations**: ASCII art diagrams to illustrate concepts
- **Clear Explanations**: Step-by-step breakdowns of algorithms and data structures
- **Examples**: Multiple problem examples with visual execution traces
- **Complexity Analysis**: Time and space complexity for all operations
- **Python Implementation**: Well-commented code with proper structure
- **Common Patterns**: When and how to apply each technique
- **Key Takeaways**: Summary for quick reference

## Quick Reference

### Time Complexity Cheat Sheet

| Data Structure | Access | Search | Insert | Delete |
|---------------|--------|--------|--------|--------|
| Array         | O(1)   | O(n)   | O(n)   | O(n)   |
| Stack         | O(n)   | O(n)   | O(1)   | O(1)   |
| Queue         | O(n)   | O(n)   | O(1)   | O(1)   |
| Linked List   | O(n)   | O(n)   | O(1)   | O(1)   |
| Hash Table    | N/A    | O(1)   | O(1)   | O(1)   |
| Binary Tree   | O(n)   | O(n)   | O(n)   | O(n)   |
| BST (balanced)| O(log n)| O(log n)| O(log n)| O(log n)|
| Heap          | N/A    | O(n)   | O(log n)| O(log n)|
| Trie          | O(k)   | O(k)   | O(k)   | O(k)   |

*k = length of string/key*

### Algorithm Patterns

```
Problem Type → Consider These Approaches:

Sorted Array → Binary Search, Two Pointers
Unsorted Array → Hash Map, Sorting first
Subarray/Substring → Sliding Window, Prefix Sum
Tree → DFS (recursion), BFS (queue), Divide & Conquer
Graph → DFS, BFS, Union-Find, Topological Sort
Optimization → Dynamic Programming, Greedy
Choices/Decisions → Backtracking, DFS
Intervals → Sorting + Greedy/DP
Top K → Heap/Priority Queue
Frequency → Hash Map
Fast Lookup → Hash Set/Map
Pairs with Target → Two Pointers, Hash Map
```

### Common Patterns Visual Guide

```
Two Pointers:
L                           R
↓                           ↓
┌───┬───┬───┬───┬───┬───┬───┐
│ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │
└───┴───┴───┴───┴───┴───┴───┘

Sliding Window:
    L           R
    ↓           ↓
┌───┬───┬───┬───┬───┬───┬───┐
│ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │
└───┴───┴───┴───┴───┴───┴───┘
    └───────────┘ window

Fast & Slow:
    S       F
    ↓       ↓
[1]→[2]→[3]→[4]→[5]→null

Binary Search:
L       M       R
↓       ↓       ↓
┌───┬───┬───┬───┬───┐
│ 1 │ 3 │ 5 │ 7 │ 9 │
└───┴───┴───┴───┴───┘
```

## Study Tips

1. **Understand Fundamentals**: Master basic data structures before advanced algorithms
2. **Draw It Out**: Use diagrams to visualize how algorithms work
3. **Practice Regularly**: Solve problems to reinforce concepts
4. **Analyze Complexity**: Always consider time and space trade-offs
5. **Recognize Patterns**: Learn to identify which technique fits which problem type
6. **Code It**: Implement algorithms from scratch to truly understand them

## Additional Resources

- Practice problems in the `/NeetCode150` directory
- Each topic includes Python implementation examples
- Visual representations help cement understanding
- Complexity analysis for all operations

## Progress Tracking

Use this guide alongside the NeetCode150 problem set to:
- Learn theoretical concepts
- See visual representations
- Understand time/space complexity
- Practice with real problems
- Build intuition for pattern recognition

Happy Learning!
