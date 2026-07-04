# Common Python Errors, Decoded

*The errors you'll actually hit doing LeetCode, what each one is really telling you, and the usual DSA-specific cause.*

Read the last line of the [traceback](debugging-python.md) first — the error type names the crime; this page maps it to the usual suspect.

## `IndexError: list index out of range`

You asked for `nums[i]` with `i >= len(nums)` (or `i < -len(nums)`). Usual causes: looping `range(len(nums))` but indexing `nums[i + 1]` inside; forgetting an empty-input check; two-pointer code where a pointer walks past the end. Check every `+1`/`-1` near the failing line.

## `KeyError: 'x'`

Dict lookup for a key that isn't there. Either check first (`if k in d:`), use `d.get(k, default)`, or switch to a [defaultdict](../syntax/defaultdict.md) — the standard move in counting problems.

## `TypeError: 'NoneType' object is not subscriptable` (and friends)

Something is `None` where you expected a real value. Classic sources: a function that forgot to `return` (Python silently [returns None](../syntax/none-type.md)); reaching the end of a [linked list](../data-structures/linked-list.md) (`node.next.next` when `node.next` is None); a [tree](../data-structures/binary-tree.md) recursion missing its `if not node:` base case.

## `RecursionError: maximum recursion depth exceeded`

Either your recursion has no reachable [base case](../syntax/recursion-basics.md) (infinite), or the input is legitimately deeper than Python's ~1000-frame default — a 10⁵-node skewed tree will do it. Fix the base case first; if the depth is legitimate, raise the limit (see [recursion-limit (syntax)](../syntax/recursion-limit.md)) or rewrite iteratively with an explicit [stack](../data-structures/stack.md).

## `TypeError: unhashable type: 'list'`

You used a list as a [set](../syntax/set-basics.md) member or [dict](../syntax/dict-basics.md) key. Convert to a [tuple](../syntax/tuple-basics.md) first: `seen.add(tuple(path))`. Same fix for grid coordinates: store `(r, c)` tuples, not `[r, c]` lists.

## `ValueError: not enough values to unpack`

`a, b = something` where `something` didn't have exactly two items. Often a function returning one value where you expected a pair — see [tuple-unpacking](../syntax/tuple-unpacking.md).

## `UnboundLocalError: local variable referenced before assignment`

You assigned to an outer variable inside a nested function (common in DFS helpers: `count += 1`), which silently makes it local. Declare `nonlocal count` — see [global-nonlocal (syntax)](../syntax/global-nonlocal.md) — or accumulate in a mutable container instead.

## `TypeError: '<' not supported between instances of …`

Usually from [heapq](../syntax/heapq-module.md) when two tuples tie on the first element and Python falls back to comparing the second (an unorderable object). Add a tiebreaker index: `heappush(h, (dist, i, node))`.

## Not errors, but bugs that *look* like the judge is wrong

- **Aliased rows:** `grid = [[0] * n] * m` makes m references to *one* row — writing `grid[0][0]` changes every row. Use `[[0] * n for _ in range(m)]`. See [nested-lists](../syntax/nested-lists.md).
- **Mutable default argument:** `def f(path=[])` shares one list across *all* calls — state leaks between test cases. See [the pitfall page](../syntax/mutable-default-arg-pitfall.md).
- **Aliasing on append:** `res.append(path)` stores a *reference*; when backtracking later mutates `path`, every stored answer mutates too. Append a copy: `res.append(path[:])`. See [copy-vs-deepcopy](../syntax/copy-vs-deepcopy.md).
- **Integer division surprises:** `-7 // 2 == -4` (floors toward −∞, not toward 0). See [integer-division-modulo](../syntax/integer-division-modulo.md).

**Related:** [debugging-python](debugging-python.md) · [testing-locally](testing-locally.md) · [how-to-use-leetcode](how-to-use-leetcode.md)
