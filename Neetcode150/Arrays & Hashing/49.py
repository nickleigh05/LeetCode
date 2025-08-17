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
        
        anagram_map = {}
        
        for s in strs:
            sorted_str = ''.join(sorted(s))
            if sorted_str in anagram_map:
                anagram_map[sorted_str].append(s)
            else:
                anagram_map[sorted_str] = [s]
        
        return list(anagram_map.values())
            
"""
My thought process:

The question is asking me to group strings that are anagrams of each other. Anagrams have the same 
characters but in different order. I need to find a way to identify which strings belong to the same group.

anagram_map = {}         # this line creates a dictionary to group anagrams together

what is a dictionary? A dictionary in Python is a collection of key-value pairs. It's mutable 
and allows for fast lookups, additions, and deletions of key-value pairs.

for s in strs:           # this line iterates through each string in the input array

sorted_str = ''.join(sorted(s))  # this line sorts the characters and creates a key for grouping

if sorted_str in anagram_map:    # this line checks if we've seen this pattern before
    anagram_map[sorted_str].append(s)  # if yes, add to existing group

else:                            # if no, create new group
    anagram_map[sorted_str] = [s]

return list(anagram_map.values())  # this line returns all the grouped anagrams as a list

###########################################################################################   

Claude's thought process:

1. Problem Analysis:
   - Need to group strings that are anagrams of each other
   - Anagrams contain same characters with same frequencies, just rearranged
   - Need to identify which strings belong together
   - Return groups as list of lists

2. Approach Options:
   a) Brute Force: Compare every string with every other string O(n² * m log m)
   b) Sorting: Sort characters in each string as key O(n * m log m)
   c) Character counting: Count frequency of each character O(n * m)

3. Optimal Solution (Sorting as Key):
   - Sort characters in each string to create a canonical form
   - Use sorted string as key in hash map
   - Group strings with same sorted form together
   - Return all groups

###########################################################################################   

Time complexity breakdown:

- Loop through strings: O(n) where n = number of strings
- Sort each string: O(m log m) where m = average length of strings
- Dictionary operations: O(1) average case per operation
- Total: O(n * m log m) time complexity

Space complexity: O(n * m) for storing all strings in the hash map

Alternative approaches:
- Brute force comparison: O(n² * m log m) time, O(n * m) space
- Character counting: O(n * m) time, O(n * m) space
- Sorting approach: O(n * m log m) time, O(n * m) space (good balance)

###########################################################################################   

Code solution breakdown line by line with inline comments and explanations

class Solution:
    # Define a class called Solution (LeetCode requirement)
    
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        # Function signature:
        # - self: reference to the instance
        # - strs: input list of strings to group
        # - -> List[List[str]]: returns list of anagram groups
        
        anagram_map = {}
        # Create empty dictionary to group anagrams
        # Key: sorted string (canonical form), Value: list of original strings
        # All anagrams will have the same sorted form
        # Example: anagram_map = {} (empty dict ready for grouping)
        
        for s in strs:
            # Iterate through each string in the input array
            # s represents the current string we're processing
            # Example: if strs = ["eat","tea","tan"], s will be "eat", then "tea", then "tan"
            
            sorted_str = ''.join(sorted(s))
            # Create canonical form by sorting characters in the string
            # sorted(s) returns list of characters in alphabetical order
            # ''.join() combines the characters back into a string
            # Example: "eat" → ['a','e','t'] → "aet"
            # Example: "tea" → ['a','e','t'] → "aet" (same as "eat"!)
            
            if sorted_str in anagram_map:
                # Check if we've already seen this canonical form
                # If yes, it means we found another anagram for existing group
                # Example: if "aet" already exists in map, we found another anagram
                
                anagram_map[sorted_str].append(s)
                # Add current string to the existing anagram group
                # The group already exists, just append new member
                # Example: anagram_map["aet"] = ["eat"] becomes ["eat", "tea"]
            else:
                # This is the first time seeing this canonical form
                # Create a new group with this string as the first member
                # Example: anagram_map["aet"] = ["eat"] (new group created)
                
                anagram_map[sorted_str] = [s]
                # Initialize new list with current string as first element
                # This creates a new anagram group
        
        return list(anagram_map.values())
        # Extract all the grouped lists from the dictionary
        # .values() gives us all the lists (anagram groups)
        # list() converts the dictionary values to a list
        # Example: returns [["eat","tea","ate"], ["tan","nat"], ["bat"]]

# Example walkthrough with strs = ["eat","tea","tan","ate","nat","bat"]:
# Initial: anagram_map = {}
# 
# s="eat": sorted_str="aet", not in map, anagram_map = {"aet": ["eat"]}
# s="tea": sorted_str="aet", IS in map, anagram_map = {"aet": ["eat","tea"]}
# s="tan": sorted_str="ant", not in map, anagram_map = {"aet": ["eat","tea"], "ant": ["tan"]}
# s="ate": sorted_str="aet", IS in map, anagram_map = {"aet": ["eat","tea","ate"], "ant": ["tan"]}
# s="nat": sorted_str="ant", IS in map, anagram_map = {"aet": ["eat","tea","ate"], "ant": ["tan","nat"]}
# s="bat": sorted_str="abt", not in map, anagram_map = {"aet": ["eat","tea","ate"], "ant": ["tan","nat"], "abt": ["bat"]}
# 
# Final return: [["eat","tea","ate"], ["tan","nat"], ["bat"]]
"""