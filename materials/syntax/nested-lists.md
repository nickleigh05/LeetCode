# Nested Lists (2-D Arrays)

```python
grid = [[0, 0], [0, 0]]
grid[0][1] = 5          # row 0, column 1
rows, cols = len(grid), len(grid[0])

for row in grid:
    for val in row:
        print(val)
```

A "2-D array" in Python is just a list of lists — `grid[r][c]` accesses row `r`, column `c`. Watch out when *creating* one: `[[0] * cols] * rows` makes `rows` references to the **same inner list** (mutating one row mutates all of them); use `[[0] * cols for _ in range(rows)]` instead.

**Related:** [list-basics](list-basics.md) · [list-comprehension](list-comprehension.md) · [copy-vs-deepcopy](copy-vs-deepcopy.md)
