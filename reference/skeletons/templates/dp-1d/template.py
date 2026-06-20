"""
1-D Dynamic Programming — Tabulation and Memoization Skeletons

DP breaks a problem into overlapping subproblems, solves each once, and reuses
the answer. Every DP has three pieces — name them before writing any code:

  STATE       — what dp[i] means, in one precise sentence.
  TRANSITION  — how dp[i] is built from smaller states (the recurrence).
  BASE CASE   — the smallest states you can fill in directly.

Two equivalent shapes:
  1. BOTTOM-UP (tabulation) — fill an array from the base cases forward.
  2. TOP-DOWN (memoization) — recurse from the goal, caching each result.

Invariant: by the time dp[i] is read, every smaller state it depends on has
already been computed correctly.
"""

from functools import lru_cache
from typing import List


def dp_bottom_up(nums: List[int]) -> int:
    """Tabulation: fill dp left to right from the base cases.

    Time:      O(n * transition_cost)
    Space:     O(n) for the table — often reducible to O(1) rolling variables
               when dp[i] only looks back a constant number of steps.
    Invariant: dp[i] is final and correct before dp[i + 1] reads it.
    """

    n = len(nums)
    if n == 0:
        return 0  # TODO: problem-specific empty-input answer

    # STATE: dp[i] = the answer for the subproblem ending at / using index i.
    # TODO: writing this definition down precisely is the whole game.
    dp = [0] * n

    # BASE CASE: the smallest subproblem(s), fillable with no recurrence.
    dp[0] = nums[0]  # TODO: problem-specific base value

    for i in range(1, n):
        # TRANSITION: combine previously-computed states into dp[i].
        # TODO: problem-specific recurrence, e.g.
        #   dp[i] = max(dp[i - 1] + nums[i], nums[i])   # max subarray (Kadane)
        #   dp[i] = dp[i - 1] + dp[i - 2]               # ways to climb stairs
        #   dp[i] = max(dp[i - 1], dp[i - 2] + nums[i]) # house robber
        dp[i] = max(dp[i - 1] + nums[i], nums[i])

    # TODO: the answer is sometimes dp[n - 1], sometimes max(dp), sometimes dp[0].
    return max(dp)


def dp_top_down(nums: List[int]) -> int:
    """Memoization: recurse from the goal, caching each subproblem once.

    Time:      O(number_of_states * transition_cost)
    Space:     O(number_of_states) cache + O(depth) recursion stack.
    Invariant: solve(i) runs at most once per i; every later call is a cache
               hit, which is what turns exponential recursion into polynomial.
    """

    @lru_cache(maxsize=None)
    def solve(i: int) -> int:
        # BASE CASE: the smallest states return directly, no recursion.
        # TODO: problem-specific, e.g. `if i < 0: return 0`.
        if i == 0:
            return nums[0]

        # TRANSITION: express solve(i) using strictly smaller states only.
        # TODO: problem-specific recurrence (mirror the bottom-up one above).
        return max(solve(i - 1) + nums[i], nums[i])

    if not nums:
        return 0
    return max(solve(i) for i in range(len(nums)))
