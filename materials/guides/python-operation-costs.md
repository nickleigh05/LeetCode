# Python Operation Costs

*The Big-O of every built-in you actually use — because `x in list` and `x in set` look identical and differ by a factor of n.*

Your solution's complexity includes the hidden cost of built-ins. This is the lookup table.

## list

| Operation | Cost | Notes |
|-----------|------|-------|
| `lst[i]`, `lst[i] = v` | O(1) | index access |
| `lst.append(x)`, `lst.pop()` | O(1) | end only (amortized) |
| `lst.pop(0)`, `lst.insert(0, x)` | **O(n)** | shifts everything — use a [deque](../data-structures/deque.md) |
| `x in lst` | **O(n)** | linear scan — use a [set](../data-structures/hashset.md) |
| `lst.remove(x)`, `del lst[i]` | O(n) | search and/or shift |
| `lst[a:b]`, `lst.copy()` | O(b−a) | slicing copies |
| `lst.sort()`, `sorted(lst)` | O(n log n) | Timsort; O(n) if nearly sorted |
| `min/max/sum(lst)`, `lst.count(x)` | O(n) | full scan |
| `lst2 = lst + other`, `lst * k` | O(len result) | builds a new list |

## dict / set

| Operation | Cost | Notes |
|-----------|------|-------|
| `d[k]`, `d[k] = v`, `del d[k]`, `k in d` | O(1) avg | the whole point of [hashing](../learning/01-arrays-hashing.md) |
| `s.add(x)`, `x in s`, `s.remove(x)` | O(1) avg | |
| `s1 & s2`, `s1 | s2`, `s1 - s2` | O(len) | proportional to set sizes |
| iterate all items | O(n) | |
| keys must be hashable | — | tuples yes, lists no ([why](../syntax/tuple-basics.md)) |

## str (immutable!)

| Operation | Cost | Notes |
|-----------|------|-------|
| `s[i]`, `len(s)` | O(1) | |
| `s + t` | O(len s + len t) | new string every time — `+=` in a loop is O(n²) |
| `"".join(parts)` | O(total) | **the** way to build strings ([join](../syntax/string-join-slice.md)) |
| `x in s`, `s.find`, `s.replace`, `s.split` | O(n) | |
| slicing `s[a:b]` | O(b−a) | copies |

## deque, heapq, bisect

| Operation | Cost | Notes |
|-----------|------|-------|
| `deque.append/appendleft/pop/popleft` | O(1) | [deque](../syntax/deque-basics.md); indexing middle is O(n) |
| `heapq.heappush/heappop` | O(log n) | [heapq](../syntax/heapq-module.md) |
| `heapq.heapify(lst)` | O(n) | cheaper than n pushes |
| `bisect.bisect/insort` | O(log n) search / **O(n)** insert | [bisect](../syntax/bisect-module.md) — insort still shifts the list |

## The classic accidental-O(n²) traps

- `lst.pop(0)` in a loop → use `deque.popleft()`
- `s += char` in a loop → collect in a list, `"".join` at the end
- `x in lst` inside a loop → build a `set` once, test against it
- `lst.insert(0, x)` repeatedly → append then `reverse()`, or use a deque
- `min(lst)` inside a loop → track the running min, or use a [heap](../data-structures/heap.md)

**Related:** [constraints-cheatsheet](constraints-cheatsheet.md) · [Time complexity lesson](../learning/00d-time-complexity.md) · [list-methods (syntax)](../syntax/list-methods.md) · [dict-methods (syntax)](../syntax/dict-methods.md)
