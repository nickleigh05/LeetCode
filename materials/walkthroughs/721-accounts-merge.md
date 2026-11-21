# 721. Accounts Merge

**Medium** · [LeetCode](https://leetcode.com/problems/accounts-merge/) · [Solution file (no hints)](../../problems/0500-0999/721.py)

[📖 11. Graphs lesson](../learning/11-graphs.md) · [📖 Union-Find](../learning/12-union-find.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 11. Graphs problems](../rmap-practice/11-graphs.md)

---

You're given a list `accounts`. Each `accounts[i]` is a list of strings: the first is a **name**, and the rest are **emails** belonging to that account.

Two accounts belong to the same person if they share **any** email. Accounts with the same name aren't necessarily the same person. Merge the accounts and return them as `[name, email1, email2, ...]`, with each person's emails **sorted**. The accounts themselves can be returned in any order.

```
accounts = [["John","johnsmith@mail.com","john_newyork@mail.com"],
            ["John","johnsmith@mail.com","john00@mail.com"],
            ["Mary","mary@mail.com"],
            ["John","johnnybravo@mail.com"]]

→ [["John","john00@mail.com","john_newyork@mail.com","johnsmith@mail.com"],
   ["Mary","mary@mail.com"],
   ["John","johnnybravo@mail.com"]]
```

The first two accounts share `johnsmith@mail.com`, so they merge. The fourth John shares nothing, so he stays separate.

**Constraints:** `1 <= accounts.length <= 1000` · `2 <= accounts[i].length <= 10` · `1 <= accounts[i][j].length <= 30` · emails are valid and accounts sharing an email always have the same name

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| share **any** email → same person | Connection is **transitive**. If A shares with B and B shares with C, then A and C are the same person even if they share nothing directly |
| same name ≠ same person | **Never** group by name. Names are only labels for the output |
| merged emails **sorted** | Collect each group's emails, then sort them |
| any order of accounts | No ordering requirement between groups |

**This is a connected-components problem in disguise.** Treat every **email** as a node. Every account says "all of these emails belong together," so connect them. Each connected component is then one person.

The transitivity is the key point. It's why you can't just compare accounts pairwise once: A–B and B–C linking A to C needs either repeated merging or a structure built for it.

**How to connect an account's emails cheaply.** You don't need edges between every pair. Linking every email to the account's **first** email is enough, because that makes them all one component. An account with k emails then needs k − 1 links, not k².

🤔 **Before you open the next section:** what data structure answers "are these two in the same group?" and "merge these two groups" quickly, with groups that keep growing?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Repeated pairwise merging | Merge any two accounts that overlap, repeat until stable | O(n² · k) per round | O(n·k) | ❌ Slow and fiddly |
| Graph + DFS | Email adjacency list, DFS each component | O(E log E) | O(E) | ✅ Works well |
| **Union-Find** | Union each email with its account's first email, group by root | **O(E log E)** | O(E) | ✅ Built for this |

Here E is the total number of emails, and the log comes from the final sort.

**The decision: [Union-Find](../data-structures/union-find.md) (disjoint set union).**

Union-Find is the structure for "group things that are connected, where connections arrive one at a time." Each `union` merges two groups, and each `find` returns a group's representative. With path compression, both are close to O(1).

**DFS is equally valid.** Build `email → neighbouring emails`, then DFS from each unvisited email to collect its component. Choose whichever you can write without bugs. Union-Find tends to be shorter here because you never build an explicit adjacency list.

**Using emails as keys directly.** Instead of mapping emails to integer ids, the `parent` dict can use the email strings themselves. It's the same structure and avoids an extra lookup table.

**One more map: email → name.** Every email in a group belongs to the same person (the problem guarantees it), so you can look up the name from the group's root email.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
parent = {}

def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x
```

**`find` with path compression.** Walk up the parent pointers to the root, which is the email whose parent is itself. On the way, `parent[x] = parent[parent[x]]` points each node at its grandparent, which halves the path each time. Future finds get faster.
→ [dict-basics](../syntax/dict-basics.md) · [while-loop](../syntax/while-loop.md) · [function-basics](../syntax/function-basics.md)

```python
def union(a, b):
    parent[find(a)] = find(b)
```

**Merge two groups** by making one root point at the other. If they already share a root, this just sets the root's parent to itself, which does nothing.
→ [closures](../syntax/closures.md)

```python
email_to_name = {}
for account in accounts:
    name = account[0]
    for email in account[1:]:
        if email not in parent:
            parent[email] = email
        email_to_name[email] = name
        union(account[1], email)
```

**Build the groups.** For every email in the account:

1. If it's new, make it its own group (`parent[email] = email`).
2. Remember its owner's name.
3. Union it with the account's **first** email, `account[1]`. That links the whole account into one group in k − 1 operations. (Unioning `account[1]` with itself on the first pass is harmless.)

`account[1:]` slices off the name and leaves just the emails.
→ [list-slicing](../syntax/list-slicing.md) · [membership-operators](../syntax/membership-operators.md)

```python
groups = defaultdict(list)
for email in parent:
    groups[find(email)].append(email)
```

**Collect components.** Every email that has the same root belongs to the same person. A `defaultdict(list)` creates the empty list the first time a root appears.
→ [defaultdict](../syntax/defaultdict.md)

```python
result = []
for root, emails in groups.items():
    result.append([email_to_name[root]] + sorted(emails))
return result
```

**Format the output.** The name comes from any email in the group (the root is convenient), followed by the sorted emails.
→ [sorting-key](../syntax/sorting-key.md) · [dict-methods](../syntax/dict-methods.md)

<details>
<summary>The whole thing together</summary>

```python
from collections import defaultdict

class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        parent = {}

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a, b):
            parent[find(a)] = find(b)

        email_to_name = {}
        for account in accounts:
            name = account[0]
            for email in account[1:]:
                if email not in parent:
                    parent[email] = email
                email_to_name[email] = name
                union(account[1], email)

        groups = defaultdict(list)
        for email in parent:
            groups[find(email)].append(email)

        result = []
        for root, emails in groups.items():
            result.append([email_to_name[root]] + sorted(emails))
        return result
```

</details>

**Trace it.** The example, abbreviating emails as `js`, `jny`, `j00`, `m`, `jb`:

| Account | Emails | Unions performed | Groups after |
|---|---|---|---|
| John | js, jny | js–js, jny→js | {js, jny} |
| John | js, j00 | js–js, j00→js | {js, jny, j00} |
| Mary | m | m–m | {js, jny, j00}, {m} |
| John | jb | jb–jb | {js, jny, j00}, {m}, {jb} |

The second account's `js` was already in the first group, so unioning `j00` with it pulls `j00` into that group. That's the transitive merge.

Three groups → three output accounts ✅.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(E log E)</summary>

**O(E · α(E) + E log E)**, which is effectively **O(E log E)**, where E is the total number of emails.

- **Building:** one `union` per email. Each `find` is near-constant with path compression. (α is the inverse Ackermann function, which is ≤ 4 for any realistic input.)
- **Grouping:** one `find` per distinct email.
- **Sorting:** each group is sorted, and the group sizes add up to E, so at worst O(E log E).

The sort dominates. **Strictly, this `union` only uses path compression, not union by rank.** That's enough for excellent performance in practice. Add union by rank or size if the interviewer wants the formal α bound.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(E)</summary>

**O(E).**

- `parent`: one entry per distinct email.
- `email_to_name`: one entry per distinct email.
- `groups` plus the result: each email appears once.

That's all linear in the number of emails. You can't do better, since the output itself contains every email.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Accounts sharing an email are the same person, and that's transitive, so this is connected components with emails as nodes. I'll use Union-Find keyed directly on email strings. For each account I union every email with the account's first email, which links the account in k − 1 operations, and I record each email's name. Then I group emails by their root, sort each group, and prepend the name. Union-Find operations are near O(1) with path compression, so sorting dominates at O(E log E). Space is O(E)."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Could you use DFS instead?" | Yes. Build an email adjacency list (link each email to the account's first), then DFS each unvisited email to collect a component. Same complexity. |
| "Why not group by name?" | Different people can share a name. The fourth John in the example is a different person. |
| "Why link to the first email instead of every pair?" | Connecting to one hub email already makes a single component, in k − 1 links instead of k². |
| "Add union by rank?" | Track a size or rank per root and attach the smaller tree under the larger. That guarantees the α(n) bound. |
| "Emails arrive as a stream?" | Union-Find is naturally incremental. Keep unioning as accounts arrive, and group only when asked. |

**Traps:**

- **Merging by name.** It's the most common wrong answer.
- **A single pass of pairwise merging.** It misses transitive links (A–B, then B–C discovered later).
- **Forgetting to initialise `parent[email] = email`.** `find` then hits a `KeyError`.
- **Unsorted email output.** The problem requires each group sorted.
- **Recursive `find` on long chains.** It can hit Python's recursion limit. The iterative version above avoids that.

**This same move shows up in:** [Number of Provinces](547-number-of-provinces.md) (counting connected components) · [Redundant Connection](684-redundant-connection.md) (Union-Find detecting a cycle edge) · [Number of Connected Components](323-number-of-connected-components-in-an-undirected-graph.md) (the textbook Union-Find count) · [Graph Valid Tree](261-graph-valid-tree.md) (Union-Find plus an edge-count check).

</details>

---
