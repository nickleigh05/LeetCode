"""
217. Contains Duplicate

Easy

Given an integer array nums, return true if any value appears at least 
twice in the array, and return false if every element is distinct.

    Example 1:

    Input: nums = [1,2,3,1]
    Output: true

    Explanation:
    The element 1 occurs at the indices 0 and 3.

    Example 2:

    Input: nums = [1,2,3,4]
    Output: false

    Explanation:
    All elements are distinct.

    Example 3:

    Input: nums = [1,1,1,3,3,4,3,2,4,2]
    Output: true

Constraints:
1 <= nums.length <= 10^5
-10^9 <= nums[i] <= 10^9
"""

class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        # Code solution below

        seen = set()
        
        for num in nums:
            if num in seen:
                return True
            seen.add(num)
        
        return False
            
"""
My thought process:

the question is asking me to check an array of numbers, if a number appears more than once 
than i can return true if not return false. if i return false that means each number within 
the array is unique.

seen = set()          # this line creates a set called seen

what is a set? A set in Python is an unordered collection of unique elements. It is a mutable 
data type, meaning elements can be added or removed after creation, but the elements themselves 
must be immutable

for num in nums:      # this line uses a for loop to iterate through nums we are creating a loop variable called num to go through the nums

if num in seen:       # the line uses an if statement to check if the loop varaiable we created called num is in seen

return True           # this line returns True if the if statements is True 

seen.add(num)         # this line is adding the num to the seen set

return False          # this line returns false if the for loops doesnt return True

###########################################################################################   

Claude's thought process:

1. Problem Analysis:
   - Need to detect if any number appears more than once
   - Return True if duplicate exists, False if all unique
   - Need efficient lookup to check if we've seen a number before

2. Approach Options:
   a) Brute Force: Compare each element with every other element O(n²)
   b) Sorting: Sort array, check adjacent elements O(n log n)
   c) Hash Set: Use set for O(1) average lookup time O(n)

3. Optimal Solution (Hash Set):
   - Iterate through array once
   - For each number, check if already in set
   - If yes: duplicate found, return True
   - If no: add to set and continue
   - If loop completes: no duplicates, return False

###########################################################################################   

Time complexity breakdown:

- Loop through array: O(n) where n = length of nums
- Set operations (lookup and add): O(1) average case per operation
- Total: O(n) * O(1) = O(n) time complexity

Space complexity: O(n) worst case when all elements are unique

Alternative approaches:
- Brute force: O(n²) time, O(1) space
- Sorting: O(n log n) time, O(1) space
- Set approach: O(n) time, O(n) space (optimal for time)

###########################################################################################   

Code solution breakdown line by line with inline comments and explanations

class Solution:
    # Define a class called Solution (LeetCode requirement)
    
    def containsDuplicate(self, nums: List[int]) -> bool:
        # Function signature:
        # - self: reference to the instance
        # - nums: input list of integers
        # - -> bool: returns True or False
        
        seen = set()
        # Create an empty set to store numbers we've already encountered
        # Why set? Sets have O(1) average lookup time vs O(n) for lists
        # Example: seen = {} (empty set ready to store unique values)
        
        for num in nums:
            # Loop through each number in the input array
            # num is our loop variable that takes each value one by one
            # Example: if nums = [1,2,3,1], num will be 1, then 2, then 3, then 1
            
            if num in seen:
                # Check if current number already exists in our seen set
                # This is where we detect the duplicate!
                # Example: when num=1 (second time), it's already in seen={1,2,3}
                
                return True
                # IMMEDIATELY return True when we find our first duplicate
                # No need to continue checking - we found what we're looking for
                
            seen.add(num)
            # Add current number to our seen set for future reference
            # Only executed if num was NOT already in seen
            # Example: seen starts {}, becomes {1}, then {1,2}, then {1,2,3}
        
        return False
        # If we've checked ALL numbers and found no duplicates, return False
        # This line only executes if the loop completes without finding duplicates
        # Meaning every element in the array is unique

# Example walkthrough with nums = [1,2,3,1]:
# Iteration 1: num=1, seen={}, 1 not in seen, add 1, seen={1}
# Iteration 2: num=2, seen={1}, 2 not in seen, add 2, seen={1,2}  
# Iteration 3: num=3, seen={1,2}, 3 not in seen, add 3, seen={1,2,3}
# Iteration 4: num=1, seen={1,2,3}, 1 IS in seen, return True (duplicate found!)
"""