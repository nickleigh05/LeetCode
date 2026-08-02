# 01. The Design Interview Framework

*Four steps, forty-five minutes — the procedure that turns "design Twitter" from a panic into a plan.*

[← Prev](00f-foundations-drills.md) · [🗺 Interview Roadmap](../../interview.md) · [Next →](02-caching.md)

---

> **Builds on:** [How to Approach a Problem](../guides/how-to-approach-a-problem.md) — the same discipline of *understand before you solve*, scaled up from a function to a fleet — and the [Interview Guide](../guides/interview-guide.md) for the meta-game: thinking out loud, checking in, owning the clock.

A coding interview has a correct answer; a design interview has a *defended* one. The interviewer hands you a prompt that would take a real team a year — "design a chat app" — and grades how you carve it down, not whether you finish it. Candidates who wing it produce forty-five minutes of plausible rambling and nothing gradeable; candidates with a framework produce four checkable deliverables in order. This lesson is that framework. Every other lesson in this track exists to fill in one of its steps, and every exercise on the ladder is a rep of running it.

## Concept

### The Shape of the Hour

```
  minute  0        5        10                  25                  40    45
          ├────────┼────────┼───────────────────┼───────────────────┼─────┤
          │ STEP 1 │ STEP 2 │       STEP 3      │       STEP 4      │ buf │
          │ reqs & │ estim- │     high-level    │     deep dives    │ fer │
          │  API   │  ates  │       design      │                   │     │
```

**What it is:** A fixed budget for four deliverables. The clock is the silent killer — candidates who spend twenty minutes on requirements never reach the deep dives, and the deep dives are where the senior signal lives.

**Timeboxes:**

| Step | Time | Deliverable | You're off the rails if… |
|------|------|-------------|--------------------------|
| 1. Requirements & API | ~5 min | Scoped feature list + endpoint sketch | still asking questions at minute 12 |
| 2. Estimates | ~5 min | QPS, storage, read:write — rounded hard | doing long division on the board |
| 3. High-level design | ~15 min | Boxes & arrows, data walked end to end | drawing boxes you can't justify |
| 4. Deep dives | ~15 min | 2–3 components at depth, trade-offs argued | describing instead of deciding |
| Buffer | ~5 min | Bottlenecks, failure points, "what I'd do next" | — |

**Key Properties:**
- The steps are **strictly ordered** — each one's output is the next one's input. Estimates need requirements to estimate; the design needs estimates to size; deep dives need a design to dive into.
- Every step ends with a **check-in**: a one-line summary and a question. You're allowed to be wrong at each step; you're not allowed to be wrong *silently* for ten minutes.
- The timeboxes are soft but the **order isn't** — an interviewer can pull you into Step 4 early, and you follow. You should never pull *yourself* back to Step 1 late.

### Step 1 — Requirements & API (~5 min)

**What it is:** Turning a one-line prompt into a contract you can be graded against.

- **Functional requirements** — what the system does. Three to five bullets, phrased as user actions: "post a message," "follow a user," "load a feed."
- **Non-functional requirements** — how well. Scale (how many users? how much data?), latency ("feed loads in <200ms"), availability vs consistency (is stale data acceptable?), read-heavy or write-heavy.
- **The API** — two to four endpoints that make the features concrete. Signatures, not schemas:

```
POST /posts              {text}           → {post_id}
GET  /feed?user_id=…                      → [posts…]
POST /follow             {followee_id}    → 200
```

**Scope aggressively.** The prompt is deliberately too big; cutting it down *is* the test. Say the cut out loud: "I'll design posting and the feed — search, ads, and DMs are out of scope unless you'd rather I cover one of them." Then the check-in that separates drivers from passengers: **"Does this scope match what you had in mind?"** Ten seconds, and you've either confirmed the map or been corrected before the wrong map cost you anything.

### Step 2 — Estimates (~5 min)

**What it is:** Three or four numbers that decide what you're allowed to build — the full technique is [Estimation](00e-estimation.md).

**Key Properties:**
- **QPS** — requests per second, average and peak, reads and writes separately.
- **Storage** — bytes per record × records per day × retention. This is the number that decides whether one machine holds the data.
- **The read:write ratio** — the single number that shapes the whole design; it justifies (or forbids) the cache.
- **Round violently.** A day is 100K seconds. You're sizing, not invoicing.

**Use when:** always — but the payoff comes in Steps 3 and 4, because **numbers earn boxes**. No cache without a read ratio, no sharding without a storage total, no queue without a spike. And if the numbers come out small — a few hundred QPS, gigabytes of data — *say so*: "one good database handles this; I'll keep the design boring and flag where it breaks." That sentence is a senior answer, not a cop-out.

### Step 3 — High-Level Design (~15 min)

```
  client ──► load balancer ──► app servers ──► cache ──► database
                                    │
                                    └──► queue ──► workers      (async work)
```

**What it is:** Boxes and arrows on the board — the five-box spine above covers most designs on the ladder — followed by the move that actually earns points: **walk the data through**. Pick one user action from Step 1 and narrate it end to end: "the POST hits the load balancer, lands on any app server — they're stateless — the server validates, writes the row, invalidates the cache key, returns 201." Then walk the read. A diagram nobody walks through is furniture.

**Key Properties:**
- **Every box gets a sentence.** "Cache, because reads outnumber writes 50:1." If you can't attach the sentence, erase the box.
- **Breadth before depth.** Cover every functional requirement shallowly before going deep anywhere — depth is Step 4's job, and diving early is how candidates run out of clock with half a system on the board.
- **End with an offer:** "That's the high level — where would you like to go deeper?" You've just handed the interviewer a menu instead of waiting for an ambush.

### Step 4 — Deep Dives (~15 min)

**What it is:** Two or three components at real depth. The interviewer picks ("how does the feed actually get built?") or you volunteer the scariest part — volunteering is the stronger move. **Trade-offs are the grading axis**: every deep dive should surface at least two options, an honest cost for each, and a choice justified by a Step-1 requirement or a Step-2 number.

| Weak answer | Strong answer |
|-------------|---------------|
| "I'd use Redis here." | "Two options: fan-out-on-write gives fast reads but is expensive for celebrity accounts; fan-out-on-read is the reverse. At our 100:1 read ratio I'd fan out on write, special-casing accounts over 1M followers." |

**Use when:** the shape is universal — options, costs, choice, justification. Lessons [02](02-caching.md) through [11](11-specialized-infra.md) exist to stock this step with material; the framework is what makes the material land.

### What's Graded — and How It Shifts by Level

**What it is:** The same 45-minute performance, read against a different bar depending on the level you're interviewing for.

| Signal | Junior / entry | Senior |
|--------|----------------|--------|
| Structure | Followed the four steps ✓ | Assumed — table stakes |
| Fundamentals | Sane API, sensible boxes, knows what a cache is | Assumed — table stakes |
| Trade-offs | Nice to have | The core grade — every choice has a named alternative |
| Depth | One area beyond the surface | Answers survive three consecutive "why?"s |
| Driving | Responds well when steered | Sets the agenda, volunteers deep dives, owns the clock |

**Driving vs being driven:** the interviewer will happily steer all forty-five minutes — and grade you down for needing it. Driving looks like announcing which step you're on, checking in at every boundary, and proposing the next deep dive. Being driven looks like silence until asked, answering exactly what was asked, and waiting. Same knowledge, different hire decision.

### The Anti-Patterns

**What it is:** The four recurring ways strong engineers fail this interview. Know which one is yours.

- **Schema-first** — opening with `CREATE TABLE` before any requirement exists. You're answering before the question is set. Requirements → API → *then* the data model.
- **Silence** — thinking for two minutes without narrating. The interviewer can't grade a blank feed; think out loud even at the cost of polish.
- **Monologuing** — the opposite failure: fifteen unbroken minutes of your plan with zero check-ins. You may be building the wrong system, confidently.
- **Over-engineering** — Kafka, ten shards, and three regions for a system your own Step 2 said was 50 QPS. Designing below your estimates reads as junior; designing above them reads as not believing your own numbers. Build the scale you computed.

## The Pattern — The Four Steps

This whole lesson *is* the pattern; here it is as the move set you'll run on all thirteen designs of the [ladder](../../interview.md#the-design-ladder):

1. **Scope it** — functional + non-functional requirements, an API sketch, cut everything else. Check in: "does this scope match what you had in mind?"
2. **Size it** — QPS, storage, read:write ratio ([Estimation](00e-estimation.md)). Say out loud what the numbers permit.
3. **Draw it** — boxes and arrows, then walk one write and one read through the diagram, narrating.
4. **Defend it** — two or three deep dives: options, costs, a choice, a justification. Volunteer the scariest one.

The invariant to protect: **never introduce a component you can't justify from a requirement or a number.** Every box on the board must trace back to Step 1 or Step 2 — the moment one doesn't, you're decorating, and a good interviewer will ask about exactly that box.

## The Template

The design-interview worksheet lives in [`appendix/templates/system-design/`](../appendix/templates/system-design/) — it's this framework as a fill-in form. Read the README (when to reach for each component, common traps), then run every practice design against [`template.md`](../appendix/templates/system-design/template.md) until the four headings appear in your head unbidden.

## Practice

This lesson's exercise is *every* design on the [ladder](../../interview.md#the-design-ladder) — the framework is the one pattern you'll run all the way up. Start with [**Design a URL Shortener →**](../sd-practice/01-url-shortener.md): a system small enough that the framework is the hard part, which is exactly the point.

## Check Yourself

- [ ] I can name the four steps, their timeboxes, and each one's deliverable from memory.
- [ ] I can produce functional + non-functional requirements and an API sketch for "design Pastebin" in under five minutes.
- [ ] I can name the four anti-patterns and say which one is *my* default failure under pressure.
- [ ] I know my Step-1 check-in question word for word.

---

**Up next:** [Caching](02-caching.md) — the highest-leverage box you'll draw in Step 3, and the first deep dive most interviewers reach for.

[← Prev](00f-foundations-drills.md) · [🗺 Interview Roadmap](../../interview.md) · [Next →](02-caching.md)
