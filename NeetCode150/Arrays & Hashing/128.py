"""
128. Longest Consecutive Sequence

Medium

Given an unsorted array of integers nums, return the length of the longest consecutive elements sequence.

You must write an algorithm that runs in O(n) time.

        Example 1:

        Input: nums = [100,4,200,1,3,2]
        Output: 4
        Explanation: The longest consecutive elements sequence is [1, 2, 3, 4]. 
        Therefore its length is 4.

        Example 2:

        Input: nums = [0,3,7,2,5,8,4,6,0,1]
        Output: 9

        Example 3:

        Input: nums = [1,0,1,2]
        Output: 3

Constraints:

    0 <= nums.length <= 105
    -109 <= nums[i] <= 109

"""

class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        # Code solution below

        if not nums:
            return 0

        num_set = set(nums)
        longest = 0

        for num in num_set:
            # Only start counting from potential beginning of sequence
            if num - 1 not in num_set:
                current_num = num
                current_length = 1

                # Keep extending the sequence
                while current_num + 1 in num_set:
                    current_num += 1
                    current_length += 1

                longest = max(longest, current_length)

        return longest

"""
My thought process:

The question is asking me to find the longest consecutive sequence in an unsorted array.
I need to do this in O(n) time, so I can't sort the array first.

if not nums:              # this line handles the edge case of empty array
    return 0

num_set = set(nums)       # this line converts array to set for O(1) lookups

what is a set? A set in Python is an unordered collection of unique elements that allows
for fast O(1) average case lookups, additions, and removals.

longest = 0               # this line tracks the maximum sequence length found

for num in num_set:       # this line iterates through unique numbers

if num - 1 not in num_set: # this line checks if current number is start of a sequence

current_num = num         # this line starts counting from current number
current_length = 1        # this line initializes length counter

while current_num + 1 in num_set: # this line extends sequence while consecutive numbers exist
    current_num += 1      # this line moves to next consecutive number
    current_length += 1   # this line increments sequence length

longest = max(longest, current_length) # this line updates maximum length found

###########################################################################################

Claude's thought process:

1. Problem Analysis:
   - Find longest consecutive sequence (like 1,2,3,4)
   - Must be O(n) time complexity (can't sort)
   - Numbers don't need to be adjacent in original array
   - Need to handle duplicates and negative numbers

2. Approach Options:
   a) Sort first: O(n log n) - violates time constraint
   b) Hash Set: Convert to set, find sequence starts, extend sequences O(n)

3. Optimal Solution (Hash Set):
   - Convert array to set for O(1) lookups
   - For each number, check if it's the start of a sequence
   - If it's a start (no num-1 exists), count how long sequence extends
   - Track maximum sequence length found

###########################################################################################

Time complexity breakdown:

- Convert to set: O(n) where n = length of nums
- Loop through unique numbers: O(n) in worst case
- For each sequence start, extend sequence: O(n) total across all sequences
- Each number is visited at most twice (once as start, once as extension)
- Total: O(n) time complexity

Space complexity: O(n) for the set storing unique numbers

Alternative approaches:
- Sorting approach: O(n log n) time, O(1) space
- Hash set approach: O(n) time, O(n) space (optimal for time requirement)

###########################################################################################

Code solution breakdown line by line with inline comments and explanations

class Solution:
    # Define a class called Solution (LeetCode requirement)

    def longestConsecutive(self, nums: List[int]) -> int:
        # Function signature:
        # - self: reference to the instance
        # - nums: input list of integers (can be unsorted)
        # - -> int: returns length of longest consecutive sequence

        if not nums:
            # Handle edge case of empty array
            # If no numbers provided, longest sequence is 0
            return 0

        num_set = set(nums)
        # Convert array to set for O(1) lookup operations
        # Removes duplicates automatically and enables fast membership testing
        # Example: [100,4,200,1,3,2] becomes {1,2,3,4,100,200}

        longest = 0
        # Track the maximum consecutive sequence length found so far
        # Initialize to 0 since we haven't found any sequences yet

        for num in num_set:
            # Iterate through each unique number in our set
            # We use set instead of original array to avoid checking duplicates

            if num - 1 not in num_set:
                # Check if current number is the START of a consecutive sequence
                # If num-1 doesn't exist, then num is potentially the beginning
                # This optimization ensures we only start counting from sequence beginnings
                # Example: for sequence [1,2,3,4], we only start counting from 1, not 2,3,4

                current_num = num
                # Set starting point for our sequence extension
                # This will be incremented as we find consecutive numbers

                current_length = 1
                # Initialize length counter for current sequence
                # Starts at 1 because current number counts as length 1

                while current_num + 1 in num_set:
                    # Keep extending sequence while consecutive numbers exist
                    # Check if next number (current_num + 1) is in our set
                    # Example: if current_num=1 and 2 is in set, continue sequence

                    current_num += 1
                    # Move to next consecutive number
                    # This extends our sequence by one position

                    current_length += 1
                    # Increment sequence length counter
                    # Track how many consecutive numbers we've found

                longest = max(longest, current_length)
                # Update maximum sequence length if current sequence is longer
                # Keep track of the best (longest) sequence found so far

        return longest
        # Return the length of the longest consecutive sequence found

# Example walkthrough with nums = [100,4,200,1,3,2]:
# num_set = {1,2,3,4,100,200}
#
# Check num=1: (1-1=0) not in set, so 1 is sequence start
#   current_num=1, length=1
#   1+1=2 in set: current_num=2, length=2
#   2+1=3 in set: current_num=3, length=3
#   3+1=4 in set: current_num=4, length=4
#   4+1=5 not in set: stop, longest=max(0,4)=4
#
# Check num=2: (2-1=1) IS in set, so 2 is not sequence start, skip
# Check num=3: (3-1=2) IS in set, so 3 is not sequence start, skip
# Check num=4: (4-1=3) IS in set, so 4 is not sequence start, skip
# Check num=100: (100-1=99) not in set, so 100 is sequence start
#   current_num=100, length=1
#   100+1=101 not in set: stop, longest=max(4,1)=4
# Check num=200: (200-1=199) not in set, so 200 is sequence start
#   current_num=200, length=1
#   200+1=201 not in set: stop, longest=max(4,1)=4
#
# Return longest=4 (sequence [1,2,3,4])
"""