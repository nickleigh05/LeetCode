# Arrays & Hashing

## 1. Arrays & Hashing (9 problems)

| Problem # | Difficulty | Problem Name | LeetCode Link |
|-----------|------------|--------------|---------------|
| 217 | Easy | Contains Duplicate | [Link](https://leetcode.com/problems/contains-duplicate/) |
| 242 | Easy | Valid Anagram | [Link](https://leetcode.com/problems/valid-anagram/) |
| 1 | Easy | Two Sum | [Link](https://leetcode.com/problems/two-sum/) |
| 49 | Medium | Group Anagrams | [Link](https://leetcode.com/problems/group-anagrams/) |
| 347 | Medium | Top K Frequent Elements | [Link](https://leetcode.com/problems/top-k-frequent-elements/) |
| 238 | Medium | Product of Array Except Self | [Link](https://leetcode.com/problems/product-of-array-except-self/) |
| 36 | Medium | Valid Sudoku | [Link](https://leetcode.com/problems/valid-sudoku/) |
| 271 | Medium | Encode and Decode Strings | [Link](https://leetcode.com/problems/encode-and-decode-strings/) |
| 128 | Medium | Longest Consecutive Sequence | [Link](https://leetcode.com/problems/longest-consecutive-sequence/) |

---

## Data Structures

### Array
A contiguous block of memory where elements are stored at indexed positions. Accessing any element by index is O(1), but inserting or deleting in the middle is O(n) because elements must shift. Most problems in this category give you an array and ask you to find something about its values.

### Hash Table (dict / set)
Stores key-value pairs using a hash function to map keys to buckets. Average O(1) for insert, delete, and lookup. A **hash set** is just a hash table where you only care about the keys (used for membership checks). A **hash map** stores values alongside keys (used for counting, grouping, or looking up).

---

## Core Patterns

### Frequency Counting
Build a hash map of `value → count`. Lets you answer "how many times does X appear?" in O(1) after an O(n) setup pass. Used in Valid Anagram, Top K Frequent Elements, Group Anagrams.

### Seen-Before Check
Add elements to a hash set as you iterate. Before adding, check if it's already there — if yes, you found a duplicate or a complement. Used in Contains Duplicate, Two Sum.

### Complement Lookup (Two Sum Pattern)
For each element `x`, check if `target - x` is already in a hash map. Store `x → index` as you go so you can retrieve the index later. Turns an O(n²) brute force into O(n).

### Prefix Products
To get the product of all elements except index `i`, compute a left-product array and a right-product array, then multiply them. Avoids division and handles zeros. Used in Product of Array Except Self.

### Grouping by Key
Normalize elements to a canonical key (e.g. sort the characters of a string), then group all elements sharing that key in a hash map. Used in Group Anagrams.

### Bucket Sort / Counting Sort
When values are bounded, use an array indexed by value as a frequency table instead of a hash map — O(n) time, no hash collisions. Used in Top K Frequent Elements (via bucket sort on frequency).
