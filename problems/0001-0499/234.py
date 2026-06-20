"""

234. Palindrome Linked List

Easy

Given the head of a singly linked list, return true if it is a palindrome or false otherwise.

Example 1:

    1 -> 2 -> 2 -> 1

    Input: head = [1,2,2,1]
    Output: true

Example 2:

    1 -> 2

    Input: head = [1,2]
    Output: false

Constraints:

    The number of nodes in the list is in the range [1, 105].
    0 <= Node.val <= 9

Follow up: Could you do it in O(n) time and O(1) space?

"""

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:

        slow = head
        fast = head

        while fast is not None and fast.next is not None:
            slow = slow.next
            fast = fast.next.next

        prev = None
        current = slow

        while current is not None:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node

        first_half_pointer = head
        second_half_pointer = prev
        is_palindrome = True

        while second_half_pointer is not None:
            if first_half_pointer.val != second_half_pointer.val:
                is_palindrome = False
                break
            first_half_pointer = first_half_pointer.next
            second_half_pointer = second_half_pointer.next

        prev = None
        current = second_half_pointer if second_half_pointer is None else None
        current = slow

        return is_palindrome
    












