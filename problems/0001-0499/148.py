"""

148. Sort List

Medium

Given the head of a linked list, return the list after sorting it in ascending order.

Example 1:

    Input: head = [4,2,1,3]
    Output: [1,2,3,4]

Example 2:

    Input: head = [-1,5,3,4,0]
    Output: [-1,0,3,4,5]

Example 3:

    Input: head = []
    Output: []

Constraints:

    The number of nodes in the list is in the range [0, 5 * 10^4].
    -10^5 <= Node.val <= 10^5

Follow up: Can you sort the linked list in O(n logn) time and O(1) memory (i.e. constant space)?

"""

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def sortList(self, head: ListNode | None) -> ListNode | None:

        if not head or not head.next:
            return head

        slow = head
        fast = head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        mid = slow.next
        slow.next = None

        left = self.sortList(head)
        right = self.sortList(mid)
        return self.merge(left, right)

    def merge(self, a, b):
        dummy = ListNode()
        tail = dummy
        while a and b:
            if a.val <= b.val:
                tail.next = a
                a = a.next
            else:
                tail.next = b
                b = b.next
            tail = tail.next
        if a:
            tail.next = a
        else:
            tail.next = b
        return dummy.next


























    