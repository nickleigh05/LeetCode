"""
238. Product of Array Except Self

Medium

Hint
Given an integer array nums, return an array answer such that answer[i] is equal 
to the product of all the elements of nums except nums[i].

The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.

You must write an algorithm that runs in O(n) time and without using the division operation.

    Example 1:

    Input: nums = [1,2,3,4]
    Output: [24,12,8,6]

    Example 2:

    Input: nums = [-1,1,0,-3,3]
    Output: [0,0,9,0,0]
 
Constraints:

2 <= nums.length <= 105
-30 <= nums[i] <= 30
The input is generated such that answer[i] is guaranteed to fit in a 32-bit integer.
 

Follow up: Can you solve the problem in O(1) extra space complexity? (The output array does not count as extra space for space complexity analysis.)
"""

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        # Code solution below
        
        result = [1] * len(nums)
        
        prefix = 1
        for i in range(len(nums)):
            result[i] = prefix
            prefix *= nums[i]
        
        postfix = 1
        for i in range(len(nums) - 1, -1, -1):
            result[i] *= postfix
            postfix *= nums[i]
        
        return result
            
"""
My thought process:

The question is asking me to find the product of all elements in an array except for the element 
at each specific index. I cannot use division and need O(n) time complexity.

result = [1] * len(nums)     # this line creates an array filled with 1s, same length as input

prefix = 1                   # this variable tracks the product of all elements to the left
for i in range(len(nums)):   # this loop fills result with left products
    result[i] = prefix       # store the product of all elements to the left of i
    prefix *= nums[i]        # update prefix to include current element for next iteration

postfix = 1                  # this variable tracks the product of all elements to the right
for i in range(len(nums) - 1, -1, -1):  # this loop goes backwards through the array
    result[i] *= postfix     # multiply left product by right product to get final answer
    postfix *= nums[i]       # update postfix to include current element for next iteration

###########################################################################################   

Claude's thought process:

1. Problem Analysis:
   - Need product of all elements except current element at each index
   - Cannot use division operation
   - Must be O(n) time complexity
   - O(1) extra space preferred (output array doesn't count)

2. Approach Options:
   a) Brute Force: For each index, multiply all other elements O(n²)
   b) Division Approach: Total product ÷ current element (not allowed)
   c) Left/Right Products: Calculate left products, then multiply by right products O(n)

3. Optimal Solution (Left/Right Products):
   - First pass: Calculate product of all elements to the left of each index
   - Second pass: Calculate product of all elements to the right, multiply with left products
   - Use the result array to store left products, then modify in-place for space efficiency

###########################################################################################   

Time complexity breakdown:

- First loop (left products): O(n) where n = length of nums
- Second loop (right products): O(n) 
- Total: O(n) + O(n) = O(n) time complexity

Space complexity: O(1) extra space (output array doesn't count as extra space)

Alternative approaches:
- Brute force: O(n²) time, O(1) space
- Division method: O(n) time, O(1) space (but division not allowed)
- Two separate arrays: O(n) time, O(n) space (less space efficient)

###########################################################################################   

Code solution breakdown line by line with inline comments and explanations

class Solution:
    # Define a class called Solution (LeetCode requirement)
    
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        # Function signature:
        # - self: reference to the instance
        # - nums: input list of integers
        # - -> List[int]: returns list of products
        
        result = [1] * len(nums)
        # Create result array filled with 1s, same length as input
        # We use 1s because 1 is the multiplicative identity (1 * x = x)
        # This array will store our final answer
        # Example: if nums = [1,2,3,4], result = [1,1,1,1] initially
        
        prefix = 1
        # Variable to track the running product of elements to the left
        # Starts at 1 because there are no elements to the left of index 0
        # This accumulates the product as we move left to right
        
        for i in range(len(nums)):
            # First pass: fill result array with left products
            # For each position i, store product of all elements to its left
            
            result[i] = prefix
            # Store current left product at position i
            # At this point, prefix contains product of all elements left of index i
            # Example: when i=2, prefix contains nums[0] * nums[1]
            
            prefix *= nums[i]
            # Update prefix to include current element for next iteration
            # Now prefix will be used for the next position (i+1)
            # Example: if prefix was 2 and nums[i] is 3, prefix becomes 6
        
        postfix = 1
        # Variable to track the running product of elements to the right
        # Starts at 1 because there are no elements to the right of the last index
        # This accumulates the product as we move right to left
        
        for i in range(len(nums) - 1, -1, -1):
            # Second pass: traverse backwards and multiply by right products
            # range(len(nums)-1, -1, -1) goes from last index to 0
            # Example: if len(nums)=4, this goes 3, 2, 1, 0
            
            result[i] *= postfix
            # Multiply existing left product by right product
            # result[i] already contains left product from first pass
            # postfix contains product of all elements to the right of index i
            # Final result[i] = (left product) * (right product) = product except self
            
            postfix *= nums[i]
            # Update postfix to include current element for next iteration
            # Now postfix will be used for the previous position (i-1)
            # Example: if postfix was 12 and nums[i] is 4, postfix becomes 48
        
        return result
        # Return the final array where each element is the product of all others

# Example walkthrough with nums = [1,2,3,4]:

# Initial state:
# nums = [1,2,3,4], result = [1,1,1,1], prefix = 1

# First pass (left products):
# i=0: result[0] = prefix(1), prefix = 1*nums[0] = 1*1 = 1,  result = [1,1,1,1]
# i=1: result[1] = prefix(1), prefix = 1*nums[1] = 1*2 = 2,  result = [1,1,1,1]  
# i=2: result[2] = prefix(2), prefix = 2*nums[2] = 2*3 = 6,  result = [1,1,2,1]
# i=3: result[3] = prefix(6), prefix = 6*nums[3] = 6*4 = 24, result = [1,1,2,6]

# After first pass: result = [1,1,2,6] (left products)
# postfix = 1

# Second pass (right products, going backwards):
# i=3: result[3] *= postfix(1) = 6*1 = 6,  postfix = 1*nums[3] = 1*4 = 4,  result = [1,1,2,6]
# i=2: result[2] *= postfix(4) = 2*4 = 8,  postfix = 4*nums[2] = 4*3 = 12, result = [1,1,8,6]
# i=1: result[1] *= postfix(12) = 1*12 = 12, postfix = 12*nums[1] = 12*2 = 24, result = [1,12,8,6]
# i=0: result[0] *= postfix(24) = 1*24 = 24, postfix = 24*nums[0] = 24*1 = 24, result = [24,12,8,6]

# Final result = [24,12,8,6]
# Verification: 
# Index 0: 2*3*4 = 24 ✓ (all except nums[0]=1)
# Index 1: 1*3*4 = 12 ✓ (all except nums[1]=2) 
# Index 2: 1*2*4 = 8 ✓  (all except nums[2]=3)
# Index 3: 1*2*3 = 6 ✓  (all except nums[3]=4)

# Example walkthrough with nums = [-1,1,0,-3,3]:

# First pass (left products):
# result = [1, -1, -1, 0, 0] (left products)

# Second pass (right products):
# Final result = [0,0,9,0,0]
# The 0 in the original array causes most results to be 0
# Only index 2 has non-zero result because the 0 is excluded from that calculation
"""
        