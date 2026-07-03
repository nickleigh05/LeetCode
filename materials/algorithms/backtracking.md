# Backtracking

```python
def backtrack(path, choices):
    if is_complete(path):
        results.append(path[:])     # record a copy — path keeps mutating
        return
    for choice in choices:
        path.append(choice)          # choose
        backtrack(path, next_choices(choices, choice))   # explore
        path.pop()                     # un-choose
```

[DFS](dfs.md) over the space of *partial solutions*: try a choice, recurse to explore everything that follows from it, then undo the choice before trying the next one — the "un-choose" step is what distinguishes backtracking from plain DFS, since it lets the same `path` list be reused across every branch instead of copying it. Add a pruning check (`if invalid(path): return` before recursing further) to skip whole branches that can't lead anywhere valid, which is what keeps otherwise-exponential search practical.

Used for subsets, permutations, combinations, N-Queens, Sudoku — anything shaped like "build up a solution piece by piece, backing out of dead ends."

**Complexity:** typically exponential in the worst case (bounded by the size of the solution space), pruning reduces the practical branching factor.

**Related:** [dfs](dfs.md) · [recursion-basics (syntax)](../syntax/recursion-basics.md) · [itertools-basics (syntax)](../syntax/itertools-basics.md)
