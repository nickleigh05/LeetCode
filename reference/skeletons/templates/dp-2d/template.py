"""
2-D Dynamic Programming — Grid / Two-Sequence Skeleton

Same idea as 1-D DP, but the state needs two indices. Two flavors dominate:

  GRID DP       — dp[r][c] = best way to reach / cover cell (r, c). Transitions
                  come from the neighbors you may step from (usually up + left).
  TWO-SEQUENCE  — dp[i][j] = answer for prefix A[:i] against prefix B[:j]. Used
                  for edit distance, LCS, string matching, knapsack.

State / transition / base case are exactly as in 1-D — there are just two axes.

Invariant: when dp[i][j] is computed, every cell it depends on (typically
dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) is already final.
"""

from typing import List


def dp_two_sequence(text_a: str, text_b: str) -> int:
    """Two-sequence DP over prefixes of A and B (LCS-style transition shown).

    Time:      O(len_a * len_b)
    Space:     O(len_a * len_b) — reducible to O(min(len_a, len_b)) with two rows.
    Invariant: dp[i][j] is the answer for text_a[:i] vs text_b[:j]; it only reads
               shorter prefixes, which are already filled in.
    """

    len_a, len_b = len(text_a), len(text_b)

    # 1-based prefix lengths: row/col 0 model the EMPTY prefix. The extra row and
    # column are what make the base cases fall out for free.
    dp = [[0] * (len_b + 1) for _ in range(len_a + 1)]

    # BASE CASE: dp[0][*] and dp[*][0] are the empty-prefix answers (here, 0).
    # TODO: for edit distance seed dp[i][0] = i and dp[0][j] = j (pure
    # deletions / insertions); for LCS the zeros above are already correct.

    for i in range(1, len_a + 1):
        for j in range(1, len_b + 1):
            # NOTE the index shift: the i-th character is text_a[i - 1].
            if text_a[i - 1] == text_b[j - 1]:
                # Characters align: extend the diagonal subproblem.
                # TODO: problem-specific match branch.
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                # Characters differ: drop one char from A or from B, take best.
                # TODO: problem-specific mismatch branch.
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # TODO: the answer is usually the bottom-right corner.
    return dp[len_a][len_b]


def dp_grid(grid: List[List[int]]) -> int:
    """Grid DP: best cost to reach each cell from the top-left (min-path shown).

    Time:      O(rows * cols)
    Space:     O(rows * cols) — reducible to O(cols) with a single rolling row.
    Invariant: dp[r][c] is the optimal value to reach (r, c); it reads only the
               cells above and to the left, which are already done.
    """

    rows, cols = len(grid), len(grid[0])
    dp = [[0] * cols for _ in range(rows)]

    # BASE CASE: the origin is just its own cost.
    dp[0][0] = grid[0][0]

    # The first row and first column each have exactly one way in — from their
    # single in-bounds neighbor — so fill them before the main loop.
    for c in range(1, cols):
        dp[0][c] = dp[0][c - 1] + grid[0][c]
    for r in range(1, rows):
        dp[r][0] = dp[r - 1][0] + grid[r][0]

    for r in range(1, rows):
        for c in range(1, cols):
            # TRANSITION: arrive from above or from the left, take the better.
            # TODO: problem-specific (min vs max, counting paths vs cost, etc.).
            dp[r][c] = grid[r][c] + min(dp[r - 1][c], dp[r][c - 1])

    return dp[rows - 1][cols - 1]
