# Arrays & Hashing

## Arrays

### What is an Array?
An array is a contiguous block of memory that stores elements of the same type. Each element can be accessed directly using its index.

### Visual Representation
```
Index:    0     1     2     3     4
        ┌─────┬─────┬─────┬─────┬─────┐
Array:  │ 10  │ 20  │ 30  │ 40  │ 50  │
        └─────┴─────┴─────┴─────┴─────┘
Memory: 0x100 0x104 0x108 0x10C 0x110
```

### Key Characteristics
- **Fixed Size**: Size is determined at creation (in static arrays)
- **Contiguous Memory**: Elements are stored next to each other
- **Index-Based Access**: O(1) time to access any element
- **Zero-Indexed**: First element is at index 0

### Time Complexity
| Operation | Time Complexity |
|-----------|----------------|
| Access    | O(1)          |
| Search    | O(n)          |
| Insert (end) | O(1) amortized |
| Insert (middle) | O(n) |
| Delete    | O(n)          |

### Common Operations

#### Accessing Elements
```
arr = [10, 20, 30, 40, 50]
arr[2]  # Returns 30

Visual:
        ↓ Access index 2
┌─────┬─────┬─────┬─────┬─────┐
│ 10  │ 20  │ 30  │ 40  │ 50  │
└─────┴─────┴─────┴─────┴─────┘
```

#### Inserting at End
```
Before: [10, 20, 30, 40]
Insert 50 at end

After:  [10, 20, 30, 40, 50]

┌─────┬─────┬─────┬─────┬─────┐
│ 10  │ 20  │ 30  │ 40  │ 50  │ ← New element
└─────┴─────┴─────┴─────┴─────┘
```

#### Inserting in Middle
```
Before: [10, 20, 40, 50]
Insert 30 at index 2

Step 1: Shift elements right
┌─────┬─────┬─────┬─────┬─────┐
│ 10  │ 20  │ 40  │ 40  │ 50  │
└─────┴─────┴─────┴─────┴─────┘
              ↓ shift

Step 2: Insert new element
┌─────┬─────┬─────┬─────┬─────┐
│ 10  │ 20  │ 30  │ 40  │ 50  │
└─────┴─────┴─────┴─────┴─────┘
              ↑ insert
```

#### Deleting Element
```
Before: [10, 20, 30, 40, 50]
Delete element at index 2

Step 1: Remove element
┌─────┬─────┬─────┬─────┬─────┐
│ 10  │ 20  │  X  │ 40  │ 50  │
└─────┴─────┴─────┴─────┴─────┘

Step 2: Shift elements left
┌─────┬─────┬─────┬─────┐
│ 10  │ 20  │ 40  │ 50  │
└─────┴─────┴─────┴─────┘
      ← shift ←
```

---

## Hashing

### What is Hashing?
Hashing is a technique to map data of arbitrary size to fixed-size values (hash codes). It's used to implement fast lookups, insertions, and deletions.

### Hash Function
A hash function converts a key into an index in the hash table:
```
hash(key) → index

Example: hash("apple") → 3
         hash("banana") → 7
         hash("orange") → 2
```

### Hash Table Structure
```
Key → Hash Function → Index → Value

"apple"  ─┐
          │ hash()
          ↓
Index:    0     1     2     3     4     5     6     7
        ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐
Table:  │     │     │     │  5  │     │     │     │  2  │
        └─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘
                            ↑                         ↑
                        "apple"                  "banana"
                        value: 5                 value: 2
```

### Collision Handling

#### 1. Chaining (Separate Chaining)
When multiple keys hash to the same index, store them in a linked list:

```
Index:    0     1     2     3     4     5
        ┌─────┬─────┬─────┬─────┬─────┬─────┐
Table:  │     │  ●  │     │  ●  │     │     │
        └─────┴──│──┴─────┴──│──┴─────┴─────┘
                 │            │
                 ↓            ↓
              [k1:v1]      [k3:v3] → [k4:v4] → [k5:v5]
                            (collision chain)
```

#### 2. Open Addressing (Linear Probing)
If a collision occurs, find the next available slot:

```
Insert "apple" → hash = 3
Insert "apricot" → hash = 3 (collision!)

Step 1: Try index 3 (occupied)
Step 2: Try index 4 (empty, insert here)

Index:    0     1     2     3     4     5
        ┌─────┬─────┬─────┬─────┬─────┬─────┐
Table:  │     │     │     │apple│apric│     │
        └─────┴─────┴─────┴─────┴─────┴─────┘
                            ↑     ↑
                        hash=3  probe→
```

### Hash Map Operations

#### Insert/Update
```
map = {}
map["key1"] = "value1"

"key1" → hash() → index 3
        ┌─────┬─────┬─────┬─────┬─────┐
        │     │     │     │ k1:v1│     │
        └─────┴─────┴─────┴─────┴─────┘
```

#### Lookup
```
map["key1"]  # Returns "value1"

"key1" → hash() → index 3 → retrieve value
        ┌─────┬─────┬─────┬─────┬─────┐
        │     │     │     │ k1:v1│     │
        └─────┴─────┴─────┴──↑──┴─────┘
                              │
                          O(1) lookup
```

#### Delete
```
del map["key1"]

"key1" → hash() → index 3 → remove entry
        ┌─────┬─────┬─────┬─────┬─────┐
        │     │     │     │  X  │     │
        └─────┴─────┴─────┴─────┴─────┘
```

### Time Complexity

| Operation | Average Case | Worst Case |
|-----------|-------------|-----------|
| Insert    | O(1)        | O(n)      |
| Delete    | O(1)        | O(n)      |
| Search    | O(1)        | O(n)      |

**Note**: Worst case occurs when all keys collide (poor hash function or many collisions).

### Hash Set vs Hash Map

#### Hash Set
Stores only keys (no values):
```
set = {1, 2, 3, 4}

Index:    0     1     2     3     4
        ┌─────┬─────┬─────┬─────┬─────┐
        │  1  │     │  3  │     │  2  │
        └─────┴─────┴─────┴─────┴─────┘
```

#### Hash Map (Dictionary)
Stores key-value pairs:
```
map = {"a": 1, "b": 2, "c": 3}

Index:    0     1     2     3     4
        ┌─────┬─────┬─────┬─────┬─────┐
        │ a:1 │     │ c:3 │     │ b:2 │
        └─────┴─────┴─────┴─────┴─────┘
```

### Common Use Cases

1. **Frequency Counting**
```
text = "hello"
freq = {}

After processing:
┌─────┬─────┬─────┬─────┐
│ h:1 │ e:1 │ l:2 │ o:1 │
└─────┴─────┴─────┴─────┘
```

2. **Two Sum Problem**
```
nums = [2, 7, 11, 15], target = 9

seen = {}
For each num:
  complement = target - num
  if complement in seen: return [seen[complement], current_index]
  seen[num] = current_index

Visualization:
num=2: seen = {2: 0}
num=7: complement=2, found! seen={2:0}, current=1
       return [0, 1]
```

3. **Deduplication**
```
arr = [1, 2, 2, 3, 3, 3, 4]
unique = set(arr)  # {1, 2, 3, 4}

Before:  [1, 2, 2, 3, 3, 3, 4]
After:   {1, 2, 3, 4}  (set)
```

### Load Factor & Rehashing

#### Load Factor
```
Load Factor = Number of Elements / Table Size

Example: 6 elements, 8 slots
Load Factor = 6/8 = 0.75

Index:    0     1     2     3     4     5     6     7
        ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐
        │  ●  │     │  ●  │  ●  │     │  ●  │  ●  │  ●  │
        └─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘
```

#### Rehashing (when load factor > threshold, typically 0.75)
```
Old Table (size 4):
┌─────┬─────┬─────┬─────┐
│  a  │  b  │  c  │     │
└─────┴─────┴─────┴─────┘

Rehash → New Table (size 8):
┌─────┬─────��────┬─────┬─────┬─────┬─────┬─────┐
│     │  a  │    │  b  │     │     │  c  │     │
└─────┴─────┴────┴─────┴─────┴─────┴─────┴─────┘
(elements redistributed with new hash function)
```

### Python Implementation Examples

```python
# Array operations
arr = [1, 2, 3, 4, 5]
arr.append(6)        # O(1) - add to end
arr.insert(0, 0)     # O(n) - insert at beginning
arr.pop()            # O(1) - remove from end
arr[2] = 10          # O(1) - update element

# Hash Map (dict)
hashmap = {}
hashmap["key"] = "value"    # O(1) - insert
value = hashmap.get("key")  # O(1) - lookup
del hashmap["key"]          # O(1) - delete
if "key" in hashmap:        # O(1) - contains

# Hash Set
hashset = set()
hashset.add(1)       # O(1) - insert
hashset.remove(1)    # O(1) - delete
if 1 in hashset:     # O(1) - contains
```

### Key Takeaways

**Arrays:**
- Use when you need indexed access
- Good for iteration and random access
- Fixed-size or dynamic (Python lists are dynamic)
- Cache-friendly due to contiguous memory

**Hashing:**
- Use when you need fast lookups, insertions, deletions
- Trade memory for speed
- Good hash function is crucial for performance
- Handle collisions appropriately
- Python's dict and set use hashing internally
