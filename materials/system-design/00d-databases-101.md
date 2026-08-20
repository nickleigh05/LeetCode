# 00d. Databases from First Principles

*Where the state went. Three shapes of data, four guarantees, and the tree structure secretly powering every fast query.*

[← Prev](00c-servers-scaling.md) · [🗺 Interview Roadmap](../../interview.md) · [Next →](00e-estimation.md)

---

## Three shapes of data

Lesson [00c](00c-servers-scaling.md) pushed all the state out of your servers. It landed in a database — and your first real decision is what *shape* the data takes:

| Model | Think of it as | Classic examples | Shines when |
|-------|----------------|------------------|-------------|
| **Relational** (tables) | spreadsheets with strict columns, linked by IDs | PostgreSQL, MySQL | structured data, relationships, strong guarantees |
| **Document** | JSON blobs, each self-contained | MongoDB, DynamoDB | flexible/nested records you read as one unit |
| **Key-value** | a giant [hash map](../data-structures/hashmap.md) | Redis, Memcached | one key in, one value out, as fast as possible |

A user in a relational DB is rows scattered across `users`, `addresses`, and `orders` tables, stitched together by **joins**. In a document store it's one JSON blob holding everything. In a key-value store it's `user:42 → <blob>` and no other question is answerable. Each shape makes some queries trivial and others miserable — the same match-the-structure-to-the-operation game as [picking a data structure](../data-structures/_index.md), played with disks.

## ACID in one screen

Relational databases group writes into **transactions** — all-or-nothing units — with four promises:

- **Atomicity** — all of it happens, or none of it does. A money transfer debits *and* credits, never just one.
- **Consistency** — every rule the schema declares (balances non-negative, IDs unique) holds before and after.
- **Isolation** — concurrent transactions can't see each other's half-finished work; it's *as if* they ran one at a time.
- **Durability** — once committed, it survives a crash. The database said "OK," so it's on disk.

When an interviewer says "this is payments," they're fishing for the word **transaction**. Give it to them.

## What an index actually is

Without an index, `WHERE email = 'ada@example.com'` reads *every row* — a full scan, O(n), and n lives on disk where a seek costs ~10 ms. An **index** is a sorted structure kept alongside the table so the database can *search* instead of scan.

The structure is almost always a **B-tree** — the on-disk cousin of the [balanced BST](../data-structures/balanced-bst.md) you met in [Trees (07)](../learning/08-trees.md). Same idea — sorted keys, balanced height, O(log n) search — with one twist: each node is fat, holding hundreds of keys, so the node fills exactly one disk page.

```
memory: balanced BST — tall & skinny        disk: B-tree — short & fat
        2 children per node                  ~hundreds of children per node
        height ~30 for a billion keys        height ~3–4 for a billion keys
        (30 pointer hops: fine in RAM)       (3–4 disk reads: fine at ~ms each)
```

Same logarithm, different base — chosen because the expensive unit changed from "pointer hop" to "disk read." That's the general lesson: **the structures don't change at scale, the constants do.** The trade-off is also familiar: every index speeds up its reads but taxes *every write* (the tree must be updated too). Index the columns you query by; don't index everything.

## The real SQL-vs-NoSQL question

The interview cliché is "NoSQL is faster / webscale." That's not the question, and a well-indexed Postgres outruns a badly-modeled anything. The real trade:

- **Relational (SQL)** buys you **structure and guarantees** — schemas, joins, ACID transactions. Cost: scaling *writes* beyond one machine is genuinely hard, because joins and transactions resist being split across servers.
- **NoSQL** buys you **flexibility and horizontal scale** — schemaless records and data models designed from day one to spread across many machines. Cost: you give up joins and (usually) full transactions, and the guarantees get weaker — a trade the later replication lessons make precise.

The interview default: **start relational**, because most data is relational and the guarantees are free at small scale. Reach for NoSQL when you can *name the reason* — a key-value cache for sessions, a document store for genuinely schemaless blobs, write volume no single machine can absorb. "We'll use MongoDB because it's fast" is how you fail this question; "because these records are self-contained, never joined, and must spread across shards" is how you pass it.

## Check Yourself

- [ ] I can describe the same `user` record living in a relational, document, and key-value store — and one query each shape makes awkward.
- [ ] I can expand ACID from memory and explain atomicity with the money-transfer example.
- [ ] I can explain why databases use B-trees instead of binary search trees — the disk-page argument, in ratios.
- [ ] I can state the real SQL-vs-NoSQL trade (guarantees vs horizontal scale) without saying "NoSQL is faster."

---

**Up next:** [Back-of-Envelope Estimation](00e-estimation.md) — the arithmetic that tells you whether you even *need* more than one database. It's the Big-O of system design.

[← Prev](00c-servers-scaling.md) · [🗺 Interview Roadmap](../../interview.md) · [Next →](00e-estimation.md)
