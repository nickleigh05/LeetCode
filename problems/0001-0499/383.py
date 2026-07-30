"""

383. Ransom Note

Easy

Given two strings ransomNote and magazine, return true if 
ransomNote can be constructed by using the letters from magazine 
and false otherwise. Each letter in magazine can only be used 
once in ransomNote.

Example 1:

    Input: ransomNote = "a", magazine = "b"
    Output: false

Example 2:

    Input: ransomNote = "aa", magazine = "ab"
    Output: false

Example 3:

    Input: ransomNote = "aa", magazine = "aab"
    Output: true

Constraints:

    1 <= ransomNote.length, magazine.length <= 105
    ransomNote and magazine consist of lowercase English letters.

"""

class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        if len(ransomNote) > len(magazine):
            return False

        counts = [0] * 26

        for char in magazine:
            counts[ord(char) - ord('a')] += 1

        for char in ransomNote:
            counts[ord(char) - ord('a')] -= 1
            if counts[ord(char) - ord('a')] < 0:
                return False

        return True










### My original ###

class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        
        hashmap_Magazine = {}
        for char in magazine:
            hashmap_Magazine[char] = hashmap_Magazine.get(char, 0) + 1
        
        hashmap_ransomNote = {}
        for char in ransomNote:
            hashmap_ransomNote[char] = hashmap_ransomNote.get(char, 0) + 1
            if hashmap_ransomNote == hashmap_Magazine:
                return True
            else:
                return False









