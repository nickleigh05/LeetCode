"""

25. Reverse Nodes in k-Group

Hard

Given the head of a linked list, reverse the nodes of the list k at a time, and return the modified list.
k is a positive integer and is less than or equal to the length of the linked list. If the number of nodes 
is not a multiple of k then left-out nodes, in the end, should remain as it is.
You may not alter the values in the list's nodes, only nodes themselves may be changed.

Example 1:

    (1) ---> (2) ---> (3) ---> (4) ---> (5)
                    |
                    v
    (2) ---> (1) ---> (4) ---> (3) ---> (5)

    Input: head = [1,2,3,4,5], k = 2
    Output: [2,1,4,3,5]

Example 2:

    (1) ---> (2) ---> (3) ---> (4) ---> (5)
                    |
                    v
    (3) ---> (2) ---> (1) ---> (4) ---> (5)

    Input: head = [1,2,3,4,5], k = 3
    Output: [3,2,1,4,5]

Constraints:

    The number of nodes in the list is n.
    1 <= k <= n <= 5000
    0 <= Node.val <= 1000

Follow-up: Can you solve the problem in O(1) extra memory space?

"""

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:

        def get_kth(node, steps):
            while node and steps > 0:
                node = node.next
                steps -= 1
            return node

        dummy = ListNode(0, head)
        group_prev = dummy

        while True:
            kth = get_kth(group_prev, k)
            if not kth:
                break
            group_next = kth.next

            prev = group_next
            curr = group_prev.next

            while curr != group_next:
                next_node = curr.next
                curr.next = prev
                prev = curr
                curr = next_node

            group_tail = group_prev.next
            group_prev.next = kth
            group_prev = group_tail

        return dummy.next
