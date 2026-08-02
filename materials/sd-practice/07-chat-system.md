# 07. Design a Chat System — Mid

The Design Ladder works like the DSA practice sets: attempt first, then peek. Work the design on paper against the [framework template](../appendix/templates/system-design/template.md) for a full 45 minutes before opening any step below — the struggle *is* the practice.

[← Back to the lesson](../system-design/05-queues-streams.md) · [🗺 Interview Roadmap](../../interview.md)

---

## The prompt

> "Design a messaging app like WhatsApp — 1:1 and small-group chats. Messages arrive in real time when the recipient is online, get delivered when they come back if not, and users can scroll their history."

Typical follow-up constraints when you ask (and you should ask — that's Step 1):

- **~50M DAU**; a message must be **durable before the sender sees a checkmark** — never lost, even if servers crash mid-flight.
- Delivery receipts: **sent / delivered / read**.
- Offline recipients get everything on reconnect.
- Multi-device (phone + laptop on one account) is a follow-up — flag it, design for one device first.

Why this design? It's the first ladder rung where request/response breaks: the *server* must initiate delivery to the client, which drags in websockets, stateful connection servers, and a routing problem no earlier design had.

<details>
<summary>Step 1 — Requirements & API</summary>

**Functional:**
- Send a message to a user or small group (~up to a few hundred members).
- Real-time delivery to online recipients; queued delivery to offline ones.
- Receipts: sent (persisted), delivered (reached device), read (opened).
- Paginated conversation history.
- Presence (online / last seen) — confirm scope; it's cheap to include, easy to over-build.

**Non-functional:**
- **Durability before acknowledgment** — the sent checkmark is a promise; persist first, ack second.
- Real-time means sub-second delivery to online users, not hard-real-time.
- Messages within a conversation appear in a **consistent order for everyone** — subtler than it sounds (Step 3).

**API sketch:**

```
# Persistent websocket, not request/response — frames both ways:
→ { "type": "send",    "conv_id": "c17", "client_msg_id": "dev1-4402", "text": "hey" }
← { "type": "ack",     "client_msg_id": "dev1-4402", "msg_id": "c17:5093", "seq": 5093 }
← { "type": "message", "conv_id": "c17", "seq": 5094, "from": "u9", "text": "yo" }
→ { "type": "read",    "conv_id": "c17", "up_to_seq": 5094 }

# History over plain HTTP — it's an ordinary paginated read:
GET /api/conversations/c17/messages?before_seq=5093&limit=50
```

One decision worth saying out loud: the client generates a **client_msg_id** before sending. It's how the sender matches acks to pending messages, and — Step 4 — it's the dedup key that makes retries safe.
</details>

<details>
<summary>Step 2 — Estimates</summary>

Keep it to one-significant-figure math (the [estimation recipes](../system-design/00e-estimation.md)):

- **Messages:** 50M DAU × ~40 messages/day = 2B/day ≈ **25K messages/s**, peak ~75K/s. Each triggers a persist plus a fan-out to a handful of recipients — call it ~100K deliveries/s peak. Real but manageable.
- **Concurrent connections:** ~10% of DAU online at once → **5M open websockets**. At ~50K–100K connections per gateway box, that's **50–100 connection servers** — the connection count, not message throughput, sizes this tier.
- **Storage:** ~200 bytes/message × 2B/day ≈ **400 GB/day → ~150 TB/year**. Must be partitioned; and the access pattern is extreme — append-heavy writes, reads overwhelmingly of the most recent messages per conversation.
- **Receipts multiply traffic:** every message spawns delivered + read events — roughly **3× the frame volume** of messages alone. Cheap frames, but budget them.

The numbers just decided the shape: a dedicated fleet sized by connections (not QPS), and a storage engine chosen for append-heavy, recent-read workloads.
</details>

<details>
<summary>Step 3 — High-level design</summary>

```
 sender ══ws══► ┌───────────┐     ┌─────────────────┐
                │ Gateway A │ ──► │  Chat service    │
                └───────────┘     │ 1 persist msg    │──► ┌─────────────┐
                                  │ 2 assign seq     │    │ Message DB  │
 ┌──────────────────────┐         │ 3 ack sender     │    │ (wide-col,  │
 │ Session registry     │ ◄─────► │ 4 fan out        │    │ by conv_id) │
 │ user → gateway addr  │         └────────┬─────────┘    └─────────────┘
 └──────────────────────┘                  │lookup
                                  online? ─┴─ offline?
 recipient ◄══ws══ ┌───────────┐              ┌──────────────┐
                   │ Gateway B │ ◄─────────── │ Offline queue │ drained
                   └───────────┘              │ per user      │ on connect
                                              └──────────────┘
```

**Why websockets:** HTTP is client-initiated ([the HTTP lesson](../system-design/00b-http-apis.md)) — the server can't push a message to a phone that hasn't asked. Polling wastes battery and adds seconds of latency; a persistent **websocket** gives a full-duplex pipe. That makes the **gateway tier stateful** — a user's connection lives on one specific box — which breaks round-robin load balancing: use **least-connections** to place new connections ([load balancing](../system-design/03-load-balancing.md)) and a **session registry** (Redis: `user → gateway address`, written on connect, heartbeat-refreshed) so anyone can find where a user is attached.

**The send flow — order matters and interviewers check it:**
1. Sender's frame arrives at Gateway A → chat service.
2. **Persist first.** The message hits the DB before anything else — a crash after this point loses nothing.
3. Assign the conversation's next **sequence number** and ack the sender (checkmark ✓).
4. Fan out: registry lookup per recipient → online: forward to their gateway, which pushes down the socket → offline: append to their per-user offline queue, drained on next connect (plus a push notification via the [notification system](05-notification-system.md) you already designed).

**Ordering:** wall-clock timestamps can't order messages — clocks skew across servers and two messages can tie. A **per-conversation sequence number** (atomic counter, natural because a conversation's messages serialize through its handler/partition) gives every participant the same total order, gives clients gap-detection ("I have 5093, received 5095 — fetch 5094"), and doubles as the history-pagination cursor.

**Message store:** 150 TB/year of append-heavy writes with reads concentrated on recent messages per conversation → an **LSM-based wide-column store** (Cassandra-style), partitioned by `conv_id` and clustered by `seq` descending ([databases at scale](../system-design/04-databases-at-scale.md)). Writes append cheaply; "last 50 messages of this conversation" is one contiguous slice of one partition.

**Groups:** same flow with a member-list lookup — fan-out of ~10–300, bounded and fine. Contrast this out loud with the [news feed's](06-news-feed.md) celebrity problem: chat caps fan-out by capping group size, which is why chat never needs the hybrid push/pull dance.
</details>

<details>
<summary>Step 4 — Deep dives & what interviewers probe</summary>

**"Can you guarantee exactly-once delivery?"** — No — nobody can, and saying so is the point. The socket drops after the server persisted but before the ack arrives; the client *must* retry or risk losing the message; the retry *may* duplicate. Standard resolution: **at-least-once plus dedup** — the retry carries the same `client_msg_id`, the server treats persist as idempotent on it, recipients dedup by message ID. The user *experiences* exactly-once because duplicates are absorbed at the edges (the full story is the [delivery-semantics lesson](../system-design/10-delivery-semantics.md)).

**"A user has a phone, a laptop, and a tablet."** — The registry becomes `user → set of (device, gateway)`; fan-out delivers to every online device and keeps a per-device delivery cursor (`last seq delivered`) so each device back-fills independently. Wrinkles worth naming: "delivered" now means *any* device, read receipts must sync across the user's own devices (reading on the phone clears the laptop's badge — the user's other devices are effectively subscribers to their own account), and the sender's other devices need their own sent messages echoed to them.

**"What exactly happens for an offline user?"** — Registry lookup misses (or the gateway's push fails — the registry can be stale; handle both) → message is already durable in the DB, so the offline queue is really just a pointer problem: store per-user `last delivered seq` per conversation and, on reconnect, the client syncs everything newer. Fire a push notification for the phone's lock screen. Key insight to say: because the DB is the source of truth, the "offline queue" can be tiny or even virtual — reconnect sync is a DB read, not a replay of a fragile buffer.

**"Presence — how does 'online / last seen' work?"** — Clients heartbeat over the socket every ~30s; the registry entry carries a TTL, and expiry means offline with `last_seen` recorded. The trap is **broadcasting**: pushing every flicker of every contact's status to everyone multiplies traffic enormously for near-zero value. Debounce transitions (offline only after a missed-heartbeat grace period) and prefer fetch-on-open over push for most presence.

**"Typing indicators?"** — The throwaway that tests judgment: **ephemeral, fine to drop**. Route gateway-to-gateway to online participants only, never persist, no retries, no receipts. If a typing frame is lost, nothing is lost. Showing you know which data *doesn't* deserve durability is as strong a signal as the persist-first flow.

**Common mistakes at this design:**
- Polling over HTTP, or hand-waving "the server pushes" without owning the stateful-gateway consequences (registry, least-connections, reconnect).
- Acking the sender before the message is durable — the checkmark that lies.
- Ordering by timestamp instead of per-conversation sequence numbers.
- Claiming exactly-once instead of at-least-once + dedup.
- Persisting typing indicators and presence flickers — durability applied indiscriminately.
</details>

---

**Next on the ladder:** [Design a Web Crawler →](08-web-crawler.md) — BFS at planetary scale, where the frontier queue is measured in billions and politeness is a hard constraint.
