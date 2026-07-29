"""

1089. Duplicate Zeros

Easy

Given a fixed-length integer array arr, duplicate each occurrence of zero, shifting the remaining elements to the right.

Note that elements beyond the length of the original array are not written. Do the above modifications to the input array in place and do not return anything.

Example 1:

    Input: arr = [1,0,2,3,0,4,5,0]
    Output: [1,0,0,2,3,0,0,4]
    Explanation: After calling your function, the input array is modified to: [1,0,0,2,3,0,0,4]

Example 2:

    Input: arr = [1,2,3]
    Output: [1,2,3]
    Explanation: After calling your function, the input array is modified to: [1,2,3]

Constraints:

    1 <= arr.length <= 104
    0 <= arr[i] <= 9

"""

class Solution:
    def duplicateZeros(self, arr: List[int]) -> None:
        """
        Do not return anything, modify arr in-place instead.
        """

        n = len(arr)
        i = 0

        while i < n:
            if arr[i] == 0:
                if i + 1 < n:
                    arr[i+2:] = arr[i+1:n-1]
                    arr[i+1] = 0
                i += 2
            else:
                i += 1
















class Solution:
    def duplicateZeros(self, arr: List[int]) -> None:
        """
        Do not return anything, modify arr in-place instead.
        """

        n = len(arr)
        zeros = arr.count(0)
        i = n - 1          # pointer for original array (reading)
        j = n + zeros - 1  # pointer for "virtual" extended array (writing)
        
        while i >= 0:
            if j < n:
                arr[j] = arr[i]
            if arr[i] == 0:
                j -= 1
                if j < n:
                    arr[j] = 0
            i -= 1
            j -= 1

















