# 11. Design Ride Sharing — Senior

The Design Ladder works like the DSA practice sets: attempt first, then peek. Work the design on paper against the [framework template](../appendix/templates/system-design/template.md) for a full 45 minutes before opening any step below — the struggle *is* the practice.

[← Back to the lesson](../system-design/11-specialized-infra.md) · [🗺 Interview Roadmap](../../interview.md)

---

## The prompt

> "Design a ride-sharing service — Uber-lite. Riders request a ride, we match them with a nearby driver, and both sides see live location during the trip."

Typical follow-up constraints when you ask (and you should ask — that's Step 1):

- ~1M drivers online concurrently, each phone pinging its location every ~4 seconds.
- Match a rider to a driver in under ~30 seconds.
- Locations must be *fresh* — matching against a driver's position from two minutes ago dispatches a ghost.
- Surge pricing exists; namecheck it, don't design it.

Why this design? It's the ladder's write-heavy, real-time entry: the location firehose forbids the default "put it in the database" move, and the **geospatial index** at the center is your [grid drilling](../learning/11b-grids-primer.md) reborn as infrastructure ([specialized infra](../system-design/11-specialized-infra.md)).

<details>
<summary>Step 1 — Requirements & API</summary>

**Functional:**
- Drivers stream location updates; riders see nearby cars before requesting.
- Rider requests a ride → system finds candidate drivers → offers → one accepts → matched.
- Live tracking for both parties during pickup and the ride.
- Trip lifecycle: request through completion, with fares recorded durably.
- (Confirm scope) pricing/surge, ratings, payments — acknowledge, defer (payments is [the next rung](12-payment-system.md)).

**Non-functional:**
- **Freshness over durability for locations:** a driver's position from 10 seconds ago is useful; from 2 minutes ago it's noise. Most pings can be *dropped* harmlessly — the next one arrives in 4 seconds. Trips are the opposite: durable, never lost.
- Match latency < 30s end-to-end; the nearby-drivers query itself must be ~tens of ms.
- Regional isolation: an outage in one city shouldn't touch another.

**API sketch:**

```
POST /drivers/me/location    body: { "lat": ..., "lng": ..., "ts": ... }   # every ~4s
GET  /riders/nearby?lat&lng                 → visible cars for the map
POST /rides                  body: { "pickup": ..., "dropoff": ... }
                             → 201 { "ride_id", "state": "matching" }
GET  /rides/{id}             → state + live driver location (poll or push)
POST /rides/{id}/accept      (driver)  → 200 | 409 already taken
```

That `409 already taken` is a design decision hiding in the API — two riders must never "win" the same driver. Flag it now; it pays off in Step 4.
</details>

<details>
<summary>Step 2 — Estimates</summary>

One-significant-figure math (the [estimation recipes](../system-design/00e-estimation.md)):

- **Location writes:** 1M drivers / 4s = **250K writes/s**, all day long. This is the number that runs the design: it flatly forbids "write every ping to PostgreSQL" (a well-tuned relational DB does maybe 10K writes/s per node — you'd need a 25-node cluster to store data that's stale in 10 seconds). The pings belong **in memory**.
- **Location read side:** each update is tiny (~30 bytes of coordinates + id + timestamp): 250K/s × 30 B ≈ **~8 MB/s** — trivially small *bytes*; it's the *operation rate* that bites.
- **Memory for the index:** 1M drivers × ~100 bytes (position + a short recent trail) ≈ **100 MB** — the entire live index fits in one machine's RAM many times over. Sharding is for isolation and query load, not for fitting.
- **Ride requests:** say ~1M rides/hour at global peak ≈ **~300 requests/s** — three orders of magnitude below the location firehose. Matching is not a throughput problem; it's a *correctness and latency* problem.
- **Durable trips:** ~20M rides/day × ~1 KB ≈ 20 GB/day — an ordinary replicated database yawns.

The numbers just split the system in two: an in-memory, loss-tolerant location plane (250K/s, disposable data) and a small, durable trip plane (300/s, sacred data). Designing them as one system is the classic mistake here.
</details>

<details>
<summary>Step 3 — High-level design</summary>

```
 Drivers ─ pings ─► ┌──────────┐    ┌──────────────────────────────┐
 (every 4s)         │ Gateway  │──► │ Location service (per region)│
                    │ (region  │    │  in-memory geo index:        │
 Riders ◄─ live ────│  sharded)│    │  geohash cell → {driver:pos} │
   ▲     tracking   └────┬─────┘    │  + recent trail per driver   │
   │                     │          └───────┬──────────────────────┘
   │                     ▼                  │ sampled/trip traces
   │              ┌─────────────┐           ▼
   └── offers ◄── │  Matching   │    durable storage (analytics)
                  │  service    │
                  └──────┬──────┘   candidates → filter → rank → reserve
                         ▼
                  ┌─────────────┐
                  │ Trip service│  state machine, durable DB, events
                  └─────────────┘
```

**Ingestion — embrace the disposability.** Pings hit a regional gateway and update the **in-memory geospatial index** — overwrite the driver's entry, keep a short recent trail (for map smoothing and ETA), done. No synchronous durable write. A *sample* of pings, plus full traces for active trips, flows to durable storage asynchronously for analytics and support. Losing an in-memory node loses ~4 seconds of positions — the next round of pings rebuilds it. Say that recovery story out loud; it's why this plane gets to be fast.

**The geospatial index — THE decision.** "Find drivers near X" over raw lat/lng is a full scan; you need cells ([specialized infra](../system-design/11-specialized-infra.md) — and structurally the same move as your [grid problems](../learning/11b-grids-primer.md): discretize space, then look at a cell and its neighbors):

1. **Geohash prefix buckets** — interleave lat/lng bits into a string; a prefix of length k names a fixed cell (~5 chars ≈ 5 km, ~6 ≈ 1 km). Index is just `cell → set of drivers` in a hash map: O(1) updates, and "nearby" = query the rider's cell **plus its 8 neighbors** — required, because a rider near a cell edge has most of their nearby drivers in the *adjacent* cell, and two points can be meters apart across a geohash boundary with wildly different prefixes. Fixed cell size is the weakness: downtown cells bulge, rural cells sit empty.
2. **Quadtree** — recursively split any cell exceeding N drivers; adapts beautifully to density. But it's a mutating tree under 250K writes/s — rebalancing, locking, more machinery.
3. **PostGIS / DB spatial index** — correct and lovely, and dead on arrival at this write rate (the Step 2 verdict).

Pick **geohash buckets** — the O(1) hash-map update wins at this write rate, and the known weaknesses have cheap patches: always search neighbors (boundary), split hot cells to a finer precision level (density). Offer the quadtree as what you'd revisit if density variance dominated.

**Sharding — by city/region**, the natural partition ([partitioning](../system-design/08-partitioning.md)): a rider in Lisbon never needs drivers in Tokyo, so shards share nothing, scale independently, and fail independently — the regional-isolation requirement falls out for free. Geo-partitioning's classic hot-spot risk is real (one mega-city ≫ many towns) — split big cities into sub-regions along quiet boundaries.

**Matching — candidates → filter → rank → reserve.** Query the cell + neighbors for candidates; **filter** (available, right vehicle class, not finishing another trip); **rank by ETA — road-network distance, not straight-line** (a driver across the river is 50 m away and 20 minutes away; call the routing service for the top handful of candidates only). Offer to the best driver with a **short-TTL reservation** — the driver is atomically marked `offered` for ~10s; decline or timeout releases them and the offer cascades to the next candidate. The reservation is what makes `409 already taken` true.

**Trip state machine — the durable half.** `requested → matched → en_route_pickup → in_ride → completed` (plus `cancelled` edges). Every transition is a durable, validated write (no `completed → matched`) in an ordinary replicated DB ([replication](../system-design/07-replication.md)), emitting events to a [stream](../system-design/05-queues-streams.md) that receipts, analytics, and surge signals consume. Boring on purpose — this is the record of who owes whom money.
</details>

<details>
<summary>Step 4 — Deep dives & what interviewers probe</summary>

**"A rider stands on a geohash cell boundary. Do they see the driver 50 meters away in the next cell?"** — The classic. Yes, *if* every proximity query covers the cell **and its 8 neighbors** — proximity in space does not imply proximity in geohash strings, so neighbor expansion is mandatory, not an optimization. If candidates are still thin, widen by dropping to a shorter prefix (coarser cells) and re-query. An answer that stops at "hash the location into a cell" fails this probe.

**"Two riders request at once; your matcher offers both the same driver."** — The double-dispatch race. The fix is the **atomic reservation**: transitioning a driver `available → offered` is a compare-and-swap on the driver's state (single owner per driver record — easy, since the region shard owns it); exactly one matcher wins, the loser instantly moves to its next candidate. The **TTL** on the reservation handles the driver who never answers — no offer can leak a driver forever. Distributed-lock-free, because ownership made it a local problem.

**"Friday night at the airport: 3,000 drivers in one geohash cell."** — Fixed cell size meeting real density. Split hot cells to finer precision (6-char, then 7-char) — geohash nesting makes this hierarchical and local, and only hot cells pay for it. This is also the honest moment to concede the quadtree does this natively — the trade you named in Step 3, revisited with evidence. Rank-then-offer already caps matching cost regardless of cell population.

**"You're storing everyone's movements. Talk about location privacy."** — Separate need-to-know by plane: live raw positions expire from memory in seconds by design; durable storage gets **sampled** traces, full precision only for active trips (support, safety, fare disputes), with retention limits and access controls on the trail data. Off-duty drivers can be coarsened or dropped entirely. Treating "we just keep it all" as a default is the wrong answer in 2026.

**"A whole region's location service dies."** — Blast radius = that region (the sharding dividend). Recovery: spin up replacements and let the 4-second ping cycle repopulate the index — cold-start to warm in ~one ping interval. In-flight *trips* are unaffected: trip state is durable and separate. This is the two-plane split proving its worth.

**Common mistakes at this design:**
- Writing every ping to a durable database — the 250K/s estimate exists to catch exactly this.
- One global index instead of regional shards — throwing away the natural partition.
- Forgetting neighbor-cell search — the single most common geohash flub.
- Ranking candidates by straight-line distance and dispatching a driver across the river.
- Letting match "locks" live in the matcher's memory with no TTL — a crashed matcher strands drivers in `offered` forever.
</details>

---

**Next on the ladder:** [Design a Payment System →](12-payment-system.md) — the QPS collapses to a trickle and every hard problem is correctness: money must never be lost, and never moved twice.
