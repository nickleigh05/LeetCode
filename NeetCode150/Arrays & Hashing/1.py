"""
1. Two Sum

Easy

Hint
Given an array of integers nums and an integer target, return indices of the two 
numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not 
use the same element twice.

You can return the answer in any order.

    Example 1:

    Input: nums = [2,7,11,15], target = 9
    Output: [0,1]
    Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

    Example 2:
    Input: nums = [3,2,4], target = 6
    Output: [1,2]

    Example 3:
    Input: nums = [3,3], target = 6
    Output: [0,1]
 
Constraints:

2 <= nums.length <= 104
-109 <= nums[i] <= 109
-109 <= target <= 109
Only one valid answer exists.

Follow-up: Can you come up with an algorithm that is less than O(n2) time complexity?
"""

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # Code solution below
        
        prevMap = {}
        
        for i, n in enumerate(nums):
            diff = target - n
            if diff in prevMap:
                return [prevMap[diff], i]
            prevMap[n] = i
            
"""
My thought process:

The question is asking me to find two numbers in an array that add up to a target value and 
return their indices. I need to find the positions of these two numbers, not the numbers themselves.

prevMap = {}             # this line creates a dictionary to store numbers and their indices

what is a dictionary? A dictionary in Python is a collection of key-value pairs. It's mutable 
and allows for fast lookups, additions, and deletions of key-value pairs.

for i, n in enumerate(nums):  # this line uses enumerate to get both index and value from the array

diff = target - n        # this line calculates what number we need to find to reach the target

if diff in prevMap:      # this line checks if the complement number already exists in our map
    return [prevMap[diff], i]  # if found, return the indices of both numbers

prevMap[n] = i           # this line stores the current number and its index for future lookups

###########################################################################################   

Claude's thought process:

1. Problem Analysis:
   - Need to find two numbers that sum to target
   - Return their indices, not the values
   - Exactly one solution exists
   - Cannot use same element twice

2. Approach Options:
   a) Brute Force: Check every pair of numbers O(n²)
   b) Hash Map: Store complements and check for matches O(n)
   c) Two Pointer: Sort first, then use two pointers O(n log n)

3. Optimal Solution (Hash Map):
   - For each number, calculate its complement (target - number)
   - Check if complement already exists in our map
   - If yes: found our pair, return indices
   - If no: store current number and index for future reference

###########################################################################################   

Time complexity breakdown:

- Loop through array: O(n) where n = length of nums
- Dictionary operations (lookup and insert): O(1) average case per operation
- Total: O(n) * O(1) = O(n) time complexity

Space complexity: O(n) worst case when no solution found until the end

Alternative approaches:
- Brute force: O(n²) time, O(1) space
- Two pointer: O(n log n) time, O(1) space
- Hash map approach: O(n) time, O(n) space (optimal for time)

###########################################################################################   

Code solution breakdown line by line with inline comments and explanations

class Solution:
    # Define a class called Solution (LeetCode requirement)
    
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # Function signature:
        # - self: reference to the instance
        # - nums: input list of integers
        # - target: the sum we're looking for
        # - -> List[int]: returns list of two indices
        
        prevMap = {}
        # Create an empty dictionary to store numbers we've seen and their indices
        # Key: the number value, Value: its index in the array
        # This allows O(1) lookup to find complements
        # Example: prevMap = {} (empty dict ready to store number -> index mappings)
        
        for i, n in enumerate(nums):
            # Loop through array with both index (i) and value (n)
            # enumerate() gives us (index, value) pairs
            # Example: if nums = [2,7,11,15], we get (0,2), (1,7), (2,11), (3,15)
            
            diff = target - n
            # Calculate the complement number we need to find
            # If current number is n, we need (target - n) to reach our target
            # Example: if target=9 and n=2, we need diff=7 to get 2+7=9
            
            if diff in prevMap:
                # Check if the complement already exists in our dictionary
                # This means we found our pair!
                # Example: if diff=7 and prevMap contains 7, we found our solution
                
                return [prevMap[diff], i]
                # Return indices of both numbers that sum to target
                # prevMap[diff] gives us the index where we saw the complement
                # i is the current index
                # Example: return [0, 1] if complement was at index 0 and current at index 1
            
            prevMap[n] = i
            # Store current number and its index for future reference
            # Only executed if we haven't found our solution yet
            # Future iterations can check if they need this current number
            # Example: prevMap[2] = 0 means number 2 is at index 0

# Example walkthrough with nums = [2,7,11,15], target = 9:
# Iteration 1: i=0, n=2, diff=9-2=7, 7 not in prevMap={}, store prevMap={2:0}
# Iteration 2: i=1, n=7, diff=9-7=2, 2 IS in prevMap={2:0}, return [0,1]
# Solution found: indices 0 and 1 contain numbers 2 and 7 which sum to 9!

# Example walkthrough with nums = [3,2,4], target = 6:
# Iteration 1: i=0, n=3, diff=6-3=3, 3 not in prevMap={}, store prevMap={3:0}
# Iteration 2: i=1, n=2, diff=6-2=4, 4 not in prevMap={3:0}, store prevMap={3:0, 2:1}
# Iteration 3: i=2, n=4, diff=6-4=2, 2 IS in prevMap={3:0, 2:1}, return [1,2]
# Solution found: indices 1 and 2 contain numbers 2 and 4 which sum to 6!
"""