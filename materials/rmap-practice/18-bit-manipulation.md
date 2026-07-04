# 18. Bit Manipulation — Practice

The Roadmap follows a curated list called the NeetCode 150 for practice problems. If you want more or fewer problems, check the other lists in [lists/](../../lists/).

[← Back to the lesson](../learning/18-bit-manipulation.md) · [🗺 Roadmap](../../roadmap.md)

---

### 136. Single Number — Easy
[LeetCode](https://leetcode.com/problems/single-number/)  
[Solution file (no hints)](../../problems/0001-0499/136.py)

Every number appears twice except one; find that one in O(1) space. Why does XOR-ing everything together cancel out all the pairs and leave only the single number?

<details>
<summary>Hint</summary>

XOR is its own inverse: `a ^ a = 0` and `a ^ 0 = a` (see [bitwise operators](../syntax/bitwise-operators.md)). XOR-ing every number together cancels every pair to 0, leaving only the number that appears once.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def singleNumber(self, nums: List[int]) -> int:

        res = 0
        for num in nums:
            res ^= num
        return res
```

Building blocks: [bitwise-operators](../syntax/bitwise-operators.md) (`^`) · [for-loop](../syntax/for-loop.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — a single pass over the array.
**Space: O(1)** — one running variable.
</details>

---

### 191. Number of 1 Bits — Easy
[LeetCode](https://leetcode.com/problems/number-of-1-bits/)  
[Solution file (no hints)](../../problems/0001-0499/191.py)

Count the number of 1 bits in an integer's binary representation. Why does `n & (n - 1)` always clear exactly the lowest set bit — and how does repeating that let you count set bits in a number of steps equal to their count?

<details>
<summary>Hint</summary>

Brian Kernighan's trick: `n & (n - 1)` (see [bitwise operators](../syntax/bitwise-operators.md)) clears the lowest set bit each time. Count how many times you can do that before `n` becomes 0.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def hammingWeight(self, n: int) -> int:

        count = 0
        while n:
            n &= n - 1   # clears the lowest set bit
            count += 1
        return count
```

Building blocks: [bitwise-operators](../syntax/bitwise-operators.md) (`&`) · [while-loop](../syntax/while-loop.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(k)** — k is the number of set bits (at most 32 for a standard integer).
**Space: O(1)** — one running counter.
</details>

---

### 338. Counting Bits — Easy
[LeetCode](https://leetcode.com/problems/counting-bits/)  
[Solution file (no hints)](../../problems/0001-0499/338.py)

For every number from 0 to n, count its set bits. Why does the set-bit count of `i` equal the set-bit count of `i` with its lowest bit removed, plus 1?

<details>
<summary>Hint</summary>

[DP](../algorithms/dynamic-programming.md) building on smaller answers: `bits(i) = bits(i >> 1) + (i & 1)` (equivalently `bits(i // 2) + i % 2`) — dropping the lowest bit, then adding it back in if it was a 1.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def countBits(self, n: int) -> List[int]:

        ans = [0] * (n + 1)

        for i in range(1, n + 1):
            ans[i] = ans[i // 2] + (i % 2)
        return ans
```

Building blocks: [list-basics](../syntax/list-basics.md) · [integer-division-modulo](../syntax/integer-division-modulo.md) (`//`, `%`) · [for-loop](../syntax/for-loop.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — each answer computed in O(1) from a smaller one.
**Space: O(n)** — the output array.
</details>

---

### 190. Reverse Bits — Easy
[LeetCode](https://leetcode.com/problems/reverse-bits/)  
[Solution file (no hints)](../../problems/0001-0499/190.py)

Reverse the bits of a 32-bit unsigned integer. Why does building the result bit by bit — shifting the result left and pulling each source bit off the right — naturally reverse the order?

<details>
<summary>Hint</summary>

Process 32 times: shift the result left to make room, then OR in the lowest bit of `n` (see [bitwise operators](../syntax/bitwise-operators.md)); shift `n` right to move to its next bit. Building the result this way reverses the bit order.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def reverseBits(self, n: int) -> int:

        result = 0

        for i in range(32):
            bit = (n >> i) & 1
            result = result | (bit << (31 - i))
        return result
```

Building blocks: [bitwise-operators](../syntax/bitwise-operators.md) (`>>`, `<<`, `&`, `|`) · [for-loop](../syntax/for-loop.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(1)** — always exactly 32 iterations.
**Space: O(1)** — one running result variable.
</details>

---

### 268. Missing Number — Easy
[LeetCode](https://leetcode.com/problems/missing-number/)  
[Solution file (no hints)](../../problems/0001-0499/268.py)

Given n distinct numbers from `[0, n]` with one missing, find it. Why does XOR-ing every index and every value together leave only the missing number?

<details>
<summary>Hint</summary>

XOR every index `0..n` together with every value in `nums` (see [bitwise operators](../syntax/bitwise-operators.md)). Every number that's present cancels with its matching index, leaving only the number that has no partner — the missing one.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def missingNumber(self, nums: List[int]) -> int:

        res = len(nums)   # accounts for index n, which has no matching nums index

        for i, num in enumerate(nums):
            res ^= i ^ num
        return res
```

Building blocks: [bitwise-operators](../syntax/bitwise-operators.md) (`^`) · [enumerate](../syntax/enumerate.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — a single pass over the array.
**Space: O(1)** — one running variable.
</details>

---

### 371. Sum of Two Integers — Medium
[LeetCode](https://leetcode.com/problems/sum-of-two-integers/)  
Solution: not yet solved in this repo.

Add two integers without using `+` or `-`. Why does XOR give you the "sum without carrying," while AND-then-shift gives you exactly the carry to add in next?

<details>
<summary>Hint</summary>

`a ^ b` (see [bitwise operators](../syntax/bitwise-operators.md)) adds bits without carrying; `(a & b) << 1` computes the carry that resulted. Repeat — treating the XOR as the new sum and the shifted AND as the new "b" to add — until there's no carry left.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def getSum(self, a: int, b: int) -> int:

        mask = 0xFFFFFFFF   # keep results within 32 bits

        while b & mask:
            carry = (a & b) << 1
            a = (a ^ b) & mask
            b = carry & mask

        if a > 0x7FFFFFFF:   # reinterpret as a negative 32-bit signed number
            a = ~(a ^ mask)

        return a
```

Building blocks: [bitwise-operators](../syntax/bitwise-operators.md) (`^`, `&`, `<<`, `~`) · [while-loop](../syntax/while-loop.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(1)** — bounded by 32 bit positions.
**Space: O(1)** — a few running variables.
</details>

---

### 7. Reverse Integer — Medium
[LeetCode](https://leetcode.com/problems/reverse-integer/)  
Solution: not yet solved in this repo.

Reverse the digits of a 32-bit signed integer, returning 0 if it overflows. Why does peeling off digits with `% 10` and `// 10` — the same digit-extraction trick used elsewhere — naturally build the reversed number?

<details>
<summary>Hint</summary>

Repeatedly take the last digit with `x % 10` and remove it with integer division `x // 10` (see [integer division & modulo](../syntax/integer-division-modulo.md)), building the reversed number as `res = res * 10 + digit`. Check the 32-bit signed range before returning.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def reverse(self, x: int) -> int:

        sign = -1 if x < 0 else 1
        x = abs(x)

        result = 0
        while x:
            digit = x % 10
            x //= 10
            result = result * 10 + digit

        result *= sign

        INT_MIN = -2**31
        INT_MAX = 2**31 - 1
        if result < INT_MIN or result > INT_MAX:
            return 0

        return result
```

Building blocks: [integer-division-modulo](../syntax/integer-division-modulo.md) (`%`, `//`) · [while-loop](../syntax/while-loop.md) · [comparison-operators](../syntax/comparison-operators.md) (`abs()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(log₁₀ x)** — proportional to the number of digits.
**Space: O(1)** — a few running variables.
</details>
