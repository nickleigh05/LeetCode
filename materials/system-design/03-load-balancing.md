# 03. Load Balancing & Horizontal Scaling

*Many copies of your server, one front door — and the machine that decides who answers the doorbell.*

[← Prev](02-caching.md) · [🗺 Interview Roadmap](../../interview.md) · [Next →](04-databases-at-scale.md)

---

> **Builds on:** [Servers & Scaling](00c-servers-scaling.md) — vertical vs horizontal scaling and why stateless servers are the ones you're allowed to clone. This lesson is what stands *in front* of the clones.

The moment your estimates say one server isn't enough, you draw a load balancer — it's the second box in almost every Step-3 diagram, right after the client. Most candidates draw it and move on; interviewers earn their deep dives by asking what's *inside* it: which layer does it operate at, how does it pick a server, what happens when a server dies, and what happens when the balancer itself dies. This lesson stocks those four answers. Get them right and horizontal scaling stops being a hand-wave and becomes a defended design.

## Concept

### L4 vs L7 — What the Balancer Can See

```
  L4 (transport)                          L7 (application)
  sees: IPs, ports, TCP/UDP               sees: everything L4 sees, PLUS
        packets                                 the HTTP request itself —
                                                URL, headers, cookies, method
  ┌──────┐  TCP conn   ┌────┐  forward    ┌──────┐  HTTP req  ┌────┐  new req
  │Client│────────────►│ L4 │───────────► │Client│───────────►│ L7 │──────────►
  └──────┘             └────┘  packets    └──────┘            └────┘  routed by
                        fast, dumb                             content — smart,
                                                               slightly slower
```

**What it is:** The layer of the network stack the balancer operates at decides what it can route on. An **L4 balancer** sees connections — IP addresses and ports — and forwards packets without opening them. An **L7 balancer** terminates the connection, reads the full HTTP request, and can route on anything in it: `/api/video/*` to the video fleet, `/api/chat/*` to the chat fleet, mobile user-agents to a canary.

**Key Properties:**
- **L4 is faster and simpler** — no request parsing, just connection plumbing. Millions of connections per box.
- **L7 is smarter** — path-based routing, header-based routing, per-endpoint rate limits, response caching, and it's where **TLS termination** lives (below).
- Real deployments often stack them: L4 at the edge for raw throughput, L7 behind it for routing brains.

| | L4 | L7 |
|---|---|---|
| Routes on | IP + port | URL, headers, cookies, method |
| Speed | Fastest — no parsing | Parses every request |
| Can split by endpoint? | No | Yes — `/video` fleet vs `/chat` fleet |
| TLS termination | Passes encrypted bytes through | Decrypts, inspects, re-routes |

**Use when:** L7 is the default answer in an interview — you almost always want content-aware routing. Name L4 when the traffic isn't HTTP (raw TCP, game servers, [WebSockets at extreme scale](../sd-practice/07-chat-system.md)) or when you need to balance the balancers.

### Routing Algorithms — Picking a Server

**What it is:** Given N healthy servers, the rule that picks one per request.

- **Round robin** — 1, 2, 3, 1, 2, 3. The default; perfect when servers are identical and requests are uniform. Weighted round robin handles a mixed fleet (the big box gets 2 tickets per cycle).
- **Least connections** — send the request to whoever is busiest *least*. Wins when request durations vary wildly (one slow report query shouldn't stack more work on that server).
- **Hash-based routing** — hash something stable (user ID, session ID, source IP) and route by the hash, so the same user always lands on the same server. This is how you get affinity *without* cookies — and it's the doorway to [consistent hashing](08-partitioning.md), which fixes what happens to the hash when servers join or leave. Full treatment there; for now, know that naive `hash % N` reshuffles *everyone* when N changes.

| Algorithm | Picks | Wins when | Weakness |
|-----------|-------|-----------|----------|
| Round robin | Next in cycle | Uniform requests, identical servers | Ignores actual load |
| Least connections | Fewest active conns | Variable request durations | Slightly more bookkeeping |
| Hash-based | `hash(key) % N` | Same key must hit same server | Naive version reshuffles on N change |

**Use when:** say "round robin, least-connections if request times vary" and move on — the algorithm is rarely the interesting part. Reach for hash-based routing only when you *need* affinity, and question whether you do (see sticky sessions below).

### Health Checks — Ejecting the Dead

```
  every 5s:  LB ──► GET /health ──► server
             ┌────────────────────────────────────┐
             │ 200 OK  ×1  → stays in rotation    │
             │ timeout ×3  → EJECTED from pool    │
             │ 200 OK  ×2  → readmitted           │
             └────────────────────────────────────┘
```

**What it is:** The balancer probes every server on an interval — usually an HTTP `GET /health` — and stops routing to servers that fail. This is the mechanism that turns "we have 10 servers" into "we survive losing one": traffic to a dead node just... redistributes.

**Key Properties:**
- **Thresholds, not single probes** — eject after 3 consecutive failures, readmit after 2 consecutive passes. One dropped packet shouldn't drain a healthy node.
- A good `/health` endpoint checks **the server's own dependencies** (can I reach my database?), not just "process is up" — otherwise you route traffic to a server that accepts requests and fails all of them.
- Beware the **correlated failure**: if the database goes down, every server's health check fails, the LB ejects *everyone*, and you've turned a partial outage into a total one. Deep health checks should degrade, not eject, on shared-dependency failure.

**Use when:** always — a load balancer without health checks is a traffic distributor, not a fault tolerator. Naming the eject/readmit thresholds unprompted is an easy senior signal.

### Sticky Sessions vs Stateless + Shared Store

**What it is:** The question of where a logged-in user's session lives — and the answer that unlocks horizontal scaling.

- **Sticky sessions**: the LB pins each user to one server (cookie or hash-based), and that server keeps the session in local memory. Simple — and fragile. That server dies, its users are logged out; that server gets the celebrity, it melts while its siblings idle; autoscaling in new servers helps nobody who's already pinned.
- **Stateless + shared session store**: any server can handle any request, because sessions live in a shared cache — Redis, keyed by session token, exactly the [distributed cache from lesson 02](02-caching.md). Servers become interchangeable cattle: kill one, add five, nobody notices.

**Recommend the second, every time.** The one-line justification: *"I'll keep app servers stateless with sessions in Redis, so the LB can route freely and any server can die without logging users out."* The exception worth knowing: **long-lived connections** — WebSockets in a [chat system](../sd-practice/07-chat-system.md) — are inherently sticky, because the connection itself is state pinned to one machine. There the game is a connection registry, not pretending the state away.

### TLS Termination

**What it is:** HTTPS has to be decrypted somewhere, and the L7 balancer is the standard place. The LB holds the certificates, does the CPU-expensive handshake, and talks plain (or lightly re-encrypted) HTTP to the app servers inside the private network.

**Key Properties:**
- Certificates live in **one place** instead of on every app server — one box to rotate, one box to audit.
- App servers shed the handshake CPU cost and see decrypted requests, which is also what lets the L7 balancer *route* on request content in the first place.
- Say "TLS terminates at the load balancer" as one sentence in Step 3 — it's a checkbox, not a deep dive, unless the prompt is security-flavored (then mention re-encrypting LB→server traffic for zero-trust networks).

### The Balancer Is a Single Point of Failure

```
   DNS: api.example.com ──► LB-A (active) ═══ heartbeat ═══ LB-B (standby)
                              │ virtual IP floats to B if A dies
                              ▼
                        [ server fleet ]
```

**What it is:** You added the LB so no single *server* could take you down — and created a single *balancer* that can. Every interviewer who hears "load balancer" is entitled to ask "and when it dies?"

- **Active–passive pairs**: two balancers share a virtual IP with a heartbeat between them; the standby claims the IP within seconds of the active one going silent. This is the standard answer.
- **DNS-level balancing**: publish multiple LB IPs under one hostname, and DNS rotates clients across them — also how you balance across *regions*. Slow to react (DNS answers get cached), so it's the coarse layer, with LB pairs as the fine one.
- In the cloud, "the LB" is a managed, already-redundant service — say that, but *also* say what it's doing under the hood. That's the difference between using the box and understanding it.

### Autoscaling Basics

**What it is:** The payoff of everything above — since servers are stateless and the LB ejects and admits nodes automatically, the fleet size can follow the load. A rule like "add servers when average CPU > 70% for 5 minutes, remove below 30%" plus the health check for admission is the whole mechanism.

- Scale on a **leading metric** (CPU, request latency, queue depth), with thresholds far enough apart that the fleet doesn't flap.
- New servers take minutes to boot — autoscaling absorbs *trends*, not *spikes*. Spikes are absorbed by headroom and by [queues](05-queues-streams.md).
- In an interview: one sentence in Step 3 ("the app tier autoscales behind the LB"), earned by having said "stateless" first. Autoscaling stateful servers is the contradiction interviewers watch for.

## The Pattern — The Stateless Fleet

Every horizontally-scaled tier on the [ladder](../../interview.md#the-design-ladder) is built the same way:

1. **Justify with numbers** — "peak 5K QPS, one server handles ~1K, so I need a fleet" (from Step 2).
2. **Make servers stateless** — sessions and shared state move to Redis ([lesson 02](02-caching.md)); servers become interchangeable.
3. **Place the LB** — L7, terminating TLS, routing round robin (or least-connections if request times vary).
4. **Name the failure handling** — health checks with eject/readmit thresholds; the LB itself runs as an active–passive pair.
5. **Close the loop** — autoscaling on CPU or latency, admitted by the same health checks.

The invariant to protect: **any two app servers are interchangeable — any request can land on any server with the same result.** The moment a request *must* reach a specific server, you've hidden state in the fleet, and you should either move the state out or say the stickiness (and its blast radius) out loud.

## The Template

The design-interview worksheet lives in [`appendix/templates/system-design/`](../appendix/templates/system-design/). Read the README (when to reach for each component, common traps), then work designs against [`template.md`](../appendix/templates/system-design/template.md) — the load balancer is a Step-3 box, and "what happens when a server dies?" is a Step-4 dive you should be able to volunteer.

## Practice

The stateless fleet carries the read path in [**Design a News Feed →**](../sd-practice/06-news-feed.md) — millions of feed reads spread across interchangeable servers. Then [**Design a Chat System →**](../sd-practice/07-chat-system.md) breaks the pattern on purpose: long-lived WebSocket connections *are* server-pinned state, and balancing them is the exercise's central problem. Every design on the [ladder](../../interview.md#the-design-ladder) starts with this front door.

## Check Yourself

- [ ] I can explain L4 vs L7 in terms of what each can see, and say why L7 is the interview default.
- [ ] I can name three routing algorithms and the situation where each wins.
- [ ] I can argue stateless + shared session store over sticky sessions in two sentences — and name the WebSocket exception.
- [ ] Asked "what if the load balancer dies?", I can answer without pausing: pairs, virtual IP, DNS above that.

---

**Up next:** [SQL vs NoSQL & Indexing](04-databases-at-scale.md) — the fleet scaled sideways; now the box behind it, where the data actually lives, and the choice interviewers love to probe.

[← Prev](02-caching.md) · [🗺 Interview Roadmap](../../interview.md) · [Next →](04-databases-at-scale.md)
