# 10. Design a Video Platform — Senior

The Design Ladder works like the DSA practice sets: attempt first, then peek. Work the design on paper against the [framework template](../appendix/templates/system-design/template.md) for a full 45 minutes before opening any step below — the struggle *is* the practice.

[← Back to the lesson](../system-design/11-specialized-infra.md) · [🗺 Interview Roadmap](../../interview.md)

---

## The prompt

> "Design a video platform — YouTube-lite. Creators upload videos, we process them, and viewers stream them globally. Track view counts."

Typical follow-up constraints when you ask (and you should ask — that's Step 1):

- ~500 hours of video uploaded per minute.
- ~1B watch-hours per day — reads dwarf writes by orders of magnitude.
- Viewers are on flaky mobile networks as often as fiber.
- A new upload should be playable within minutes, not hours.

Why this design? It's three systems wearing one trench coat — an upload pipeline, an async processing farm, and a global delivery network — and the estimates are so violent they make most of your decisions for you. It's the ladder's showcase for [specialized infra](../system-design/11-specialized-infra.md): blob storage and CDNs as load-bearing walls, not buzzwords.

<details>
<summary>Step 1 — Requirements & API</summary>

**Functional:**
- Upload a video (large files, unreliable connections — resumable).
- Process: transcode to multiple qualities, generate thumbnails, run moderation.
- Stream: playback that adapts to the viewer's bandwidth, worldwide.
- Count views per video.
- (Confirm scope) comments, search, recommendations — assume out; live streaming — definitely out, it's a different design.

**Non-functional:**
- Playback start and smoothness are the product — buffering is churn.
- Upload durability: a creator's raw file, once accepted, is never lost.
- Upload-to-playable in minutes (drives an async pipeline with priorities, not a synchronous one).
- View counts can lag by minutes; they must not be *lossy* at the aggregate level.

**API sketch:**

```
POST /videos                        → { "video_id", "upload_url" }   # presigned, resumable
PUT  {upload_url} (chunks 1..n)     → 200 per chunk; complete when all land
GET  /videos/{id}/manifest.m3u8     → bitrate ladder + segment URLs (CDN)
GET  {cdn}/videos/{id}/720p/segment_00042.ts
POST /videos/{id}/view-events       → 202 (fire-and-forget beacon)
```

The shape of the API already tells the story: the app servers hand out *URLs* — actual bytes flow client↔blob-storage and client↔CDN, never through your application tier. Say that sentence; it's the design in miniature.
</details>

<details>
<summary>Step 2 — Estimates</summary>

One-significant-figure math (the [estimation recipes](../system-design/00e-estimation.md)):

- **Ingest:** 500 hr/min × ~1 GB/hr raw ≈ **500 GB/min ≈ 700 TB/day** *before* transcoded copies (the bitrate ladder roughly doubles it). This is the number that screams **blob storage** — no database on earth is catching 700 TB/day of media.
- **Egress:** 1B watch-hours/day × ~1 GB/hr delivered ≈ **1 EB/day ≈ ~90 Tbps average** from wherever the bytes live. Serving that from your own datacenters is absurd; this number *is* the CDN decision. Origin should see a rounding error of it.
- **Read:write on bytes:** ~1,000:1 — every architectural dollar goes to the read path.
- **Transcode compute:** transcoding ~1 hr of video per output rendition costs very roughly 1 machine-hour; 500 hr/min × ~5 renditions ≈ **~150K machines' worth of continuous transcode** at naive settings — an enormous, elastic fleet. Parallelizing *within* a video (by segment) is what makes "playable in minutes" possible at all.
- **View events:** 1B/day ≈ **~10–50K events/s** with peaks — trivial for a log, fatal as synchronous row increments.

The numbers just decided everything big: media in blob storage (700 TB/day), delivery via CDN (90 Tbps), transcoding as a segment-parallel elastic fleet (minutes-to-playable), and view counting as stream aggregation (never synchronous writes).
</details>

<details>
<summary>Step 3 — High-level design</summary>

```
 UPLOAD                      PROCESS                        DELIVER
 Creator                                                    Viewer
   │ chunks (presigned,   ┌──────────────┐                    │ manifest
   │  resumable)          │  Job queue   │                    ▼
   ▼                      └──────┬───────┘               ┌─────────┐
 ┌─────────────┐   event   ┌────▼─────────┐   segments  │   CDN   │
 │ Blob storage│ ────────► │ Transcoder   │ ──────────► │ (edge)  │
 │  (raw file) │           │ fleet: 240p→ │   + manifest└────┬────┘
 └─────────────┘           │ 4K, per-seg  │        miss      │
        ▲                  └────┬─────────┘   ┌──────────────▼──┐
 ┌──────┴──────┐    DAG: thumbs,│moderation   │ Blob storage    │
 │ App servers │◄───────────────┘             │ (transcoded)    │
 │ metadata DB │                              └─────────────────┘
 └─────────────┘    view beacons ─► event stream ─► aggregator ─► counts
```

**Upload — chunked and resumable.** The client asks the app server to start an upload; it records metadata (title, owner, `video_id`, state=`uploading`) in the DB and returns **presigned URLs** so the client writes chunks (~5–10 MB) *directly to blob storage* ([specialized infra](../system-design/11-specialized-infra.md)) — your app tier never proxies video bytes. Chunks give you resume-after-drop (re-send only the missing chunk — this is the flaky-mobile requirement), parallel upload, and per-chunk checksums. On completion, an event fires into the processing queue.

**Processing — a job DAG on a queue.** Upload-complete lands in a [queue](../system-design/05-queues-streams.md); a worker fans the video out as a **DAG of jobs**: split into ~10-second segments → transcode each segment × each rendition of the **bitrate ladder** (240p / 480p / 720p / 1080p / 4K) → stitch manifests; parallel branches for thumbnails and moderation. Segment-level parallelism is the trick worth saying twice: a 2-hour video becomes ~700 independent transcode tasks, so wall-clock time is minutes regardless of video length. Workers are stateless and idempotent (re-transcoding a segment overwrites the same output), so at-least-once delivery is safe.

**Delivery — the key decision: how do bytes reach a phone on a bad network?**

1. **Progressive download of one MP4 per quality** — simple, but quality is fixed at click time: pick 1080p on a train and you buffer forever; no mid-stream adaptation.
2. **Custom streaming protocol / stateful streaming servers** — maximal control, but you forfeit the CDN (edges cache dumb files, not sessions) — and Step 2 said 90 Tbps *requires* the CDN. Disqualified.
3. **Adaptive bitrate over HTTP (HLS/DASH)** — video is pre-chopped into segments at every quality; the client fetches a **manifest** listing them all and picks the quality of *each next segment* based on measured bandwidth. Every segment is a plain, immutable, infinitely cacheable HTTP file.

Pick **3** — ABR is the answer *because* it moves all intelligence to the client and reduces the server side to static file serving, which is exactly the shape a CDN accelerates. Flaky network drops from a crisis to "the next segment is 480p." Immutable segments + long cache TTLs mean the CDN absorbs nearly all of the 90 Tbps; origin (blob storage) only sees misses.

**Metadata** (users, video records, processing state) is small and relational — an ordinary replicated SQL database ([replication](../system-design/07-replication.md)); don't let the exabytes next door scare you into exotica.

**View counting at ~1B/day:** never a synchronous `UPDATE views = views + 1` — a viral video melts one row. Clients fire beacons into an **event stream**; a consumer aggregates counts in memory and flushes per-video deltas every few seconds. Displayed counts are approximate-then-reconciled: fast path shows near-real-time numbers, a batch job replays the log for the audited totals ([queues & streams](../system-design/05-queues-streams.md)).
</details>

<details>
<summary>Step 4 — Deep dives & what interviewers probe</summary>

**"Why chunked upload — why not one big PUT?"** — Three compounding wins: **resumability** (a 4 GB file over mobile *will* drop; retrying costs one chunk, not 4 GB), **parallelism** (several chunks in flight fill a fat pipe), and **early validation** (checksum per chunk; corruption is caught and re-sent in-flight, not discovered after an hour). Bonus point: chunk-level hashing enables dedup of re-uploaded content.

**"A conference dumps 10,000 videos at once — your transcode queue backs up for hours. Now what?"** — Two levers. **Autoscale** the transcoder fleet — jobs are stateless and segment-sized, so it scales near-linearly and the backlog is elastic-compute-shaped. And a **priority queue**: not all videos deserve equal latency — but *who jumps the line* (paying creators? predicted-viral? news?) is a **product call, not an engineering one** — surface it to the interviewer instead of silently deciding. Naming that boundary is a senior signal.

**"A video goes viral in Brazil. What breaks?"** — Edge caches in Brazilian PoPs miss simultaneously and stampede the origin across an ocean. Answers: **origin shield** (a mid-tier cache so N edges produce one origin fetch per segment — request coalescing at CDN scale) and **pre-warming** (push the top renditions of trending-in-region videos to regional edges before the wave peaks, driven by the same signals as recommendations).

**"You're adding 700+ TB/day forever, and most videos get zero views after a month. Storage cost?"** — Ride the power law with **tiered storage**: hot tier for the young and popular, cheaper cold tiers for the long tail, based on the access stats you already collect for view counts. Also: keep every *rendition* only for warm videos — cold ones keep the top rendition plus the original, re-transcoding the rest on demand (trade compute for storage). Optionally expire the raw original after transcode — but flag it as a destructive product decision, not a default.

**"How accurate are view counts, really?"** — Fast path is approximate: the stream can deliver a beacon twice (at-least-once) and dedup is best-effort in the aggregation window. That's fine for the number under the video; it's *not* fine for creator payouts — those come from the batch reconciliation over the retained log, with real dedup ([delivery semantics](../system-design/10-delivery-semantics.md) in the wild). Two consumers, two accuracy contracts, one log.

**Common mistakes at this design:**
- Streaming video bytes through your application servers — the 90 Tbps estimate exists to kill this idea.
- One transcode job per *video* instead of per *segment* — there goes "playable in minutes."
- Synchronous view-count increments — one viral video, one dead row.
- Designing upload for fiber and forgetting the flaky-mobile constraint that was in the prompt.
- Treating the CDN as an afterthought ("...and we'd add a CDN") instead of the component carrying 99% of the bytes.
</details>

---

**Next on the ladder:** [Design Ride Sharing →](11-ride-sharing.md) — the data starts *moving*: a quarter-million location writes per second, and your grid drilling comes back as geo-indexing.
