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
"""

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        # Code solution below

        hashmap = {}

        for num in nums:
            hashmap[num] = hashmap.get(num, 0) + 1

        buckets = [[] for _ in range(len(nums) + 1)]

        for num, freq in hashmap.items():
            buckets[freq].append(num)
        
        result = []
        for i in range(len(buckets) - 1, 0, -1):
            for num in buckets[i]:
                result.append(num)
                if len(result) == k:
                    return result
        
        return result
    
# Creates an empty dictionary to count the frequency of each number

# Loop through each number in the nums array
# hashmap.get(num, 0) gets the current count of num, or 0 if it doesn't exist yet
# Add 1 to that count and store it back in hashmap

# Create a list of empty lists (buckets) where index represents frequency
# buckets[i] will contain all numbers that appear i times
# Size is len(nums) + 1 because max frequency can be len(nums) (all elements are the same)

# Loop through each number and its frequency in the hashmap
# Place each number into the bucket corresponding to its frequency
# For example, if a number appears 3 times, it goes into buckets[3]

# Create an empty list to store our final result

# Loop through buckets from highest frequency to lowest
# range(len(buckets) - 1, 0, -1) starts from the last index and goes down to 1
# We skip index 0 because frequency can't be 0

# Loop through all numbers in the current frequency bucket

# Add the number to our result list

# If we've collected k elements, we're done - return the result

# Return the result (in case we collected all elements without hitting k early)