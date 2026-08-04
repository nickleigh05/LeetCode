"""

17. Letter Combinations of a Phone Number

Medium

Given a string containing digits from 2-9 inclusive, return all possible letter combinations that the number could represent. Return the answer in any order.
A mapping of digits to letters (just like on the telephone buttons) is given below. Note that 1 does not map to any letters.

+-------+-------+-------+
| 1 oo  | 2 abc | 3 def |
+-------+-------+-------+
| 4 ghi | 5 jkl | 6 mno |
+-------+-------+-------+
| 7 pqrs| 8 tuv | 9 wxyz|
+-------+-------+-------+
|  * +  |  0 _  |  ^ #  |
+-------+-------+-------+

Example 1:

    Input: digits = "23"
    Output: ["ad","ae","af","bd","be","bf","cd","ce","cf"]

Example 2:

    Input: digits = "2"
    Output: ["a","b","c"]

Constraints:

    1 <= digits.length <= 4
    digits[i] is a digit in the range ['2', '9'].

"""

class Solution:
    def letterCombinations(self, digits: str) -> List[str]:

        if not digits:
            return []

        phone = {
            "2": "abc",
            "3": "def",
            "4": "ghi",
            "5": "jkl",
            "6": "mno",
            "7": "pqrs",
            "8": "tuv",
            "9": "wxyz",
        }

        result = []

        def backtrack(index, current):
            if index == len(digits):
                result.append("".join(current))
                return
            letters = phone[digits[index]]
            for letter in letters:
                current.append(letter)
                backtrack(index + 1, current)
                current.pop()

        backtrack(0, [])
        return result












