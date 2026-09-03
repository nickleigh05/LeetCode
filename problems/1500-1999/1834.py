"""

1834. Single-Threaded CPU

Medium

You are given n tasks labeled from 0 to n - 1 represented by a 2D integer array tasks, where
tasks[i] = [enqueueTime_i, processingTime_i] means that the i-th task will be available to
process at enqueueTime_i and will take processingTime_i to finish processing.

You have a single-threaded CPU that can process at most one task at a time and will act in
the following way:

    If the CPU is idle and there are no available tasks to process, the CPU remains idle.
    If the CPU is idle and there are available tasks, the CPU will choose the one with the
        shortest processing time. If multiple tasks have the same shortest processing time,
        it will choose the task with the smallest index.
    Once a task is started, the CPU will process the entire task without stopping.
    The CPU can finish a task then start a new one instantly.

Return the order in which the CPU will process the tasks.

Example 1:

    Input: tasks = [[1,2],[2,4],[3,2],[4,1]]
    Output: [0,2,3,1]

Example 2:

    Input: tasks = [[7,10],[7,12],[7,5],[7,4],[7,2]]
    Output: [4,3,2,0,1]

Constraints:

    tasks.length == n
    1 <= n <= 10^5
    1 <= enqueueTime_i, processingTime_i <= 10^9

"""

class Solution:
    def getOrder(self, tasks: List[List[int]]) -> List[int]:

        n = len(tasks)
        indexed = sorted(range(n), key=lambda i: (tasks[i][0], tasks[i][1]))

        result = []
        heap = []
        time = 0
        ptr = 0

        while len(result) < n:
            while ptr < n and tasks[indexed[ptr]][0] <= time:
                i = indexed[ptr]
                heapq.heappush(heap, (tasks[i][1], i))
                ptr += 1

            if not heap:
                time = tasks[indexed[ptr]][0]
                continue

            proc_time, i = heapq.heappop(heap)
            time += proc_time
            result.append(i)

        return result








    