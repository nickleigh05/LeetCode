# 11. Specialized Infrastructure

*Five components that each unlock a whole class of designs — know what they are, when to reach, and one sentence of how.*

[← Prev](10-delivery-semantics.md) · [🗺 Interview Roadmap](../../interview.md)

---

> **Builds on:** three DSA lessons come back as infrastructure here — [Tries (08)](../learning/08-tries.md) power typeahead and inverted-index term lookup, [the grids primer (10b)](../learning/10b-grids-primer.md) is the intuition behind geospatial indexes, and [Bit Manipulation (18)](../learning/18-bit-manipulation.md) is what bloom filters and bitmaps are made of.

The core track gave you the universal boxes — cache, balancer, database, queue, shards. But some interview questions hinge on one *specialized* box: you can't design YouTube without blob storage, Uber without a geo-index, or a web crawler without a bloom filter. Interviewers use these questions to check whether you know the standard tool or try to jam everything into Postgres. Each section below is deliberately shallow-but-precise — the goal is to *name the right component, place it, and survive one follow-up*, which is exactly the depth a loop probes unless you're interviewing for that team specifically.

## Concept

### Blob Storage — the S3 Model

```
  upload:                                    download:
  client ─► app: "uploading cat.mp4"         client ─► app: "give me video 42"
  app ─► DB: INSERT metadata row             app ─► DB: fetch metadata
  app ─► client: presigned PUT URL           app ─► client: presigned GET URL
  client ═══ bytes ═══► OBJECT STORE         client ◄══ bytes ══ OBJECT STORE (or CDN)

  Metadata (small, queryable) in the DB.  Bytes (huge, dumb) in the object store.
  The bytes NEVER flow through your app servers.
```

**What it is:** An **object store** (S3, GCS) holds immutable blobs by key — no queries, no partial updates, just PUT/GET — at effectively infinite scale, eleven-nines durability, and pennies per GB. The pattern every media design uses: **metadata in a database, bytes in the object store**, joined by a URL or key stored in the metadata row.

**Key Properties:**
- **Presigned URLs** are the piece to name: the app server authorizes, then hands the client a short-lived signed URL so the client talks to the object store *directly*. Your app tier never proxies gigabytes — it stays a lightweight control plane.
- Objects are immutable — "editing" is writing a new version. That's a feature: immutability makes caching and CDN distribution trivial.
- Databases are the wrong tool for blobs (they're built for small rows, and replication chokes on media); local disk is worse (dies with the server, defeats horizontal scaling).

**Use when:** Videos, images, file attachments, backups, ML datasets — anything measured in MB/GB per item. If your Step-2 estimate says petabytes, you're saying "object store" in Step 3.

### CDN Internals

**What it is:** A **CDN** is a globally distributed cache of edge servers; users hit the nearest edge instead of your origin, cutting a cross-ocean ~200ms round-trip to ~20ms. Beyond "put a CDN in front," know the fork:

- **Pull (default)** — edge misses fetch from origin and cache with a TTL. Zero ops; first user per region eats a slow miss. Say pull first.
- **Push** — you upload content to edges ahead of demand. For predictable big launches (a game patch, a premiere); you now manage distribution and cleanup yourself.

**Key Properties:**
- **What to CDN:** static assets, images, video segments — and video is the killer app: HLS/DASH chop a video into small static chunks, so "streaming" becomes "serving cacheable files from edges."
- **What not to:** personalized or rapidly changing responses (your feed, a stock ticker) — per-user content has a ~0% hit rate and just adds a hop. Middle ground exists (short-TTL caching of hot public API responses), but don't lead with it.
- **Invalidation:** versioned URLs (`app.v42.js` — new deploy, new URL, old cache irrelevant) beat purge APIs, which are slow and eventual. Same [caching](02-caching.md) rules, planetary scale.

**Use when:** Any design with a global audience and static-ish content. In a video/image design the CDN is not an optimization — it's where ~95%+ of egress must come from, or your origin bill and latency are absurd.

### Search — Inverted Indexes

```
  Docs:  d1 "cheap flights to tokyo"      Inverted index:
         d2 "tokyo street food"           "tokyo"   → [d1, d2]
         d3 "cheap tokyo hotels"          "cheap"   → [d1, d3]
                                          "flights" → [d1]
  Query "cheap tokyo" → intersect [d1,d3] ∩ [d1,d2] → wait, "tokyo": [d1,d2,d3]
                      → [d1, d3] → rank → results
```

**What it is:** `WHERE text LIKE '%tokyo%'` can't use a B-tree index (the wildcard prefix forbids it) — it's a full-table scan per query, dead at any scale. An **inverted index** flips the mapping: for every term, the list of documents containing it (like a book's index). A query becomes: look up each term's posting list, intersect, rank by relevance.

**Key Properties:**
- Documents are **tokenized and normalized** at index time (lowercase, stemming: "flights" → "flight") — that's why search finds variants a LIKE never would.
- The name-drop is **Elasticsearch** (or OpenSearch/Lucene): say "I'll stream product updates into Elasticsearch via the [outbox/CDC pipeline](10-delivery-semantics.md)" — the search index is a *derived, eventually-consistent replica* of the source-of-truth DB, not a second master.
- Prefix flavors of search — typeahead — are [trie](../learning/08-tries.md) territory: same idea, term-prefix → completions, usually precomputed top-k per prefix.

**Use when:** Any "search the [products/tweets/listings]" requirement. The one-liner: "text search gets its own index — LIKE doesn't scale — so, Elasticsearch fed by CDC."

### Geospatial Indexes

```
  GEOHASH: interleave lat/lng bits → base32 string   QUADTREE: recursively split
  world → "9"  → "9q" → "9q8" → "9q8y" (SF)          busy squares into 4
  longer prefix = smaller cell                        ┌───────┬───┬───┐
  nearby points → SHARED PREFIX                       │       │▪▪▪│▪ ▪│  dense city:
  "drivers near me" =                                 │ ocean ├───┼───┤  deep splits
  WHERE geohash LIKE '9q8y%'  (+ neighbors)           │       │▪▪▪│ ▪ │  ocean: one
                                                      └───────┴───┴───┘  big cell
```

**What it is:** "Find drivers within 2km" is unanswerable with B-trees on raw lat/lng — an index on latitude gives you a *band* around the equator, not a circle around a point. The fix is encoding 2D proximity into something 1D-indexable:

- **Geohash** — interleave latitude/longitude bits into a string; longer = more precise, and **nearby points share a prefix**, so a radius query becomes a *prefix query* — your grid intuition ([10b](../learning/10b-grids-primer.md)) turned into a string index.
- **Quadtree** — recursively split any cell holding more than K points into four children; a radius query descends only into overlapping cells. Adaptive: dense downtown gets deep small cells, the ocean stays one node.

**Key Properties:**
- The geohash gotcha to volunteer: **cell edges** — two points meters apart can straddle a boundary and share no prefix. Fix: query the cell *and its 8 neighbors*.
- Geohash = fixed grid, trivially stored in any DB or Redis (`GEOSEARCH` uses it); quadtree = adaptive to skewed density, but a tree you maintain in memory. Uniform-ish or DB-backed → geohash; wildly skewed density → quadtree.
- Moving drivers = a write-heavy in-memory index (Redis geo per city), rebuilt cheap, not a durably-stored source of truth.

**Use when:** Ride sharing, delivery, "restaurants near me", geo-fenced feeds. The expected sentence: "index drivers by geohash; nearby = prefix match on my cell plus its 8 neighbors."

### Probabilistic Structures

**What it is:** At billions of items, exact answers to "seen it before? how many distinct? who's hot?" cost more memory than they're worth. Sketches trade a tunable error for orders-of-magnitude less space — all built on hashing and [bit tricks](../learning/18-bit-manipulation.md).

- **Bloom filter** — a bit array + k hash functions; insert sets k bits, lookup checks them. Answers **definitely-not / probably-yes**: false positives possible (tunable — ~1% at ~10 bits/element), **false negatives impossible**. A billion URLs in ~1.2 GB instead of a 60+ GB exact set. (Reference: [bloom filter](../data-structures/bloom-filter.md).)
- **Count-min sketch** — a bloom filter for *counts*: a small 2D array of counters; increment one cell per hash row, read the minimum across rows. Overestimates only — perfect for **heavy hitters** (top hashtags, hot keys, rate-limit candidates) in fixed memory.
- **HyperLogLog** — counts **distinct elements** (unique visitors, distinct search queries) in ~12 KB with ~1–2% error, using the max count of leading zero bits across hashed values as a cardinality estimate. Redis has it built in (`PFADD`/`PFCOUNT`) — say that.

**Key Properties:**
- The common frame — say it once: **fixed small memory, one-sided or bounded error, no way to enumerate or delete** (deletion needs variants like counting bloom filters).
- Classic pairing: bloom filter as a cheap *front* — a crawler checks "URL seen?" against the filter; "definitely not" (the overwhelming case) skips the expensive exact check entirely; "probably yes" falls through to the source of truth. The filter absorbs the fast path; correctness still lives in the exact store.

**Use when:** Crawler dedup at billions of URLs, "did this user already see this ad/notification," unique-view counters, trending/top-k. Any time exact bookkeeping at your Step-2 scale costs tens of GB for a yes/no or a rough count.

## The Pattern — Recognize, Name, Survive One Follow-Up

These components are Step-3 answers to specific requirements. The moves, in order:

1. **Recognize the trigger in Step 1** — media at scale → blob storage + CDN; text search → inverted index; "near me" → geo-index; dedup/counting at billions → a sketch. The requirement names the component.
2. **Justify with your Step-2 numbers** — "500 PB of video can't live in a database"; "an exact seen-set for 10B URLs is ~600 GB — a bloom filter is ~12 GB at 1% error."
3. **Place it and name the real system** — S3, CloudFront/Cloudflare, Elasticsearch, Redis geo, Redis HyperLogLog. Named tech signals you've seen these in the wild.
4. **Say the data flow, not the internals** — presigned URLs so bytes skip your app tier; CDC feeding the search index; prefix query plus 8 neighbors; bloom-check before the exact check.
5. **Volunteer the sharp edge** — CDN invalidation, geohash boundaries, bloom false positives, the search index lagging the DB. One caveat per component is the senior signal; a lecture is not.

The invariant to protect: **every specialized store is a derived view — the system of record stays one boring, consistent database.** The search index, the CDN edge, the geo-index, the bloom filter can all be stale, lossy, or rebuilt from scratch; the moment one of them is the *only* home of a fact, you've made a probabilistic structure your source of truth, and that's the flaw interviewers dig for.

## The Template

The design-interview worksheet lives in [`appendix/templates/system-design/`](../appendix/templates/system-design/). Read the README (when to reach for each component, common traps), then work designs against [`template.md`](../appendix/templates/system-design/template.md) — these components enter in Step 3 with a one-line justification, and the follow-up you prepared for is a Step-4 deep dive.

## Practice

Each component headlines a rung of the [ladder](../../interview.md#the-design-ladder): blob storage + CDN carry [**Design a Video Platform →**](../sd-practice/10-video-platform.md), geohash vs quadtree is the central debate of [**Design Ride Sharing →**](../sd-practice/11-ride-sharing.md), and the bloom filter is the star of [**Design a Web Crawler →**](../sd-practice/08-web-crawler.md). These three designs, back to back, exercise everything on this page.

## Check Yourself

- [ ] I can draw the metadata-DB / object-store split and explain what presigned URLs buy.
- [ ] I can explain why `LIKE '%x%'` doesn't scale and how an inverted index answers a two-word query.
- [ ] I can turn "find drivers near me" into a geohash prefix query — including the 8-neighbors fix — and say when I'd prefer a quadtree.
- [ ] For bloom filter, count-min sketch, and HyperLogLog, I can state in one sentence each: the question it answers, the error it allows, and a design that needs it.

---

**Up next:** that's the full mastery track — every box on the whiteboard now has a lesson behind it. Put it together on the senior rungs of the [design ladder](../../interview.md#the-design-ladder): work up through the payment system, ride sharing, and the distributed queue, and treat each one as a timed mock.

[← Prev](10-delivery-semantics.md) · [🗺 Interview Roadmap](../../interview.md)
