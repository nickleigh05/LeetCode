"""
347. Top K Frequent Elements

Medium

Given an integer array nums and an integer k, return the k most frequent elements. You may return the answer in any order.

    Example 1:

    Input: nums = [1,1,1,2,2,3], k = 2
    Output: [1,2]

    Example 2:

    Input: nums = [1], k = 1
    Output: [1]
 
Constraints:

1 <= nums.length <= 105
-104 <= nums[i] <= 104
k is in the range [1, the number of unique elements in the array].
It is guaranteed that the answer is unique.
 

Follow up: Your algorithm's time complexity must be better than O(n log n), where n is the array's size.
"""

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        count = {}
        freq = [[] for i in range(len(nums) + 1)]

        for num in nums:
            count[num] = 1 + count.get(num, 0)
        for num, cnt in count.items():
            freq[cnt].append(num)

        res = []
        for i in range(len(freq) - 1, 0, -1):
            for num in freq[i]:
                res.append(num)
                if len(res) == k:
                    return res
            
"""
My thought process:

The question asks me to find the k most frequent elements in an array. I need to count how 
many times each number appears, then use bucket sort to get the most frequent ones.

count = {}                           # this creates a dictionary to count frequencies
freq = [[] for _ in range(len(nums) + 1)]  # this creates buckets for each possible frequency

for num in nums:                     # this loop counts how often each number appears
    count[num] = 1 + count.get(num, 0)

for num, cnt in count.items():       # this loop puts numbers into frequency buckets
    freq[cnt].append(num)

Then I go through buckets from highest frequency to lowest, collecting k elements.

what is bucket sort? Bucket sort is a sorting algorithm that distributes elements into 
buckets based on their values, then processes buckets in order. Here we use frequency 
as the bucket index.

what is count.get(num, 0)? This gets the current count for num, or returns 0 if num 
isn't in the dictionary yet. Then we add 1 to increment the count.

###########################################################################################   

Claude's thought process:

1. Problem Analysis:
   - Count frequency of each element in array
   - Find the k elements with highest frequency
   - Must be better than O(n log n) time complexity
   - Bucket sort approach achieves O(n) time

2. Approach Options:
   a) Counter + most_common(): Uses heapq internally O(n + k log n)
   b) HashMap + Heap: Manual counting, use min-heap of size k O(n log k)  
   c) Bucket Sort: Count frequencies, sort by frequency using buckets O(n)

3. Optimal Solution (Bucket Sort - best time complexity):
   - Count all element frequencies using hashmap
   - Create frequency buckets (index = frequency, value = list of numbers)
   - Traverse buckets from highest to lowest frequency
   - Collect first k elements encountered

4. Why Bucket Sort Works Here:
   - Maximum frequency is at most n (length of array)
   - So we only need n+1 buckets (indices 0 to n)
   - Each number goes into exactly one bucket based on its frequency
   - Traverse from high frequency to low until we have k elements

###########################################################################################   

Time complexity breakdown:

Bucket Sort approach:
- Count frequencies: O(n) to iterate through nums once
- Fill frequency buckets: O(n) to iterate through count dictionary
- Traverse buckets for result: O(n) worst case, but stops early when we have k elements
- Total: O(n) time, O(n) space

Alternative approaches:
- Counter + most_common(): O(n + k log n) time, O(n) space
- Heap approach: O(n log k) time, O(k) space
- Bucket sort is optimal for time complexity O(n)

###########################################################################################   

Code solution breakdown line by line with inline comments and explanations

class Solution:
    # Define a class called Solution (LeetCode requirement)
    
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        # Function signature:
        # - self: reference to the instance
        # - nums: input list of integers to analyze
        # - k: number of top frequent elements to return
        # - -> List[int]: returns list of the k most frequent numbers
        
        count = {}
        # Create empty dictionary to store frequency count of each number
        # Key: number from nums, Value: how many times it appears
        # Example: {1: 3, 2: 2, 3: 1} means 1 appears 3 times, 2 appears 2 times, etc.
        
        freq = [[] for i in range(len(nums) + 1)]
        # Create frequency buckets - array of empty lists
        # Index represents frequency, list contains numbers with that frequency
        # Size is len(nums) + 1 because max frequency is len(nums)
        # Example: freq[3] = [1] means numbers with frequency 3 are [1]
        
        for num in nums:
            # Loop through each number in the input array
            count[num] = 1 + count.get(num, 0)
            # Increment the count for current number
            # count.get(num, 0) returns current count or 0 if not exists
            # Then we add 1 to increment the frequency
            # Example: if num=1 appears, count becomes {1: 1}, then {1: 2}, then {1: 3}
        
        for num, cnt in count.items():
            # Loop through each (number, frequency) pair in count dictionary
            freq[cnt].append(num)
            # Put the number into the bucket corresponding to its frequency
            # freq[cnt] is the list of numbers that appear cnt times
            # Example: if count = {1: 3, 2: 2, 3: 1}, then freq[3] = [1], freq[2] = [2], freq[1] = [3]

        res = []
        # Initialize empty result list to store our answer
        
        for i in range(len(freq) - 1, 0, -1):
            # Loop through frequency buckets from highest frequency to lowest
            # range(len(freq) - 1, 0, -1) goes from max frequency down to 1
            # We skip frequency 0 because numbers with 0 frequency don't exist in our array
            
            for num in freq[i]:
                # For each number in the current frequency bucket
                res.append(num)
                # Add the number to our result list
                
                if len(res) == k:
                    # Once we have k elements, we're done
                    return res
                    # Return immediately - no need to continue

# Example walkthrough with nums = [1,1,1,2,2,3], k = 2:
# Step 1: Count frequencies
#   count = {1: 3, 2: 2, 3: 1}
# Step 2: Fill frequency buckets
#   freq[3] = [1], freq[2] = [2], freq[1] = [3], freq[0] = []
# Step 3: Traverse from highest frequency
#   i=3: freq[3] = [1], res = [1], len(res) = 1 < k
#   i=2: freq[2] = [2], res = [1,2], len(res) = 2 == k, return [1,2]
# Result: [1, 2] (the two most frequent elements)
"""