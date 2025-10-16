"""
167. Two Sum II - Input Array Is Sorted

Medium

Given a 1-indexed array of integers numbers that is already sorted in non-decreasing order, find two numbers such that they add up to a specific target number. Let these two numbers be numbers[index1] and numbers[index2] where 1 <= index1 < index2 <= numbers.length.

Return the indices of the two numbers, index1 and index2, added by one as an integer array [index1, index2] of length 2.

The tests are generated such that there is exactly one solution. You may not use the same element twice.

Your solution must use only constant extra space.

        Example 1:

        Input: numbers = [2,7,11,15], target = 9
        Output: [1,2]
        Explanation: The sum of 2 and 7 is 9. Therefore, index1 = 1, index2 = 2. We return [1, 2].

        Example 2:

        Input: numbers = [2,3,4], target = 6
        Output: [1,3]
        Explanation: The sum of 2 and 4 is 6. Therefore index1 = 1, index2 = 3. We return [1, 3].

        Example 3:

        Input: numbers = [-1,0], target = -1
        Output: [1,2]
        Explanation: The sum of -1 and 0 is -1. Therefore index1 = 1, index2 = 2. We return [1, 2].

Constraints:

    2 <= numbers.length <= 3 * 104
    -1000 <= numbers[i] <= 1000
    numbers is sorted in non-decreasing order.
    -1000 <= target <= 1000
    The tests are generated such that there is exactly one solution.

"""

from typing import List

class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        # TODO: Implement your solution here
        # Hint: Use two pointers approach - one at the start, one at the end
        left = 0
        right = len(numbers) - 1

        while left < right:
            current_sum = numbers[left] + numbers[right]
            if current_sum == target:
                return [left + 1, right + 1]
            elif current_sum < target:
                left += 1
            else: 
                right -= 1
        pass























































# Test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1: Example from problem
    numbers1 = [2, 7, 11, 15]
    target1 = 9
    result1 = solution.twoSum(numbers1, target1)
    print(f"Test 1: numbers = {numbers1}, target = {target1}")
    print(f"Output: {result1}")
    print(f"Expected: [1, 2]")
    print(f"Pass: {result1 == [1, 2]}\n")

    # Test case 2: Example from problem
    numbers2 = [2, 3, 4]
    target2 = 6
    result2 = solution.twoSum(numbers2, target2)
    print(f"Test 2: numbers = {numbers2}, target = {target2}")
    print(f"Output: {result2}")
    print(f"Expected: [1, 3]")
    print(f"Pass: {result2 == [1, 3]}\n")

    # Test case 3: Example from problem (negative numbers)
    numbers3 = [-1, 0]
    target3 = -1
    result3 = solution.twoSum(numbers3, target3)
    print(f"Test 3: numbers = {numbers3}, target = {target3}")
    print(f"Output: {result3}")
    print(f"Expected: [1, 2]")
    print(f"Pass: {result3 == [1, 2]}\n")

    # Test case 4: Larger array
    numbers4 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    target4 = 17
    result4 = solution.twoSum(numbers4, target4)
    print(f"Test 4: numbers = {numbers4}, target = {target4}")
    print(f"Output: {result4}")
    print(f"Expected: [7, 10]")
    print(f"Pass: {result4 == [7, 10]}\n")

    # Test case 5: Two elements at the beginning
    numbers5 = [1, 3, 5, 7, 9]
    target5 = 4
    result5 = solution.twoSum(numbers5, target5)
    print(f"Test 5: numbers = {numbers5}, target = {target5}")
    print(f"Output: {result5}")
    print(f"Expected: [1, 2]")
    print(f"Pass: {result5 == [1, 2]}\n")

    # Test case 6: Two elements at the end
    numbers6 = [1, 2, 3, 4, 5]
    target6 = 9
    result6 = solution.twoSum(numbers6, target6)
    print(f"Test 6: numbers = {numbers6}, target = {target6}")
    print(f"Output: {result6}")
    print(f"Expected: [4, 5]")
    print(f"Pass: {result6 == [4, 5]}\n")

    # Test case 7: Negative and positive numbers
    numbers7 = [-10, -5, 0, 5, 10]
    target7 = 0
    result7 = solution.twoSum(numbers7, target7)
    print(f"Test 7: numbers = {numbers7}, target = {target7}")
    print(f"Output: {result7}")
    print(f"Expected: [1, 5] or [2, 4]")
    print(f"Pass: {result7 == [1, 5] or result7 == [2, 4]}\n")

    # Test case 8: Duplicate values
    numbers8 = [1, 2, 2, 3, 4]
    target8 = 4
    result8 = solution.twoSum(numbers8, target8)
    print(f"Test 8: numbers = {numbers8}, target = {target8}")
    print(f"Output: {result8}")
    print(f"Expected: [2, 3] (using the two 2's) or [1, 4]")
    print(f"Pass: {result8 == [2, 3] or result8 == [1, 4]}\n")
