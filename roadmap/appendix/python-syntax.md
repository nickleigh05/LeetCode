# 🐍 Python Syntax Reference — Beginner's Guide

> New to Python? This covers the core language syntax you need before diving into the DSA cheat sheets. No prior Python experience assumed.

---

## Table of Contents

| # | Section |
|---|---------|
| 01 | [Running Python](#01-running-python) |
| 02 | [Variables & Types](#02-variables--types) |
| 03 | [Operators](#03-operators) |
| 04 | [Strings](#04-strings) |
| 05 | [Lists](#05-lists) |
| 06 | [Tuples & Sets & Dicts](#06-tuples-sets--dicts) |
| 07 | [Conditionals](#07-conditionals) |
| 08 | [Loops](#08-loops) |
| 09 | [Functions](#09-functions) |
| 10 | [Classes](#10-classes) |
| 11 | [Error Handling](#11-error-handling) |
| 12 | [Useful Built-ins](#12-useful-built-ins) |
| 13 | [Imports](#13-imports) |
| 14 | [Common Beginner Mistakes](#14-common-beginner-mistakes) |
| 15 | [Complexity of Common Operations](#15-complexity-of-common-operations) |

---

## 01 Running Python

```python
# Run a file
# $ python3 solution.py

# Check your version
# $ python3 --version

# Python uses indentation (4 spaces) instead of curly braces
# This is NOT optional — wrong indentation = error

if True:
    print("indented block")   # this is inside the if
print("back outside")         # this is outside the if

# Comments start with #
# There are no multi-line comment blocks — just use multiple #
```

---

## 02 Variables & Types

```python
# No type declaration needed — Python figures it out
x = 10           # int
y = 3.14         # float
name = "Alice"   # str
flag = True      # bool  (capital T/F)
nothing = None   # None  (like null in other languages)

# Check the type of anything
type(x)          # <class 'int'>
type(name)       # <class 'str'>

# Type conversion
int("42")        # → 42
float("3.14")    # → 3.14
str(99)          # → "99"
bool(0)          # → False  (0, "", [], None are all falsy)
bool(1)          # → True

# Multiple assignment
a, b, c = 1, 2, 3
a = b = 0          # both set to 0

# Swap (no temp variable needed in Python)
a, b = b, a

# Constants (Python has no true const — convention is ALL_CAPS)
MAX_SIZE = 1000
```

---

## 03 Operators

```python
# --- Arithmetic ---
5 + 3    # 8
5 - 3    # 2
5 * 3    # 15
5 / 3    # 1.666...  (always float)
5 // 3   # 1         (floor division — rounds toward negative infinity)
5 % 3    # 2         (modulo / remainder)
5 ** 3   # 125       (exponent)

# --- Comparison (returns True or False) ---
x == y   # equal
x != y   # not equal
x > y
x < y
x >= y
x <= y

# --- Logical ---
True and False   # False
True or False    # True
not True         # False

# --- Useful shorthands ---
x += 1    # same as x = x + 1
x -= 1
x *= 2
x //= 2

# --- Chained comparisons (unique to Python) ---
1 < x < 10       # True if x is between 1 and 10
0 <= i < n       # very common in loop bounds

# --- Identity vs equality ---
x == y    # same value?
x is y    # same object in memory? (use for None checks)
x is None
x is not None
```

---

## 04 Strings

```python
# --- Creating strings ---
s = "hello"
s = 'hello'          # single or double quotes — same thing
s = """
multi
line
"""

# --- Indexing (0-based) ---
s = "hello"
s[0]       # 'h'
s[-1]      # 'o'  (last character)
s[-2]      # 'l'  (second to last)

# --- Slicing ---
s[1:4]     # 'ell'  (index 1 up to but not including 4)
s[:3]      # 'hel'  (from start)
s[2:]      # 'llo'  (to end)
s[::-1]    # 'olleh' (reversed)

# --- Strings are immutable (can't change individual chars) ---
# s[0] = 'H'   ← This will ERROR

# --- Common methods ---
s.upper()          # 'HELLO'
s.lower()          # 'hello'
s.strip()          # remove leading/trailing whitespace
s.split(",")       # split by comma → list of strings
",".join(["a","b","c"])  # → 'a,b,c'
s.replace("l","r") # 'herro'
s.startswith("he") # True
s.endswith("lo")   # True
s.find("ll")       # 2  (index of first match, -1 if not found)
s.count("l")       # 2

# --- f-strings (easiest way to format) ---
name = "Alice"
age = 30
print(f"My name is {name} and I am {age} years old.")
print(f"2 + 2 = {2 + 2}")    # expressions work inside {}

# --- Check character type ---
"a".isalpha()    # True  (letter)
"3".isdigit()    # True  (digit)
"a3".isalnum()   # True  (letter or digit)
" ".isspace()    # True

# --- String length ---
len("hello")     # 5

# --- in operator ---
"ell" in "hello"    # True
"xyz" in "hello"    # False
```

---

## 05 Lists

```python
# Lists are ordered, mutable, and can hold mixed types
nums = [1, 2, 3, 4, 5]
mixed = [1, "hello", True, 3.14]
empty = []

# --- Indexing & Slicing (same as strings) ---
nums[0]     # 1
nums[-1]    # 5
nums[1:3]   # [2, 3]

# --- Modifying ---
nums.append(6)         # add to end
nums.insert(0, 99)     # insert 99 at index 0
nums.pop()             # remove and return last element
nums.pop(0)            # remove and return element at index 0
nums.remove(3)         # remove first occurrence of value 3
nums[0] = 100          # change element at index

# --- Info ---
len(nums)              # number of elements
3 in nums              # True/False membership check
nums.index(4)          # index of first occurrence of 4
nums.count(2)          # count occurrences of 2

# --- Sorting ---
nums.sort()            # sort in-place (modifies original)
nums.sort(reverse=True)
new = sorted(nums)     # returns new sorted list, original unchanged

# --- Combining ---
a + b                  # concatenate two lists → new list
a.extend(b)            # append all of b onto a (in-place)

# --- List comprehension (compact way to build lists) ---
squares = [x**2 for x in range(5)]          # [0, 1, 4, 9, 16]
evens   = [x for x in range(10) if x % 2 == 0]  # [0, 2, 4, 6, 8]

# --- 2D list (grid) ---
grid = [[0, 1, 2],
        [3, 4, 5],
        [6, 7, 8]]
grid[1][2]    # 5  (row 1, col 2)

# Create a 3x3 grid of zeros
grid = [[0] * 3 for _ in range(3)]
# DON'T do: [[0] * 3] * 3  ← all rows point to same list (bug)
```

---

## 06 Tuples, Sets & Dicts

```python
# ── TUPLES ─────────────────────────────────────────
# Like lists but immutable (can't be changed after creation)
t = (1, 2, 3)
t[0]          # 1
# t[0] = 9   ← ERROR

# Useful for returning multiple values from a function
def min_max(arr):
    return min(arr), max(arr)   # returns a tuple

lo, hi = min_max([3, 1, 4])    # unpack directly

# Single-element tuple needs a trailing comma
single = (5,)    # not just (5) — that's just parentheses

# ── SETS ───────────────────────────────────────────
# Unordered, no duplicates, O(1) lookup
s = {1, 2, 3}
s = set()           # empty set  (NOT {} — that's an empty dict)

s.add(4)
s.discard(2)        # remove if present, no error if missing
s.remove(2)         # remove, raises error if missing

3 in s              # O(1) — much faster than checking a list

# Set from a list (removes duplicates)
unique = set([1, 2, 2, 3, 3])    # {1, 2, 3}

# ── DICTS ──────────────────────────────────────────
# Key-value pairs, O(1) get/set, insertion-ordered (Python 3.7+)
d = {"name": "Alice", "age": 30}
d = {}                          # empty dict

d["name"]                       # "Alice"
d["city"] = "NYC"               # add or update
d.get("age")                    # 30  (safe — returns None if missing)
d.get("missing", 0)             # 0   (default if key not found)
del d["age"]                    # delete a key
"name" in d                     # True (check if key exists)

# Iterate
for key in d:               # iterate keys
    print(key, d[key])

for key, val in d.items():  # iterate key-value pairs
    print(key, val)

for val in d.values():      # iterate values only
    print(val)

# Dict comprehension
squares = {x: x**2 for x in range(5)}   # {0:0, 1:1, 2:4, 3:9, 4:16}
```

---

## 07 Conditionals

```python
# --- if / elif / else ---
x = 10

if x > 10:
    print("big")
elif x == 10:
    print("ten")
else:
    print("small")

# --- Ternary / one-liner ---
result = "yes" if x > 5 else "no"

# --- Falsy values (all evaluate to False in a condition) ---
# False, 0, 0.0, "", [], {}, set(), None

if not arr:         # True when arr is empty
    print("empty")

if arr:             # True when arr is non-empty
    print("has items")

# --- Comparing None ---
if x is None:       # correct
    pass
if x is not None:   # correct
    pass
# if x == None:     ← works but not Pythonic
```

---

## 08 Loops

```python
# --- for loop over a list ---
for x in [1, 2, 3]:
    print(x)

# --- range ---
for i in range(5):        # 0, 1, 2, 3, 4
    print(i)

for i in range(2, 6):     # 2, 3, 4, 5
    print(i)

for i in range(10, 0, -2):  # 10, 8, 6, 4, 2  (step -2)
    print(i)

# --- enumerate (get index AND value) ---
fruits = ["apple", "banana", "cherry"]
for i, fruit in enumerate(fruits):
    print(i, fruit)    # 0 apple, 1 banana, 2 cherry

# --- zip (iterate two lists together) ---
names = ["Alice", "Bob"]
ages  = [30, 25]
for name, age in zip(names, ages):
    print(name, age)

# --- while loop ---
n = 10
while n > 0:
    print(n)
    n -= 1

# --- break and continue ---
for i in range(10):
    if i == 5:
        break          # exit loop entirely
    if i % 2 == 0:
        continue       # skip to next iteration
    print(i)           # prints 1, 3

# --- loop over string ---
for ch in "hello":
    print(ch)          # h, e, l, l, o

# --- loop over dict ---
for key, val in d.items():
    print(key, "→", val)

# --- nested loops ---
for r in range(3):
    for c in range(3):
        print(r, c)

# --- _ as throwaway variable ---
for _ in range(5):     # when you don't need the loop variable
    print("hello")
```

---

## 09 Functions

```python
# --- Basic function ---
def greet(name):
    return "Hello, " + name

greet("Alice")    # "Hello, Alice"

# --- Default parameters ---
def power(base, exp=2):
    return base ** exp

power(3)      # 9   (uses default exp=2)
power(3, 3)   # 27

# --- Multiple return values ---
def divide(a, b):
    return a // b, a % b    # returns a tuple

quotient, remainder = divide(10, 3)

# --- *args (variable number of arguments) ---
def total(*nums):
    return sum(nums)

total(1, 2, 3, 4)    # 10

# --- **kwargs (keyword arguments as a dict) ---
def display(**info):
    for k, v in info.items():
        print(k, v)

display(name="Alice", age=30)

# --- Lambda (anonymous one-liner function) ---
square = lambda x: x ** 2
square(5)    # 25

# Common use: sorting with a custom key
pairs = [(1, 3), (2, 1), (0, 4)]
pairs.sort(key=lambda p: p[1])   # sort by second element

# --- Scope ---
x = 10          # global variable
def foo():
    x = 5       # local variable — does NOT affect global x
    print(x)    # 5

def bar():
    global x    # explicitly modify global
    x = 99

# --- Recursion ---
def factorial(n):
    if n == 0:
        return 1           # base case
    return n * factorial(n - 1)   # recursive case

factorial(5)    # 120

# Always need a base case — without it you get infinite recursion
```

---

## 10 Classes

```python
# --- Basic class ---
class Dog:
    # __init__ is the constructor (runs when you create an object)
    def __init__(self, name, age):
        self.name = name    # instance variables
        self.age = age

    def bark(self):
        return f"{self.name} says woof!"

    def __repr__(self):
        return f"Dog(name={self.name}, age={self.age})"

# Create an object (instance)
d = Dog("Rex", 3)
d.name       # "Rex"
d.bark()     # "Rex says woof!"
print(d)     # Dog(name=Rex, age=3)

# --- Inheritance ---
class Animal:
    def __init__(self, name):
        self.name = name
    def speak(self):
        return "..."

class Cat(Animal):
    def speak(self):            # override parent method
        return f"{self.name} says meow!"

c = Cat("Whiskers")
c.speak()    # "Whiskers says meow!"

# --- Classes in LeetCode ---
# Most LeetCode problems give you a class definition like:
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# You'll use these by accessing attributes:
node = ListNode(5)
node.val     # 5
node.next    # None
```

---

## 11 Error Handling

```python
# --- try / except ---
try:
    x = int("abc")      # this raises ValueError
except ValueError:
    print("not a number")

# --- catch multiple exception types ---
try:
    result = arr[10]
except (IndexError, TypeError) as e:
    print(f"Error: {e}")

# --- finally (always runs) ---
try:
    f = open("file.txt")
except FileNotFoundError:
    print("file not found")
finally:
    print("this always runs")

# --- Common exceptions in LeetCode ---
# IndexError    — list index out of range
# KeyError      — dict key not found
# ValueError    — wrong type conversion
# ZeroDivisionError — dividing by zero
# RecursionError — too many recursive calls

# Increase recursion limit for deep recursion problems
import sys
sys.setrecursionlimit(10**6)
```

---

## 12 Useful Built-ins

```python
# --- Math ---
abs(-5)           # 5
pow(2, 10)        # 1024
round(3.7)        # 4
min(3, 1, 4)      # 1
max(3, 1, 4)      # 4
sum([1, 2, 3])    # 6
divmod(10, 3)     # (3, 1) — quotient and remainder

# --- Sequence ---
len([1, 2, 3])    # 3
sorted([3,1,2])   # [1, 2, 3]  (new list)
reversed([1,2,3]) # iterator — wrap in list() to see it
list(reversed([1,2,3]))  # [3, 2, 1]
enumerate([a,b,c])       # (0,a), (1,b), (2,c)
zip([1,2], [3,4])        # (1,3), (2,4)

# --- Type checks ---
isinstance(x, int)       # True/False
isinstance(x, (int, float))   # check multiple types

# --- any / all ---
any([False, True, False])   # True  (at least one truthy)
all([True, True, False])    # False (all must be truthy)
any(x > 0 for x in nums)   # works with generator expressions too

# --- map / filter ---
list(map(str, [1, 2, 3]))           # ['1', '2', '3']
list(filter(lambda x: x>0, nums))   # keep positive numbers
# Prefer list comprehensions — they're more readable

# --- Input / Output (not needed on LeetCode but useful for local testing) ---
x = int(input("Enter a number: "))
print("Result:", x * 2)
print(x, y, sep=", ", end="\n")    # sep between items, end after last

# --- Infinity ---
float('inf')     # positive infinity
float('-inf')    # negative infinity
# Useful for initializing min/max:
best = float('inf')
for x in arr:
    best = min(best, x)
```

---

## 13 Imports

```python
# --- Standard library modules used in LeetCode ---

import math
math.gcd(12, 8)       # 4
math.lcm(4, 6)        # 12  (Python 3.9+)
math.floor(3.7)       # 3
math.ceil(3.2)        # 4
math.sqrt(16)         # 4.0
math.inf              # same as float('inf')

import sys
sys.setrecursionlimit(10**6)

from collections import defaultdict, Counter, deque, OrderedDict
from heapq import heappush, heappop, heapify, nlargest, nsmallest
from functools import lru_cache, reduce
from itertools import combinations, permutations, product
import bisect

# --- itertools examples ---
list(combinations([1,2,3], 2))    # [(1,2),(1,3),(2,3)]
list(permutations([1,2,3], 2))    # [(1,2),(1,3),(2,1),(2,3),(3,1),(3,2)]
list(product([0,1], repeat=3))    # all 3-bit binary strings

# --- bisect examples ---
import bisect
arr = [1, 3, 5, 7]
bisect.bisect_left(arr, 5)    # 2 — index where 5 would go (leftmost)
bisect.bisect_right(arr, 5)   # 3 — index after existing 5s
```

---

## 14 Common Beginner Mistakes

```python
# ❌ Mistake 1: Modifying a list while iterating over it
for x in arr:
    if x < 0:
        arr.remove(x)     # skips elements — unpredictable behavior
# ✅ Fix: iterate over a copy, or use list comprehension
arr = [x for x in arr if x >= 0]

# ❌ Mistake 2: Shallow copy of a 2D list
grid_copy = grid[:]         # rows are still shared!
# ✅ Fix: deep copy
import copy
grid_copy = copy.deepcopy(grid)
# or for grids of primitives:
grid_copy = [row[:] for row in grid]

# ❌ Mistake 3: Using a mutable default argument
def append_to(val, lst=[]):     # lst is shared across ALL calls
    lst.append(val)
    return lst
# ✅ Fix:
def append_to(val, lst=None):
    if lst is None:
        lst = []
    lst.append(val)
    return lst

# ❌ Mistake 4: Integer division expecting a float
5 / 2     # 2.5  ✅
5 // 2    # 2    (floor division — might not be what you want)

# ❌ Mistake 5: Comparing to True/False explicitly
if flag == True:    # works but not Pythonic
if flag:            # ✅ Pythonic

# ❌ Mistake 6: Creating a 2D list wrong
grid = [[0] * 3] * 3    # all 3 rows are the SAME list object
grid[0][0] = 1           # changes ALL rows!
# ✅ Fix:
grid = [[0] * 3 for _ in range(3)]

# ❌ Mistake 7: Forgetting that strings are immutable
s = "hello"
s[0] = "H"     # ERROR: TypeError
# ✅ Fix:
s = "H" + s[1:]

# ❌ Mistake 8: Off-by-one in range
for i in range(len(arr)):      # goes 0 to len-1 ✅
for i in range(len(arr) + 1):  # includes len — likely IndexError ❌

# ❌ Mistake 9: Not copying a list when storing results
res.append(path)       # stores reference — path will change later!
res.append(path[:])    # ✅ stores a snapshot copy

# ❌ Mistake 10: Using == to compare None
if x == None:    # works but wrong style
if x is None:    # ✅ correct
```

---

## 15 Complexity of Common Operations

Know these cold — picking the wrong container (or the wrong operation on the right container) is the most common way an O(n) solution silently becomes O(n²). Times are average-case unless noted.

### `list` (dynamic array)

| Operation | Time | Notes |
|-----------|------|-------|
| `lst[i]` (index) | O(1) | |
| `lst[i] = x` | O(1) | |
| `lst.append(x)` | O(1) amortized | occasional resize doubles capacity |
| `lst.pop()` (end) | O(1) | |
| `lst.pop(0)` (front) | **O(n)** | shifts everything — use `deque` instead |
| `lst.insert(i, x)` | O(n) | shifts the tail |
| `x in lst` | O(n) | linear scan — use a `set` for membership |
| `lst[a:b]` (slice) | O(b−a) | builds a new list |
| `len(lst)` | O(1) | stored, not counted |
| `lst.sort()` | O(n log n) | Timsort, in place, stable |
| `min`/`max`/`sum` | O(n) | |

### `dict` / `set` (hash table)

| Operation | Average | Worst | Notes |
|-----------|---------|-------|-------|
| get / set / `in` | O(1) | O(n) | worst only with pathological hash collisions |
| `del d[k]` | O(1) | O(n) | |
| iterate | O(n) | O(n) | dicts preserve insertion order (3.7+) |

Keys/elements must be **hashable** (immutable): `int`, `str`, `tuple` — not `list` or `set`.

### `collections.deque` (double-ended queue)

| Operation | Time |
|-----------|------|
| `append` / `pop` (right) | O(1) |
| `appendleft` / `popleft` (left) | O(1) |
| index in the middle | O(n) |

Reach for `deque` for BFS queues and sliding-window-maximum — never `list.pop(0)`.

### `heapq` (binary heap on a list)

| Operation | Time |
|-----------|------|
| `heappush` / `heappop` | O(log n) |
| `heap[0]` (peek min) | O(1) |
| `heapify(lst)` | O(n) |

Python's `heapq` is a **min-heap**; negate values for a max-heap.

### `str` (immutable)

| Operation | Time | Notes |
|-----------|------|-------|
| `s[i]` | O(1) | |
| `s + t` | O(n+m) | builds a new string — never concat in a loop |
| `"".join(parts)` | O(total length) | the right way to build strings |
| `x in s` (substring) | O(n·m) | naive search |

> **Rule of thumb:** need membership → `set`; need order + index → `list`; need FIFO/both-ends → `deque`; need the running min/max → `heapq`; need key→value → `dict`.

---

*Start here, then move on to [the core cheatsheet](cheatsheet-core.md) for core DSA patterns and [the advanced cheatsheet](cheatsheet-advanced.md) for advanced topics.*