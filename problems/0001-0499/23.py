"""

23. Merge k Sorted Lists

Hard

You are given an array of k linked-lists lists, each linked-list is sorted in ascending order.

Merge all the linked-lists into one sorted linked-list and return it.

Example 1:

    Input: lists = [[1,4,5],[1,3,4],[2,6]]
    Output: [1,1,2,3,4,4,5,6]
    Explanation: The linked-lists are:
    [
    1->4->5,
    1->3->4,
    2->6
    ]
    merging them into one sorted linked list:
    1->1->2->3->4->4->5->6

Example 2:

    Input: lists = []
    Output: []

Example 3:

    Input: lists = [[]]
    Output: []

Constraints:

    k == lists.length
    0 <= k <= 104
    0 <= lists[i].length <= 500
    -104 <= lists[i][j] <= 104
    lists[i] is sorted in ascending order.
    The sum of lists[i].length will not exceed 104.


"""

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:

        min_heap: List[tuple] = []

        for list_index in range(len(lists)):
            head_node: Optional[ListNode] = lists[list_index]
            if head_node is not None:
                heapq.heappush(min_heap, (head_node.val, list_index, head_node))

        dummy_head: ListNode = ListNode()
        current_node: ListNode = dummy_head

        while min_heap:
            smallest_val, list_index, smallest_node = heapq.heappop(min_heap)

            current_node.next = smallest_node
            current_node = current_node.next

            next_node: Optional[ListNode] = smallest_node.next
            if next_node is not None:
                heapq.heappush(min_heap, (next_node.val, list_index, next_node))

        current_node.next = None

        return dummy_head.next
    











