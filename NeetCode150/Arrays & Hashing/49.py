"""
49. Group Anagrams

Medium

Given an array of strings strs, group the anagrams together. You can return the answer in any order.

    Example 1:

    Input: strs = ["eat","tea","tan","ate","nat","bat"]
    Output: [["bat"],["nat","tan"],["ate","eat","tea"]]

    Explanation:
    There is no string in strs that can be rearranged to form "bat".
    The strings "nat" and "tan" are anagrams as they can be rearranged to form each other.
    The strings "ate", "eat", and "tea" are anagrams as they can be rearranged to form each other.

    Example 2:

    Input: strs = [""]
    Output: [[""]]

    Example 3:

    Input: strs = ["a"]
    Output: [["a"]]

Constraints:

1 <= strs.length <= 104
0 <= strs[i].length <= 100
strs[i] consists of lowercase English letters.
"""

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        # Code solution below

        hashmap = defaultdict(list)

        for word in strs:
            count = [0] * 26
            for char in word:
                count[ord(char) - ord('a')] += 1

            hashmap[tuple(count)].append(word)
        return list(hashmap.values())
    
# Creates a dictionary where each key will map to a list of anagrams
# defaultdict(list) means if a key doesn't exist, it automatically creates an empty list

# Loop through each word in the input array

# Create an array of 26 zeros to count the frequency of each letter (a-z)
# Index 0 represents 'a', index 1 represents 'b', etc.

# Loop through each character in the current word

# Convert the character to its corresponding index (0-25)
# ord(char) gets the ASCII value of the character
# ord('a') gets the ASCII value of 'a'
# Subtracting them gives us 0 for 'a', 1 for 'b', 2 for 'c', etc.
# Increment the count at that index

# Convert the count array to a tuple (so it can be used as a dictionary key)
# and append the current word to the list of anagrams with that character frequency pattern
# Words with the same character frequencies are anagrams

# Return all the grouped anagram lists (the values from the hashmap)
# Each value is a list of words that are anagrams of each other