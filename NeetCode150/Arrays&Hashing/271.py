"""

271. Encode and Decode Strings

Medium

Design an algorithm to encode a list of strings to a single string. The encoded string is then sent
over the network and is decoded back to the original list of strings.

Example 1:

    Input: ["neet","code","love","you"]

    Output: ["neet","code","love","you"]

Example 2:

    Input: ["we","say",":","yes"]

    Output: ["we","say",":","yes"]

Constraints:

    0 <= strs.length < 100
    0 <= strs[i].length < 200
    strs[i] contains only UTF-8 characters.

"""

class Solution:
    
    def encode(self, strs: list[str]) -> str:
        return "".join(f"{len(s)}#{s}" for s in strs)

    def decode(self, s: str) -> list[str]:
        result = []
        i = 0
        while i < len(s):
            j = s.index("#", i)
            length = int(s[i:j])
            result.append(s[j + 1 : j + 1 + length])
            i = j + 1 + length
        return result
    
















