"""

709. To Lower Case

Easy

Given a string s, return the string after replacing every uppercase letter with the same lowercase letter.

Example 1:

    Input: s = "Hello"
    Output: "hello"

Example 2:

    Input: s = "here"
    Output: "here"

Example 3:

    Input: s = "LOVELY"
    Output: "lovely"

Constraints:

    1 <= s.length <= 100
    s consists of printable ASCII characters.

"""

class Solution:
    def toLowerCase(self, s: str) -> str:
        return s.lower()
















### Alternative solution using ASCII values ###

class Solution:
    def toLowerCase(self, s: str) -> str:
        res = []
        for char in s:
            # Check if character is an uppercase letter (ASCII 65-90)
            if 'A' <= char <= 'Z':
                # Convert to lowercase by adding 32 offset
                res.append(chr(ord(char) + 32))
            else:
                res.append(char)
        return "".join(res)







