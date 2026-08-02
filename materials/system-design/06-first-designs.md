# 06. Putting It Together — Your First Design

*One full design, narrated start to finish — then the ladder is yours.*

[← Prev](05-queues-streams.md) · [🗺 Interview Roadmap](../../interview.md) · [Next →](07-replication.md)

---

> **Builds on:** everything so far — the [framework](01-design-framework.md) is the procedure, and [caching](02-caching.md), [load balancing](03-load-balancing.md), [databases](04-databases-at-scale.md), and [queues](05-queues-streams.md) are the boxes it places. This lesson is the first time you watch all five run together.

You've now met every component in the beginner's toolkit, one lesson at a time. What you haven't seen is the thing the interview actually grades: all of them deployed in one continuous forty-five-minute performance, each box arriving at the right step with its justification attached. So here is one — "design Pastebin," narrated the way you'd actually say it, numbers checked, check-ins included. Read it as a performance to imitate, not a spec to memorize. Then this lesson hands you the method for turning the [practice ladder](../../interview.md#the-design-ladder) into reps: design first, grade yourself against the answer, re-do what you couldn't finish alone.

## The worked design — Pastebin

*The prompt: "Design Pastebin — users paste text, get a short link, anyone with the link can read it."*

### Step 1 — Requirements & API (~5 min)

What you'd say: *"Let me scope this. Functionally: a user pastes text and gets back a short URL; anyone with the URL reads the paste; pastes can have an expiry. I'll treat accounts, edit/delete, and syntax highlighting as out of scope unless you want one of them. Non-functionally: read-heavy, reads should be fast — say under 200ms — and a paste, once created, must not be lost or served corrupted. High availability over strict consistency: a paste appearing a second late is fine; a paste disappearing is not."*

The API, sketched on the board:

```
POST /pastes           {text, ttl?}      → {url: "pb.io/aK3x9Q"}
GET  /aK3x9Q                             → {text, created_at}
```

Then the check-in, word for word: **"Does this scope match what you had in mind?"** Ten seconds; the map is confirmed.

### Step 2 — Estimates (~5 min)

What you'd say, rounding violently the whole way:

- **Writes:** assume ~10M new pastes/month. A month is ~2.5M seconds, so 10M ÷ 2.5M ≈ **4 writes/sec**, call peak ~10/sec. Tiny.
- **Reads:** 5:1 read:write ratio → 50M reads/month ≈ **20 reads/sec**, peak ~50/sec. Still tiny.
- **Storage:** average paste ~10 KB. 10M × 10 KB = **100 GB/month** → ~1.2 TB/year, ~6 TB over five years. That's the number with teeth: QPS is trivial, but the *bytes* accumulate.
- **Keys:** 10M/month ≈ 120M/year → ~600M pastes in five years. Base62, 6 characters = 62⁶ ≈ 56 billion combinations — 600M uses about 1% of the space. Six characters is plenty.

And the senior sentence the numbers earn: *"QPS-wise this fits on one good machine with room to spare — the design pressure here is storage growth and durability, not throughput. I'll keep the compute boring and spend my attention on the data."*

### Step 3 — High-level design (~15 min)

```
  client ──► load balancer ──► app servers (stateless, ×2) ──► cache (Redis) ──► database
                                     │                                              │
                                     └───────── key-generation service ◄────────────┘
                                                (pre-generated key pool)
```

Every box gets its sentence: the **LB** because two app servers beat one for availability even when QPS doesn't demand it ([lesson 03](03-load-balancing.md)); **stateless app servers** so either can serve any request; the **cache** because reads outnumber writes 5:1 and popular pastes are read in bursts ([lesson 02](02-caching.md)); the **database** holds pastes keyed by their short code — access is purely by key, but at 6 TB and modest QPS, a single SQL database with the ID as primary key is honest and boring ([lesson 04](04-databases-at-scale.md)); the **key-generation service** hands out unique short codes so app servers never collide.

Then walk the data — first the write: *"POST hits the LB, lands on either app server. The server takes a pre-generated key from the key service, writes the row `(key, text, created_at, expires_at)` to the database, and returns the URL. No cache write — cache-aside means the first read fills it."* Then the read: *"GET /aK3x9Q → LB → app server → check Redis; hit, return in ~1ms; miss, read the DB by primary key (~10ms), fill the cache with a TTL, return."*

End with the offer: **"That's the high level — where would you like to go deeper?"**

### Step 4 — Deep dives (~15 min)

Volunteer the scariest parts. Three dives this design supports:

**Key generation.** Options: hash the content (MD5, take 6 chars — but two identical pastes collide with each other's privacy, and truncation collides eventually); generate randomly and retry on collision (fine early, degrades as the space fills); or a **key-generation service** that pre-generates random unused keys into a pool and hands them out — no runtime collision check, and app servers can grab batches. Choice: the key pool, justified by simplicity on the hot path. Cost stated: the pool is state to manage, and handed-out-but-unused keys leak (acceptable — the space is 56B).

**Expiry.** Options: delete eagerly with a scheduled job, or **lazy expiry** — check `expires_at` on read, return 404 if past, and let a nightly cleanup job reclaim storage. Choice: lazy + nightly sweep — correctness comes from the read check, so the sweep is just a storage janitor and can run whenever. The sweep is exactly a [delayed job](05-queues-streams.md).

**Storage growth.** The 6 TB number cashes in: *"Paste text is immutable blob data — I'd move bodies to object storage (S3-style) and keep only metadata + a pointer in the database, which shrinks it from terabytes to gigabytes. And since most reads hit recent pastes, cold pastes can migrate to cheaper storage tiers."* You've turned your own Step-2 estimate into your best deep dive — that's the move interviewers remember.

Buffer close: *"Single-region design; the database is the availability weak point — replication would be my next step, which I understand is where the next track picks up."*

### Why Pastebin first

Because it's deliberately adjacent to the [**URL Shortener →**](../sd-practice/01-url-shortener.md) — same short-key generation, same read-heavy cache-aside shape, same "the numbers say boring" estimate, with paste bodies swapped in for redirects. Read this walkthrough, then attempt the URL shortener *cold*: your first solo design is a near-transfer, which is exactly how you want the first rep to feel.

## How to climb the ladder

The [ladder](../../interview.md#the-design-ladder) is thirteen designs in rising difficulty, each written as the four framework steps with model answers. The method that turns them into skill:

**Design first, on paper, 45 minutes.** Open the prompt, set a timer, and run the [template](../appendix/templates/system-design/template.md) *without* reading the answer — the struggle is the training stimulus, and reading first converts an exercise into a bedtime story. Draw real boxes, write real numbers, narrate out loud even alone; the interview grades a performance, and performances need rehearsal.

**Then grade yourself, one step at a time.** Open the exercise's four steps in order and diff honestly against your page. Did you scope the same features, or miss a requirement that reshapes everything? Are your estimates within an order of magnitude, and did you *use* them? Does every box on your diagram have its sentence? Did your deep dives argue trade-offs, or describe? Write down each miss in one line — the misses are the curriculum.

**Know what tier you're performing at:**

- **Entry** — you ran the four steps in order and produced all four deliverables. Structure is intact; boxes may be under-justified.
- **Mid** — every box traces to a requirement or a number, the data walks end to end, and at least one deep dive weighs real options.
- **Senior** — you drove: volunteered the scariest dive, named failure modes unprompted, and your answers survive three consecutive "why?"s.

**The re-do rule.** Any design where you needed the answers — a step you couldn't produce, a component you only recognized in hindsight — goes back in the queue **one week later**, attempted cold again. Passing the re-do is what graduation means; nodding along at a model answer means nothing. (This is the same spaced re-do discipline as the coding side of the [roadmap](../../interview.md#the-design-ladder), for the same reason: recall under pressure is the skill, and recall only grows from retrieval.)

First rung: [**Design a URL Shortener →**](../sd-practice/01-url-shortener.md), cold, this week.

## Check Yourself

- [ ] I can re-derive the Pastebin estimates from "10M pastes/month, 5:1 reads, 10 KB average" without looking — and say which number has teeth.
- [ ] I can name the sentence that justifies each of the five boxes in the Pastebin diagram.
- [ ] I can give the three key-generation options and defend the key-pool choice.
- [ ] I've scheduled my first cold attempt at the URL shortener — timer, paper, template, no peeking.

---

**Up next:** [Replication](07-replication.md) — the Mastery Track begins: what happens when one database isn't enough, and the copies you make to survive losing it.

[← Prev](05-queues-streams.md) · [🗺 Interview Roadmap](../../interview.md) · [Next →](07-replication.md)
