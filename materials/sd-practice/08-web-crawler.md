# 08. Design a Web Crawler — Mid

The Design Ladder works like the DSA practice sets: attempt first, then peek. Work the design on paper against the [framework template](../appendix/templates/system-design/template.md) for a full 45 minutes before opening any step below — the struggle *is* the practice.

[← Back to the lesson](../system-design/05-queues-streams.md) · [🗺 Interview Roadmap](../../interview.md)

---

## The prompt

> "Design a web crawler for a search engine. It starts from a set of seed URLs, downloads pages, extracts links, and keeps going — we want a fresh copy of a meaningful chunk of the web."

Typical follow-up constraints when you ask (and you should ask — that's Step 1):

- ~1B pages per month, sustained.
- Be polite: don't hammer any single site, and respect `robots.txt`.
- Don't fetch the same URL twice; don't store the same *content* twice (mirrors, `?utm_source=` noise).
- Must survive the open web: infinite calendars, spider traps, servers that hang.

Why this design here? It's [BFS](../learning/11-graphs.md) industrialized — the graph traversal you drilled, rebuilt with queues, dedup structures, and politeness as first-class citizens. The interesting part isn't fetching pages; it's the **frontier** that decides what to fetch next.

<details>
<summary>Step 1 — Requirements & API</summary>

**Functional:**
- Given seed URLs, crawl outward: fetch page → parse links → enqueue new URLs → repeat.
- Store page content (and metadata) for the downstream indexer.
- Respect `robots.txt` and per-domain rate limits.
- (Confirm scope) recrawl for freshness, or one-shot snapshot? Assume continuous.

**Non-functional:**
- **Politeness is a hard requirement** — a crawler that DoSes small sites gets your IP range blocked and makes the news.
- Throughput over latency: nobody is waiting on a single page; sustained pages/s is the metric.
- Resilient: one malicious or broken site must never stall the fleet.
- Deduplication at two levels — exact URLs and near-duplicate content.

**API sketch** (internal — this is a pipeline, not a public service):

```
POST /seeds        body: { "urls": [...] }         # inject seed/priority URLs
GET  /status       returns crawl rate, frontier depth, per-domain backlog
```

The real "interface" is the data flow: frontier → fetcher → parser → storage → frontier. Say that — it reframes the whole design as a loop, which is the right mental model.
</details>

<details>
<summary>Step 2 — Estimates</summary>

One-significant-figure math (the [estimation recipes](../system-design/00e-estimation.md)):

- **Fetch rate:** 1B / month ≈ 1B / 2.6M seconds ≈ **400 pages/s** sustained.
- **Bandwidth:** ~100 KB per average page × 400/s ≈ **40 MB/s** ingest — real but not exotic; a modest fetcher fleet handles it.
- **Storage:** 100 KB × 1B ≈ **100 TB/month raw** — blob storage territory, not a database. Compression (HTML squeezes well, ~3–5×) buys a lot.
- **Fleet size:** a fetcher is I/O-bound — mostly waiting on remote servers. One machine running a few hundred concurrent connections does ~50–100 pages/s, so **~5–10 fetcher machines**. Small fleet, big coordination problem.
- **Seen-URL set:** say 10B URLs known over time × ~100 bytes ≈ 1 TB of exact storage — but a [bloom filter](../data-structures/bloom-filter.md) at ~10 bits/URL is ~**12 GB**, which fits in memory.

The numbers just decided three things: content goes to blob storage (100 TB/month kills any DB plan), the seen-set needs a bloom filter in front of exact storage (1 TB doesn't fit in RAM, 12 GB does), and the hard problem is coordination across ~10 fetchers, not raw throughput.
</details>

<details>
<summary>Step 3 — High-level design</summary>

```
 seeds ──► ┌────────────────── URL Frontier ──────────────────┐
           │  per-domain queues        next-allowed-fetch     │
           │  [a.com]→ u1,u2,...       min-heap over domains  │
           │  [b.org]→ u3,...          (politeness scheduler) │
           └──────────────────────┬───────────────────────────┘
                                  │ next URL (domain is "due")
                       ┌──────────▼──────────┐
                       │   Fetcher fleet     │──► robots.txt cache
                       │ (async HTTP, DNS $) │──► page → blob storage
                       └──────────┬──────────┘
                                  │ raw HTML
                       ┌──────────▼──────────┐
                       │      Parser         │──► content simhash → dup?
                       │ extract + normalize │
                       └──────────┬──────────┘
                                  │ candidate URLs
                       ┌──────────▼──────────┐
                       │  URL dedup          │  bloom filter → exact store
                       └──────────┬──────────┘
                                  │ genuinely new
                                  └──────────► back to Frontier
```

**The URL frontier — the heart of the design.** A naive single queue is BFS; the frontier is BFS with two extra jobs:

1. **Politeness:** URLs are bucketed into **per-domain queues**. A **min-heap keyed on next-allowed-fetch time** decides which domain is "due" — pop the earliest, take one URL from its queue, push it back with `now + delay` (from `robots.txt` `Crawl-delay` or a default ~1 req/s/domain). One domain can never occupy more than its slot, no matter how many URLs it has queued.
2. **Prioritization:** an importance score (link count, page rank-ish signal, freshness need) decides *which URL within the crawl* gets fetched first — priority tiers feeding the domain queues. Without this you spend your 400/s on infinite comment pages.

**Distributing the frontier — the key decision.** Three options for spreading work over ~10 fetchers:

1. **Shared central queue, any worker takes any URL** — simple, but two workers can hit the same domain simultaneously; politeness now needs distributed locking per domain. Messy.
2. **Partition the frontier by domain** (hash domain → worker) — each domain is owned by exactly one worker, so per-domain rate limiting is a *local* counter. Politeness becomes trivial; dedup for that domain's URLs can even be local-first.
3. **Central scheduler service dispatching to dumb fetchers** — clean separation but the scheduler is a bottleneck and single point of failure at higher scale.

Pick **2** — partition by domain. It converts the hardest distributed problem (politeness across a fleet) into a single-machine problem, and hashing by domain balances fine because no single domain dominates a 1B-page crawl. Say the trade-off: a worker dying orphans its domains until reassignment ([partitioning lesson](../system-design/08-partitioning.md) — same rebalancing story).

**Dedup, two layers:**
- **URL dedup:** normalize first (lowercase host, strip fragments and tracking params, resolve relative paths), then check a [bloom filter](../data-structures/bloom-filter.md) ([specialized infra lesson](../system-design/11-specialized-infra.md)) — hits fall through to the exact seen-URL store; misses are definitely new and skip the disk read entirely.
- **Content dedup:** exact hash catches mirrors; **simhash** catches near-duplicates (same article, different sidebar) — pages with hamming-close fingerprints are treated as already seen. Namecheck it; nobody expects the bit-twiddling.

**Supporting pieces, one line each:** DNS resolution at 400/s needs a local **DNS cache** (resolvers throttle you otherwise). `robots.txt` is fetched once per domain and cached with a TTL. Fetched content lands in blob storage keyed by URL hash; a metadata DB tracks fetch time, status, and content fingerprint for recrawl decisions.
</details>

<details>
<summary>Step 4 — Deep dives & what interviewers probe</summary>

**"How do you stay polite when the fetchers are distributed?"** — The partition-by-domain answer, stated crisply: hash each domain to exactly one worker, so "max 1 req/s to a.com" is enforced by one process with a local timestamp — no distributed coordination at all. This is the probe the whole design exists for; if you chose a shared queue in Step 3, this is where it unravels.

**"Your bloom filter says 'seen' for a URL you've never crawled. What happens?"** — A false positive means you *skip* a genuinely new page — you lose a little coverage, you never do extra work or double-fetch. At ~10 bits/element the false-positive rate is ~1%, and a missed page usually has other inbound links that survive the filter. That's why a bloom filter is safe here: the failure mode is benign and the direction of the error is the cheap one. (False negatives — recrawling a seen URL — can't happen.)

**"How do you avoid crawl traps — infinite calendars, session-ID URLs?"** — Three fences: **URL normalization** (strip session/tracking params so a million variants collapse to one), a **max depth / max URLs per domain** budget, and trap heuristics (URL length limits, repeating path segments). Plus the politeness limiter already caps the damage — a trap domain can only waste its own 1 req/s slot.

**"How do you decide what to *re*crawl?"** — Freshness is a priority signal, not a separate system: track observed change frequency per page (news homepage changes hourly, a 2009 blog post never), and feed `expected-change × importance` back into the frontier's priority tiers. The frontier already knows how to order work — reuse it.

**"A fetcher worker dies. What's lost?"** — Its in-memory domain queues. Two-part answer: the frontier's queues are backed by a durable [queue/log](../system-design/05-queues-streams.md) (in-memory is just the working set), and its domains get rehashed to survivors. Worst case some in-flight URLs are refetched — dedup makes that harmless, which is a nice "at-least-once + idempotency" note to strike.

**Common mistakes at this design:**
- Designing the fetcher (easy, boring) and hand-waving the frontier (the actual design).
- Treating politeness as a nice-to-have instead of the constraint that shapes the architecture.
- One global queue = pure BFS = the crawl drowns in the first big site's pagination.
- Forgetting URL normalization — your dedup is worthless if `?utm_source=x` makes every URL unique.
- Storing 100 TB/month of HTML in a relational database.
</details>

---

**Next on the ladder:** [Design a Distributed Cache →](09-distributed-cache.md) — you've been *using* Redis all the way up the ladder; time to build it.
