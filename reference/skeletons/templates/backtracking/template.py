"""
Backtracking — Choose / Explore / Un-choose Skeleton

Backtracking is DFS over the tree of partial solutions. At each node you make a
choice, recurse to extend it, then undo the choice so the next sibling starts
from a clean slate. Pruning — refusing to recurse into branches that cannot
possibly succeed — is what keeps the exponential search tractable.

The three-beat rhythm never changes:
    choose    -> push a candidate onto the current path
    explore   -> recurse to build on it
    un-choose -> pop it back off so siblings aren't polluted

Invariant: `path` always holds exactly the choices made on the route from the
root to the current recursion node — no more, no less.
"""

from typing import List


def backtrack(candidates: List[int]) -> List[List[int]]:
    """Enumerate every valid combination / permutation via DFS with undo.

    Time:      O(branching ^ depth) worst case — exponential by nature; pruning
               is what makes real inputs feasible.
    Space:     O(depth) for the recursion stack and path (output not counted).
    Invariant: on entry to dfs(start), `path` is a valid partial solution and
               `start` is the first candidate index still allowed to be chosen.
    """

    results: List[List[int]] = []
    path: List[int] = []

    def dfs(start: int) -> None:
        # GOAL TEST: record a solution when `path` satisfies the target shape.
        # TODO: problem-specific — record every node (subsets), only paths of a
        # fixed length (combinations/permutations), or only when a sum is hit.
        results.append(list(path))  # COPY: path keeps mutating after this line

        # OPTIONAL early exit once the path is complete:
        # TODO: `if len(path) == k: return`

        # Try each remaining candidate as the next choice.
        for index in range(start, len(candidates)):
            # PRUNE: skip choices that cannot lead to a valid solution.
            # TODO: e.g. skip duplicate siblings
            #   if index > start and candidates[index] == candidates[index - 1]:
            #       continue
            # or break early when the remaining sum would overshoot the target.

            # CHOOSE
            path.append(candidates[index])

            # EXPLORE: pass `index + 1` to forbid reuse (combinations); pass
            # `index` to allow reuse (combination sum); use a `used` set and
            # start from 0 for permutations.
            dfs(index + 1)

            # UN-CHOOSE: undo the choice so the next sibling branch starts clean.
            path.pop()

    dfs(0)
    return results
