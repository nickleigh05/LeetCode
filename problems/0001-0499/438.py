"""

438. Find All Anagrams in a String

Medium

Given two strings s and p, return an array of all the start indices of p's in s. You may return the answer in any order.

Example 1:

    Input: s = "cbaebabacd", p = "abc"
    Output: [0,6]
    Explanation:
    The substring with start index = 0 is "cba", which is an anagram of "abc".
    The substring with start index = 6 is "bac", which is an anagram of "abc".

Example 2:

    Input: s = "abab", p = "ab"
    Output: [0,1,2]
    Explanation:
    The substring with start index = 0 is "ab", which is an anagram of "ab".
    The substring with start index = 1 is "ba", which is an anagram of "ab".
    The substring with start index = 2 is "ab", which is an anagram of "ab".

Constraints:

    1 <= s.length, p.length <= 3 * 104
    s and p consist of lowercase English letters.

"""

class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:

        k = len(p)
        pCount = Counter(p)
        sCount = Counter(s[:k])
        result = [0] if sCount == pCount else []

        for i in range(k, len(s)):
            sCount[s[i]] += 1          # add incoming right char
            sCount[s[i - k]] -= 1      # remove outgoing left char
            if sCount[s[i - k]] == 0:
                del sCount[s[i - k]]   # keep Counter clean for == comparison

            if sCount == pCount:
                result.append(i - k + 1)

        return result
    








### Sliding Window + Frequency Map ###

class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:

        if len(p) > len(s):
            return []

        pCount = Counter(p)
        sCount = Counter(s[:len(p)])
        result = []

        matches = sum(1 for c in pCount if pCount[c] == sCount[c])

        if matches == len(pCount):
            result.append(0)

        for i in range(len(p), len(s)):

            r = s[i]
            sCount[r] += 1
            if r in pCount:
                if sCount[r] == pCount[r]:
                    matches += 1
                elif sCount[r] == pCount[r] + 1:
                    matches -= 1

            l = s[i - len(p)]
            sCount[l] -= 1
            if l in pCount:
                if sCount[l] == pCount[l]:
                    matches += 1
                elif sCount[l] == pCount[l] - 1:
                    matches -= 1

            if matches == len(pCount):
                result.append(i - len(p) + 1)

        return result
    





