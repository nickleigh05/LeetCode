# The Interview Roadmap


## How to use this roadmap


The [DSA Roadmap](roadmap.md) gets you through the coding rounds. This roadmap covers everything else the loop grades: the **behavioral** rounds, the **system design** rounds, and the shape of the loop itself. A technical interview is three separate skills scored by three separate people — being excellent at one doesn't transfer, and most rejections come from the pillar the candidate didn't prepare.

Three rules here too: **start behavioral early** (good stories take weeks to season — this is the most procrastinated, highest-return hour of prep), **pace system design against your DSA progress** (the [pacing table](#pacing--system-design-alongside-dsa) below tells you exactly when to read what — the concepts share DNA), and **stop where your level stops** (through SD lesson 06 plus the Entry/Mid designs is a complete junior→mid prep; the Mastery Track and Senior designs are for senior loops — don't grind consensus algorithms for a new-grad interview).


## The loop itself


Know the game before playing it. Full guide: [**The Interview Loop →**](materials/guides/interview-loop.md)

| Stage | Typically | What's actually graded |
|-------|-----------|------------------------|
| Recruiter screen | 30 min call | Interest, logistics, level calibration — not technical skill |
| Phone screen | 45–60 min, 1–2 coding | Can you code at the bar? Half the funnel exits here |
| Onsite: coding ×2 | 45 min each | [The coding choreography](materials/guides/interview-guide.md) |
| Onsite: system design | 45–60 min | [Pillar 3](#pillar-3--system-design) — trade-offs out loud |
| Onsite: behavioral | 45 min | [Pillar 1](#pillar-1--behavioral) — evidence you're good to work with |
| Debrief | you're not there | Written feedback + scores; one strong champion matters |


## Pillar 1 — Behavioral


Half the onsite, and the half nobody drills. The method is a **story bank**: 6–8 real stories from your experience, indexed against the question categories, told in situation → task → action → result shape, rehearsed *aloud*.

**Start here:** [**Behavioral Interviews — the story bank method →**](materials/guides/behavioral-interviews.md)

Build the bank in week one of prep, then rehearse one story per day alongside your DSA drilling. It's an hour a week and it moves offers.


## Pillar 2 — Technical (Coding)


This pillar already has its own course: the [**DSA Roadmap →**](roadmap.md) — 20 units across four phases, ≈180 h, with lessons, templates, walkthroughs and practice sets. Work it top to bottom; it is the largest time investment of the three pillars by far. Phases 1–3, core problems only, is a complete junior→mid coding prep.

Knowing the patterns and performing them under observation are different skills. Once you're past the roadmap's early phases, layer in [**The Coding Interview →**](materials/guides/interview-guide.md) — the 45-minute choreography, what's graded, and how to practice with mocks — and follow the [study plan](materials/guides/study-plan.md) for retention.


## Pillar 3 — System Design


Completely absent from LeetCode, half the loop for mid-level+ roles, and the easiest pillar to fake badly. The track works exactly like the DSA lessons: read, then drill designs from [the ladder](#the-design-ladder).

### Foundations

*How the pieces of the internet fit together. Readable from day one — no DSA prerequisite.*

| # | Lesson | One-line idea |
|---|--------|---------------|
| 00a | [How the Internet Works](materials/system-design/00a-internet.md) | DNS → TCP → TLS → response; the latency numbers that constrain every design. |
| 00b | [HTTP & APIs](materials/system-design/00b-http-apis.md) | Request anatomy, REST, pagination; websockets vs polling vs SSE. |
| 00c | [Servers, Statelessness & Scaling](materials/system-design/00c-servers-scaling.md) | Why stateless services scale horizontally and state is the enemy. |
| 00d | [Databases from First Principles](materials/system-design/00d-databases-101.md) | Tables vs documents vs key-value; ACID; what an index actually is. |
| 00e | [Back-of-Envelope Estimation](materials/system-design/00e-estimation.md) | QPS, storage, bandwidth — the SD analog of Big-O. |
| 00f | [Foundations Drills](materials/system-design/00f-foundations-drills.md) | Trace-a-request, estimation, and pick-a-database drills. |

### Core

*The components every design uses and the framework that assembles them. This tier + the Entry/Mid designs = complete junior→mid prep.*

| # | Lesson | One-line idea | Practice |
|---|--------|---------------|----------|
| 01 | [The Design Interview Framework](materials/system-design/01-design-framework.md) | Requirements → estimates → high-level → deep dives, timeboxed over 45 min. | [The ladder](#the-design-ladder) |
| 02 | [Caching](materials/system-design/02-caching.md) | Cache-aside, eviction, TTLs — and the failure modes interviewers probe. | [Distributed Cache](materials/sd-practice/09-distributed-cache.md) · [Typeahead](materials/sd-practice/03-typeahead.md) |
| 03 | [Load Balancing & Horizontal Scaling](materials/system-design/03-load-balancing.md) | Many copies of your server, one front door; L4/L7, health checks. | [News Feed](materials/sd-practice/06-news-feed.md) · [Chat](materials/sd-practice/07-chat-system.md) |
| 04 | [SQL vs NoSQL & Indexing](materials/system-design/04-databases-at-scale.md) | The engine-choice rubric; B-tree vs LSM; why indexes tax writes. | [URL Shortener](materials/sd-practice/01-url-shortener.md) · [News Feed](materials/sd-practice/06-news-feed.md) |
| 05 | [Queues, Streams & Async Work](materials/system-design/05-queues-streams.md) | Decouple, absorb spikes, retry safely; queue vs pub/sub; DLQs. | [Notifications](materials/sd-practice/05-notification-system.md) · [Web Crawler](materials/sd-practice/08-web-crawler.md) |
| 06 | [Putting It Together — Your First Design](materials/system-design/06-first-designs.md) | A fully worked design, then how to climb the ladder solo. | [URL Shortener](materials/sd-practice/01-url-shortener.md) |

### Mastery Track *(senior roles)*

*Distributed systems proper. Severable — a junior loop will not probe this; a senior loop will probe little else.*

| # | Lesson | One-line idea | Practice |
|---|--------|---------------|----------|
| 07 | [Replication & Failover](materials/system-design/07-replication.md) | Leader–follower, replication lag, split-brain. | [Distributed Cache](materials/sd-practice/09-distributed-cache.md) |
| 08 | [Partitioning & Consistent Hashing](materials/system-design/08-partitioning.md) | Sharding, hot keys, the ring — hashing's final form. | [Distributed Cache](materials/sd-practice/09-distributed-cache.md) · [Distributed Queue](materials/sd-practice/13-distributed-queue.md) |
| 09 | [Consistency Models & Consensus](materials/system-design/09-consistency-consensus.md) | Linearizable → eventual; quorums; Raft at whiteboard depth. | [Distributed Queue](materials/sd-practice/13-distributed-queue.md) |
| 10 | [Delivery Semantics & Idempotency](materials/system-design/10-delivery-semantics.md) | Exactly-once is a lie; idempotency keys, outbox, sagas. | [Payments](materials/sd-practice/12-payment-system.md) |
| 11 | [Specialized Infrastructure](materials/system-design/11-specialized-infra.md) | Blob storage, CDNs, search, geospatial, bloom filters. | [Video Platform](materials/sd-practice/10-video-platform.md) · [Ride Sharing](materials/sd-practice/11-ride-sharing.md) |

### The Design Ladder

*The practice set. Work each one on paper for 45 minutes against the [framework template](materials/appendix/templates/system-design/template.md), then check the steps. Easy → hard, like everything else in this repo.*

| # | Design | Tier | What it exercises |
|---|--------|------|-------------------|
| 01 | [URL Shortener](materials/sd-practice/01-url-shortener.md) | Entry | ID generation, DB choice, caching with numbers |
| 02 | [Rate Limiter](materials/sd-practice/02-rate-limiter.md) | Entry | Token bucket vs sliding window, distributed state |
| 03 | [Typeahead](materials/sd-practice/03-typeahead.md) | Mid | Tries vs precomputed top-k, aggressive caching |
| 04 | [Top-K Leaderboard](materials/sd-practice/04-top-k-leaderboard.md) | Mid | Heaps at scale, sorted sets, approximation |
| 05 | [Notification System](materials/sd-practice/05-notification-system.md) | Mid | Queue fan-out, retries, idempotent delivery |
| 06 | [News Feed](materials/sd-practice/06-news-feed.md) | Mid | Fan-out on write vs read — the classic trade-off |
| 07 | [Chat System](materials/sd-practice/07-chat-system.md) | Mid | Websockets, ordering, presence, offline delivery |
| 08 | [Web Crawler](materials/sd-practice/08-web-crawler.md) | Mid | BFS industrialized: frontier, politeness, dedup |
| 09 | [Distributed Cache](materials/sd-practice/09-distributed-cache.md) | Senior | Consistent hashing, LRU per node, hot keys |
| 10 | [Video Platform](materials/sd-practice/10-video-platform.md) | Senior | Blob storage, transcoding pipelines, CDN |
| 11 | [Ride Sharing](materials/sd-practice/11-ride-sharing.md) | Senior | Geospatial indexes, matching, location streams |
| 12 | [Payment System](materials/sd-practice/12-payment-system.md) | Senior | Idempotency, ledgers, reconciliation — correctness over scale |
| 13 | [Distributed Message Queue](materials/sd-practice/13-distributed-queue.md) | Senior | The capstone: builds lessons 05 + 07–10 into one design |


## Pacing — system design alongside DSA


System design concepts are DSA concepts wearing infrastructure clothes — hash maps become shard keys, heaps become schedulers, BFS becomes a crawler frontier. Read SD lessons right after the DSA units that plant the idea and both stick better.

| When you finish this… | …read these SD lessons | Why now |
|-----------------------|------------------------|---------|
| [Unit 00 · Foundations](roadmap.md#phase-1) | SD [00a](materials/system-design/00a-internet.md)–[00b](materials/system-design/00b-http-apis.md) | Latency numbers are the physical constants behind Big-O. |
| [Units 01–04 · Linear patterns](roadmap.md#phase-1) | SD [00c](materials/system-design/00c-servers-scaling.md)–[00f](materials/system-design/00f-foundations-drills.md) | Hash maps (01) are cache keys and shard keys; queues (04) are request buffers. |
| [Units 05–07 · Recursion, search, lists](roadmap.md#phase-2) | SD [01](materials/system-design/01-design-framework.md)–[02](materials/system-design/02-caching.md) | Linked list + hash map (07) is literally the LRU cache; an index lookup is binary search on disk. |
| [Units 08–10 · Trees, tries, heaps](roadmap.md#phase-2) | SD [03](materials/system-design/03-load-balancing.md)–[04](materials/system-design/04-databases-at-scale.md) + [Typeahead](materials/sd-practice/03-typeahead.md), [Top-K](materials/sd-practice/04-top-k-leaderboard.md) | BSTs (08) → B-tree indexes; tries (09) → typeahead; heaps (10) → schedulers and top-k. |
| [Units 11–13 · Backtracking & graphs](roadmap.md#phase-3) | SD [05](materials/system-design/05-queues-streams.md)–[06](materials/system-design/06-first-designs.md) + Entry/Mid designs | BFS (12) → crawler frontier; topo sort (13) → dependency pipelines. |
| [Units 14–17 · DP, greedy, intervals](roadmap.md#phase-3) | SD [07](materials/system-design/07-replication.md)–[09](materials/system-design/09-consistency-consensus.md) + remaining Mid designs | The trade-off instinct from DP/greedy is the grading axis of every deep dive. |
| [Units 18–19 · Math & bits](roadmap.md#phase-4), + Mastery (20) | SD [10](materials/system-design/10-delivery-semantics.md)–[11](materials/system-design/11-specialized-infra.md) + the Senior ladder | Bit manipulation (19) → bloom filters; segment trees (20) → range aggregation in analytics. |


### Materials

The reference layers this roadmap draws on.

| Hub | What's inside |
|-----|---------------|
| [Design Framework Template](materials/appendix/templates/system-design/README.md) | The 4-step worksheet to run every design against — the SD analog of the code templates |
| [Behavioral Interviews](materials/guides/behavioral-interviews.md) | STAR, the story bank, question archetypes, practice method |
| [The Interview Loop](materials/guides/interview-loop.md) | Stage-by-stage: recruiter screen → onsite → debrief |
| [The Coding Interview](materials/guides/interview-guide.md) | The 45-minute choreography for the coding rounds |
| [🗺 The DSA Roadmap](roadmap.md) | Pillar 2 in full — lessons, templates, practice sets |
