# 00e. Back-of-Envelope Estimation

*Big-O tells you how an algorithm grows; estimation tells you how a system groans. Same skill, bigger napkin.*

[← Prev](00d-databases-101.md) · [🗺 Interview Roadmap](../../interview.md) · [Next →](00f-foundations-drills.md)

---

## Why interviewers make you do arithmetic

Every design choice — one database or ten, cache or no cache, do the files even fit on a machine — hangs on numbers you're expected to *derive on the spot*. This is the system-design analog of [Big-O](../learning/00c-big-o-notation.md): nobody cares about the exact figure, they care that you can find the **order of magnitude** and let it drive the design. Ten seconds of arithmetic, then a decision.

## Powers of 2 and 10

The only lookup table you need. The whole trick is that **2¹⁰ ≈ 10³**, so binary sizes and round numbers interchange freely:

| Power of 2 | ≈ Power of 10 | Name it |
|-----------|---------------|---------|
| 2¹⁰ | ~10³ = thousand | KB |
| 2²⁰ | ~10⁶ = million | MB |
| 2³⁰ | ~10⁹ = billion | GB |
| 2⁴⁰ | ~10¹² = trillion | TB |
| 2⁵⁰ | ~10¹⁵ | PB |

And two calendar constants: a day is **86,400 seconds ≈ 10⁵**, a year is **~3 × 10⁷ seconds** (and 365 days ≈ 400 when multiplying).

## The physical constants, again

Same table as [00a](00a-internet.md), compressed to the ratios you'll actually use mid-estimate:

| Fact | Number |
|------|--------|
| memory reference | ~100 ns |
| SSD random read | ~100 μs (memory × 1,000) |
| disk seek | ~10 ms (memory × 100,000) |
| round trip in-datacenter | ~0.5 ms |
| round trip cross-continent | ~150 ms |

If your design does 20 sequential cross-continent hops, no amount of clever code saves you — the envelope already said 3 seconds.

## The three recipes

**QPS (queries per second):**

```
QPS ≈ DAU × actions per user per day ÷ 86,400      (just divide by 100,000)
peak QPS ≈ 3 × average                              (traffic isn't flat)
```

**Storage:**

```
storage/day  = writes per day × item size
storage/year = storage/day × 365                    (call it × 400)
```

**Bandwidth:**

```
bandwidth = QPS × payload size
```

That's the whole toolkit. Everything else is knowing your item sizes: a tweet-like record ~1 KB, a photo ~a few MB, a minute of video ~tens of MB.

## Rounding culture

Interviewers want **one significant figure**, delivered fast. 86,400 is 100K. 365 is 400. 150M ÷ 86,400 is "about 1,500," not 1,736.11. Precision past the first digit is *worse* than useless — it signals you don't know which digit matters. Round aggressively, say "roughly" a lot, and state your assumptions out loud so the interviewer can correct them ("assume 300M daily users — sound fair?"). The number is a means; the *decision it forces* is the answer.

## Worked example: Twitter's write path

*Estimate tweet-write QPS and storage per year.*

**Assumptions (say them out loud):** 300M DAU; the average user tweets once every 2 days → 0.5 tweets/user/day; a tweet with metadata ≈ 1 KB; ignore media for now.

```
writes/day  = 300M × 0.5            = 150M tweets/day
write QPS   = 150M ÷ 100K           ≈ 1,500 QPS
peak QPS    = 1,500 × 3             ≈ 5,000 QPS

storage/day  = 150M × 1 KB          = 150 GB/day
storage/year = 150 GB × 400         ≈ 60 TB/year   (call it ~50–60 TB)
```

Now the numbers *force conclusions*: 5,000 writes/sec is real but not exotic — a few database nodes, not a heroic architecture. 60 TB/year of text is almost quaint — but attach one 2 MB image to a tenth of tweets and storage jumps to ~30 TB/**day**, which is why media lives in blob storage behind a CDN, not in the tweets table. One minute of arithmetic just designed a third of the system. That's the point.

## Check Yourself

- [ ] I know 2¹⁰ ≈ 10³ and can convert "2³² of anything" into a round number in my head.
- [ ] I can recite the QPS recipe — DAU × actions ÷ 100K, ×3 for peak — and the storage recipe without notes.
- [ ] I can redo the Twitter example from a blank page in under two minutes, assumptions included.
- [ ] I round to one significant figure by reflex and state assumptions before computing on them.

---

**Up next:** [Foundations Drills](00f-foundations-drills.md) — trace requests, run estimates, and pick databases until this whole unit is reflex.

[← Prev](00d-databases-101.md) · [🗺 Interview Roadmap](../../interview.md) · [Next →](00f-foundations-drills.md)
