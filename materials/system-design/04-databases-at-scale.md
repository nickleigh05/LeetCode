# 04. SQL vs NoSQL & Indexing

*The most-probed choice in system design — and why "one Postgres box" is so often the senior answer.*

[← Prev](03-load-balancing.md) · [🗺 Interview Roadmap](../../interview.md) · [Next →](05-queues-streams.md)

---

> **Builds on:** [Databases 101](00d-databases-101.md) — tables, keys, transactions, and the first look at indexes — and [Trees](../learning/07-trees.md), because a database index is a [balanced BST](../data-structures/balanced-bst.md) grown up: the B-tree's O(log n) is the same O(log n) you earned there.

"SQL or NoSQL?" is the question interviewers ask to find out whether you make choices from requirements or from fashion. The wrong answer is a brand name with no reason attached; the right answer is a rubric applied out loud. Underneath the choice sits the machinery that actually determines performance — the index structures, and what every index costs you on the write path. This lesson gives you the rubric, the two engine families, and the handful of database traps (N+1, missing pools, index bloat) that make deep dives go well or badly.

## Concept

### The Engine-Choice Rubric

**What it is:** A decision procedure you say out loud in Step 3, instead of a brand preference.

- **Relations and transactions → SQL.** Orders that reference users that reference addresses; money that must move atomically; queries you haven't predicted yet. Joins, foreign keys, and ACID are exactly what relational engines sell.
- **Flexible schema, horizontal scale, simple access patterns → NoSQL.** Documents whose shape varies, write volume that demands many nodes, and — critically — access that's always *by key*: "get user 42's feed," never "join across five tables." NoSQL trades away joins and (usually) transactions to get easy sharding.
- **"At this scale, it doesn't matter" — often the senior answer.** If your Step-2 estimates say a few hundred QPS and tens of gigabytes, one well-indexed Postgres box handles it with room to spare. Saying so — *"the data is relational and the scale is modest, so a single SQL database; I'll flag where it breaks"* — beats reflexively reaching for Cassandra, and interviewers know it.

| Signal from requirements | Points to |
|--------------------------|-----------|
| Multi-row transactions (payments, inventory) | SQL |
| Rich relations, ad-hoc queries, joins | SQL |
| Access is always by key, no joins needed | NoSQL |
| Write volume beyond one machine | NoSQL (or [sharded SQL →](08-partitioning.md)) |
| Schema varies per record / evolves fast | NoSQL (document store) |
| Modest scale, unclear future queries | SQL — the boring default |

**Use when:** every design, Step 3. The rubric *is* the answer — name the requirement, then the engine, in that order.

### B-tree vs LSM-tree — Read- vs Write-Optimized

```
  B-TREE (Postgres, MySQL)                 LSM-TREE (Cassandra, RocksDB)
  write: find the page, edit in place      write: append to in-memory table,
         (random I/O, but reads are               flush sorted runs to disk,
          one tree walk)                           merge ("compact") later

        ┌────[ root ]────┐                  memtable (RAM) ──flush──► SSTable 3 (newest)
     ┌──┴──┐          ┌──┴──┐                                        SSTable 2
  [ leaf ][ leaf ]…[ leaf ][ leaf ]         read checks each ──────► SSTable 1 (oldest)
   sorted rows, O(log n) to any key         newest-first; compaction merges them
```

**What it is:** The two storage-engine families, and the read/write trade they make in opposite directions. A **B-tree** keeps data sorted in a wide, shallow tree and updates pages in place — reads are one O(log n) walk, writes pay random I/O. An **LSM-tree** never edits in place: writes append to memory and flush as sorted immutable files, which is why **Cassandra ingests so fast** — every write is sequential. Reads pay instead: a lookup may consult several files before finding the newest version, and background **compaction** merges files to keep that bounded.

**Key Properties:**
- B-tree: **read-optimized** — predictable point and range reads; the engine under Postgres and MySQL.
- LSM-tree: **write-optimized** — sequential-only disk writes absorb huge ingest; the engine under Cassandra, RocksDB, and most "write-heavy at scale" answers.
- The interview line: *"write-heavy time-series at this volume wants an LSM engine — Cassandra — because appends are sequential; the read side pays via compaction, which is fine for our access pattern."* One sentence, engine named, trade named.

**Use when:** your Step-2 numbers are write-dominated (metrics, events, chat history, crawler output) → LSM. Read-dominated or mixed with rich queries → B-tree, plus a [cache](02-caching.md).

### Composite & Covering Indexes

**What it is:** An index is a sorted copy of chosen columns with pointers back to the rows — O(log n) lookups instead of a full scan. The design skill is choosing *which* columns, in *which* order.

- **Composite index** — one index over multiple columns, sorted by the first, then the second: `(user_id, created_at)` serves "this user's posts, newest first" as a single range scan. Order matters — that index is useless for "all posts on a date across users," because `user_id` comes first. Rule of thumb: **equality columns first, range column last**.
- **Covering index** — include every column the query needs, and the database answers from the index alone, never touching the table. `(user_id, created_at, title)` makes a feed-of-titles query index-only.

**Python** (the mental model — an index is a sorted structure you binary-search, straight from [Binary Search](../learning/05-binary-search.md)):
```python
# index on (user_id, created_at): sorted list of tuples
idx = sorted((row.user_id, row.created_at, row.id) for row in table)

# "user 42's posts, newest first" = one bisect + a contiguous scan
lo = bisect_left(idx, (42,))          # O(log n) to the start
hi = bisect_left(idx, (43,))          # everything for user 42 is adjacent
posts = idx[lo:hi]                    # already sorted by created_at
```

**Use when:** you name the index *with* the query it serves: "reads are `GET /feed?user=…`, so a composite index on `(user_id, created_at)`." An index without its query is decoration.

### Every Index Taxes Writes

**What it is:** The bill for read speed. Each index is a separate sorted structure the engine must also update on every `INSERT`/`UPDATE`/`DELETE` — a table with five indexes does six writes per row change, plus the page splits and cache churn that come with them.

**Key Properties:**
- Index the queries you *have*, not the queries you can imagine. Unused indexes are pure write tax.
- Write-heavy tables want **few** indexes — often just the primary key and one access-path index.
- The interview move: when you add an index in a deep dive, say the cost in the same breath — "indexed on `(user_id, created_at)`; that's one extra structure to maintain per write, worth it at our 50:1 read ratio." Numbers earn indexes, same as they earn caches.

### Denormalization — A Deliberate Trade

**What it is:** Copying data so a read needs no join — storing `author_name` on every post instead of joining to `users` a million times a day. Normalization optimizes for *correct, single-copy* writes; denormalization optimizes for *cheap* reads, and accepts that updates must now touch every copy (the author renames → a backfill job rewrites their posts, or you tolerate staleness).

**Trade-offs:**

| | Normalized | Denormalized |
|---|-----------|--------------|
| Reads | Joins — more work per query | Single lookup — fast |
| Writes | One place to update | Every copy to update |
| Consistency | Automatic | Your job now |

**Use when:** the read:write ratio is lopsided and the copied field changes rarely — names, titles, thumbnails. Say the word "deliberate": *"I'll denormalize the author name onto posts — it changes rarely, and it saves a join on every feed read."* In NoSQL this isn't even optional; without joins, denormalizing around your access patterns *is* the data model.

### Connection Pooling & the N+1 Trap

**What it is:** The two operational database mistakes that cost real systems more than any engine choice.

- **Connection pooling** — opening a database connection costs a TCP + auth handshake and a chunk of server memory; databases cap out at hundreds-to-thousands of connections, while your [autoscaled fleet](03-load-balancing.md) can demand far more. The fix is a **pool**: each app server keeps ~10–20 open connections and requests borrow and return them. One sentence in Step 3; the failure it prevents (fleet scales up → connections exhaust → database refuses everyone) is a nice Step-4 volunteer.
- **The N+1 trap** — fetch 100 posts (1 query), then loop fetching each author (100 more). 101 round trips at ~1ms each where 2 queries would do: fetch the posts, then `WHERE id IN (…)` for all the authors — or one join. ORMs generate this pattern silently; it's why "the page is slow" so often means "the page runs 400 queries."

**Use when:** N+1 is a ready-made deep-dive answer for any "why is this endpoint slow?" probe — name it, fix it with a batched `IN` query, and mention the [cache](02-caching.md) as the second layer of defense.

## The Pattern — Choose, Index, Pay

The database moves you'll make on every rung of the [ladder](../../interview.md#the-design-ladder):

1. **Run the rubric out loud** — relations/transactions vs key-based access at scale; name the engine *after* the requirement.
2. **Check the scale honestly** — if Step 2 says one box suffices, say so and stay boring.
3. **Name the top queries, then their indexes** — each index quoted with the query it serves, composite order justified.
4. **Say the write tax** — every index and every denormalized copy gets its cost stated in the same breath.
5. **Cover the plumbing** — connection pooling in Step 3; N+1 in your back pocket for the latency deep dive.

The invariant to protect: **every index and every copied field is justified by a named query.** The moment you're indexing "just in case" or denormalizing without saying who updates the copies, you've traded write cost for nothing — and that's exactly the trade an interviewer will ask you to defend.

## The Template

The design-interview worksheet lives in [`appendix/templates/system-design/`](../appendix/templates/system-design/). Read the README (when to reach for each component, common traps), then work designs against [`template.md`](../appendix/templates/system-design/template.md) — the engine choice and data model land in Step 3; indexes and the N+1/pooling material are Step-4 ammunition.

## Practice

[**Design a URL Shortener →**](../sd-practice/01-url-shortener.md) is the rubric in miniature — key-value access, huge read skew, and a genuine "does SQL vs NoSQL even matter here?" moment. [**Design a News Feed →**](../sd-practice/06-news-feed.md) is where indexing and denormalization carry the design: the feed query *is* a composite index, and fan-out is denormalization at system scale. Work both against the [ladder](../../interview.md#the-design-ladder).

## Check Yourself

- [ ] I can run the SQL-vs-NoSQL rubric on a new prompt in under a minute — requirement first, engine second.
- [ ] I can explain B-tree vs LSM-tree as read- vs write-optimized, and say why Cassandra ingests fast.
- [ ] I can design a composite index for "user 42's posts, newest first" and say what query it *can't* serve.
- [ ] I can spot an N+1 in a described read path and fix it with one batched query.

---

**Up next:** [Queues, Streams & Async Work](05-queues-streams.md) — when the work doesn't have to happen *now*, a queue absorbs the spike your database can't. (And when one database's reads can't keep up at all, that's [read replicas →](07-replication.md) — the Mastery Track opener.)

[← Prev](03-load-balancing.md) · [🗺 Interview Roadmap](../../interview.md) · [Next →](05-queues-streams.md)
