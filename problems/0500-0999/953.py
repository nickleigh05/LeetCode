"""

953. Verifying an Alien Dictionary

Easy

In an alien language, surprisingly, they also use English lowercase letters, but possibly in a different order. The order of the alphabet is some permutation of lowercase letters.

Given a sequence of words written in the alien language, and the order of the alphabet, return true if and only if the given words are sorted lexicographically in this alien language.

Example 1:

    Input: words = ["hello","leetcode"], order = "hlabcdefgijkmnopqrstuvwxyz"
    Output: true
    Explanation: As 'h' comes before 'l' in this language, then the sequence is sorted.

Example 2:

    Input: words = ["word","world","row"], order = "worldabcefghijkmnpqstuvxyz"
    Output: false
    Explanation: As 'd' comes after 'l' in this language, then words[0] > words[1], hence the sequence is unsorted.

Example 3:

    Input: words = ["apple","app"], order = "abcdefghijklmnopqrstuvwxyz"
    Output: false
    Explanation: The first three characters "app" match, and the second string is shorter (in size.) According to lexicographical rules "apple" > "app", because 'l' > '∅', where '∅' is defined as the blank character which is less than any other character (More info : https://en.wikipedia.org/wiki/Lexicographic_order).

Constraints:

    1 <= words.length <= 100
    1 <= words[i].length <= 20
    order.length == 26
    All characters in words[i] and order are English lowercase letters.

"""

class Solution:
    def isAlienSorted(self, words: List[str], order: str) -> bool:
        
        priority = {}
        index = 0

        for char in order:
            priority[char] = index
            index += 1

        def word_key(word):
            key = []
            for char in word:
                key.append(priority[char])
            return key

        for i in range(len(words) - 1):
            first_key = word_key(words[i])
            second_key = word_key(words[i + 1])
            if first_key > second_key:
                return False

        return True
    








