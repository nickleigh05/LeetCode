"""
242. Valid Anagram

Easy

Given two strings s and t, return true if t is an anagram of s, and false otherwise.

    Example 1:

    Input: s = "anagram", t = "nagaram"
    Output: true

    Example 2:

    Input: s = "rat", t = "car"
    Output: false

    Constraints:
    1 <= s.length, t.length <= 5 * 104
    s and t consist of lowercase English letters.
 
Follow up: What if the inputs contain Unicode characters? How would you adapt your solution to such a case?
"""

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        # Code solution below
        
        if len(s) != len(t):
            return False
        
        countS = {}
        countT = {}
        
        for i in range(len(s)):
            countS[s[i]] = 1 + countS.get(s[i], 0)
            countT[t[i]] = 1 + countT.get(t[i], 0)
        
        return countS == countT
            
"""
My thought process:

The question is asking me to check if two strings are anagrams of each other. Two strings are 
anagrams if they contain the same characters with the same frequency, just rearranged.

if len(s) != len(t):     # this line checks if the strings have different lengths
    return False         # if they do, they can't be anagrams

countS = {}              # this line creates a dictionary to count characters in string s
countT = {}              # this line creates a dictionary to count characters in string t

what is a dictionary? A dictionary in Python is a collection of key-value pairs. It's mutable 
and allows for fast lookups, additions, and deletions of key-value pairs.

for i in range(len(s)):  # this line uses a for loop to iterate through both strings simultaneously

countS[s[i]] = 1 + countS.get(s[i], 0)  # this line counts each character in string s
countT[t[i]] = 1 + countT.get(t[i], 0)  # this line counts each character in string t

return countS == countT  # this line compares the two dictionaries to see if they're equal

###########################################################################################   

Claude's thought process:

1. Problem Analysis:
   - Need to check if two strings contain the same characters with same frequencies
   - Anagrams have identical character counts but different arrangements
   - "anagram" and "nagaram" → both have: a:3, n:1, g:1, r:1, m:1

2. Approach Options:
   a) Sorting: Sort both strings and compare O(n log n)
   b) Character counting: Count frequency of each character O(n)
   c) Array counting: Use fixed-size array for lowercase letters O(n)

3. Optimal Solution (Character Counting):
   - If strings have different lengths, they can't be anagrams
   - Count frequency of each character in both strings
   - Compare the frequency dictionaries
   - If identical, strings are anagrams

###########################################################################################   

Time complexity breakdown:

- Length check: O(1)
- Loop through strings: O(n) where n = length of strings
- Dictionary operations (get and set): O(1) average case per operation
- Dictionary comparison: O(k) where k = number of unique characters
- Total: O(n) time complexity

Space complexity: O(k) where k = number of unique characters (at most 26 for lowercase letters)

Alternative approaches:
- Sorting approach: O(n log n) time, O(n) space
- Array counting: O(n) time, O(1) space (using fixed array of size 26)
- Dictionary approach: O(n) time, O(k) space (optimal balance)

###########################################################################################   

Code solution breakdown line by line with inline comments and explanations

class Solution:
    # Define a class called Solution (LeetCode requirement)
    
    def isAnagram(self, s: str, t: str) -> bool:
        # Function signature:
        # - self: reference to the instance
        # - s: first input string
        # - t: second input string  
        # - -> bool: returns True if anagrams, False otherwise
        
        if len(s) != len(t):
            # Quick optimization: if strings have different lengths, they can't be anagrams
            # This saves us from unnecessary character counting
            # Example: "abc" (len=3) and "abcd" (len=4) → immediately return False
            return False
        
        countS = {}
        countT = {}
        # Create two empty dictionaries to store character frequencies
        # countS will track character counts in string s
        # countT will track character counts in string t
        # Example: countS = {}, countT = {} (empty dicts ready to store counts)
        
        for i in range(len(s)):
            # Loop through both strings simultaneously using index i
            # Since we already confirmed they have same length, one loop works for both
            # Example: if s="anagram", i will be 0,1,2,3,4,5,6
            
            countS[s[i]] = 1 + countS.get(s[i], 0)
            # Count character at position i in string s
            # .get(s[i], 0) returns current count or 0 if character not seen before
            # Add 1 to the current count (or 0 if first time seeing this character)
            # Example: s[0]='a', countS becomes {'a': 1}
            
            countT[t[i]] = 1 + countT.get(t[i], 0)
            # Count character at position i in string t using same logic
            # Example: t[0]='n', countT becomes {'n': 1}
        
        return countS == countT
        # Compare the two frequency dictionaries
        # Python's == operator compares dictionaries key by key and value by value
        # Returns True if both dicts have identical key-value pairs, False otherwise
        # This tells us if both strings have the same character frequencies

# Example walkthrough with s="anagram", t="nagaram":
# Initial: countS={}, countT={}
# i=0: s[0]='a', t[0]='n' → countS={'a':1}, countT={'n':1}
# i=1: s[1]='n', t[1]='a' → countS={'a':1,'n':1}, countT={'n':1,'a':1}
# i=2: s[2]='a', t[2]='g' → countS={'a':2,'n':1}, countT={'n':1,'a':1,'g':1}
# i=3: s[3]='g', t[3]='a' → countS={'a':2,'n':1,'g':1}, countT={'n':1,'a':2,'g':1}
# i=4: s[4]='r', t[4]='r' → countS={'a':2,'n':1,'g':1,'r':1}, countT={'n':1,'a':2,'g':1,'r':1}
# i=5: s[5]='a', t[5]='a' → countS={'a':3,'n':1,'g':1,'r':1}, countT={'n':1,'a':3,'g':1,'r':1}
# i=6: s[6]='m', t[6]='m' → countS={'a':3,'n':1,'g':1,'r':1,'m':1}, countT={'n':1,'a':3,'g':1,'r':1,'m':1}
# Final comparison: countS == countT → True (same character frequencies!)
"""
