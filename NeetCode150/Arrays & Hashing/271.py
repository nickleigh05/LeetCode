"""
Encode and Decode Strings

Medium

Design an algorithm to encode a list of strings to a single string. 
The encoded string is then decoded back to the original list of strings.

Please implement encode and decode

        Example 1:

        Input: ["neet","code","love","you"]

        Output:["neet","code","love","you"]

        Example 2:

        Input: ["we","say",":","yes"]

        Output: ["we","say",":","yes"]

Constraints:

    0 <= strs.length < 100
    0 <= strs[i].length < 200
    strs[i] contains only UTF-8 characters.

"""

class Solution:

    def encode(self, strs: List[str]) -> str:
        # Code solution below

        result = ""
        for s in strs:
            result += str(len(s)) + "#" + s
        return result

    def decode(self, s: str) -> List[str]:
        # Code solution below

        result = []
        i = 0

        while i < len(s):
            # Find the delimiter
            j = i
            while s[j] != "#":
                j += 1

            # Get the length
            length = int(s[i:j])

            # Extract the string
            result.append(s[j + 1:j + 1 + length])

            # Move to next string
            i = j + 1 + length

        return result

"""
My thought process:

The question is asking me to encode a list of strings into a single string, then decode it back.
I need to handle edge cases like strings that contain delimiters.

ENCODE:
result = ""               # this line creates empty string to build result
for s in strs:            # this line loops through each string in the list
    result += str(len(s)) + "#" + s  # this line adds length + delimiter + string

what is the format? I use "length#string" format where # is delimiter
Example: ["neet","code"] becomes "4#neet4#code"

DECODE:
result = []               # this line creates empty list for decoded strings
i = 0                     # this line tracks current position in encoded string

while i < len(s):         # this line loops until we've processed entire string
    j = i                 # this line finds start of length number
    while s[j] != "#":    # this line finds the delimiter position
        j += 1

    length = int(s[i:j])  # this line extracts length as integer
    result.append(s[j + 1:j + 1 + length])  # this line extracts string of exact length
    i = j + 1 + length    # this line moves to next encoded string

###########################################################################################

Claude's thought process:

1. Problem Analysis:
   - Encode: Convert list of strings to single string
   - Decode: Convert single string back to original list
   - Must handle special characters, empty strings, strings with delimiters
   - Need unambiguous encoding scheme

2. Approach Options:
   a) Use simple delimiter: Fails if strings contain the delimiter
   b) Escape special characters: Complex and error-prone
   c) Length-prefixed encoding: Use "length#string" format

3. Optimal Solution (Length-Prefixed):
   - Encode: For each string, prepend its length followed by delimiter
   - Decode: Read length, skip delimiter, extract exact number of characters
   - No conflicts since we know exact boundaries

###########################################################################################

Time complexity breakdown:

Encode:
- Loop through all strings: O(n) where n = number of strings
- String concatenation: O(m) where m = total length of all strings
- Total: O(n + m) time complexity

Decode:
- Loop through encoded string once: O(m) where m = length of encoded string
- String slicing operations: O(k) per string where k = length of individual string
- Total: O(m) time complexity

Space complexity: O(m) for storing result

Alternative approaches:
- JSON encoding: O(m) time but adds overhead
- Base64 encoding: O(m) time but increases size
- Length-prefixed: O(m) time, minimal overhead (optimal)

###########################################################################################

Code solution breakdown line by line with inline comments and explanations

class Solution:
    # Define a class called Solution (LeetCode requirement)

    def encode(self, strs: List[str]) -> str:
        # Function to encode list of strings into single string
        # - strs: input list of strings to encode
        # - returns: single encoded string

        result = ""
        # Initialize empty string to build our encoded result
        # We'll concatenate each encoded string to this

        for s in strs:
            # Iterate through each string in the input list
            # Process one string at a time

            result += str(len(s)) + "#" + s
            # Encode current string using length-prefixed format:
            # 1. str(len(s)): Convert string length to string representation
            # 2. "#": Use hash as delimiter between length and content
            # 3. s: Append the actual string content
            # Example: "neet" becomes "4#neet"

        return result
        # Return the complete encoded string
        # Example: ["neet","code"] becomes "4#neet4#code"

    def decode(self, s: str) -> List[str]:
        # Function to decode single string back to list of strings
        # - s: encoded string to decode
        # - returns: original list of strings

        result = []
        # Initialize empty list to store decoded strings

        i = 0
        # Pointer to track current position in encoded string
        # We'll move this as we decode each string

        while i < len(s):
            # Continue until we've processed the entire encoded string
            # Each iteration decodes one string

            j = i
            # Start searching for delimiter from current position

            while s[j] != "#":
                # Find the delimiter that separates length from content
                # Keep moving j until we hit the "#" character
                j += 1

            length = int(s[i:j])
            # Extract the length number from position i to j
            # Convert string representation back to integer
            # Example: "4" becomes integer 4

            result.append(s[j + 1:j + 1 + length])
            # Extract the actual string content:
            # - j + 1: Start after the "#" delimiter
            # - j + 1 + length: End after exactly 'length' characters
            # This ensures we get the exact string regardless of its content

            i = j + 1 + length
            # Move pointer to start of next encoded string
            # Skip over the delimiter and the string we just decoded

        return result
        # Return the list of decoded strings

# Example walkthrough with encode(["neet","code","love","you"]):
# s="neet": len=4, result="" + "4#neet" = "4#neet"
# s="code": len=4, result="4#neet" + "4#code" = "4#neet4#code"
# s="love": len=4, result="4#neet4#code" + "4#love" = "4#neet4#code4#love"
# s="you": len=3, result="4#neet4#code4#love" + "3#you" = "4#neet4#code4#love3#you"

# Example walkthrough with decode("4#neet4#code4#love3#you"):
# i=0: find "#" at j=1, length=int("4")=4, extract s[2:6]="neet", i=6
# i=6: find "#" at j=7, length=int("4")=4, extract s[8:12]="code", i=12
# i=12: find "#" at j=13, length=int("4")=4, extract s[14:18]="love", i=18
# i=18: find "#" at j=19, length=int("3")=3, extract s[20:23]="you", i=23
# Result: ["neet","code","love","you"]
"""
