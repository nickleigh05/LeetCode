# 00a. How the Internet Works

*Four steps — name, connect, secure, talk — sit underneath every system you will ever design.*

[← Interview Roadmap](../../interview.md) · [🗺 Interview Roadmap](../../interview.md) · [Next →](00b-http-apis.md)

---

## The interview's favorite warm-up

"What happens when you type a URL and press Enter?" is the oldest question in the book, and it's asked because the answer *is* the internet in miniature. Every system-design diagram you'll draw later — load balancers, CDNs, caches — exists to speed up or multiply exactly one of the steps below. Learn the trip once and the rest of the track is variations on it.

## Step 1: DNS — turn a name into an address

Computers route by number, not by name. **DNS** (Domain Name System) is the internet's phone book: it maps `example.com` to an IP address like `93.184.216.34`.

Your browser doesn't call the phone book's headquarters every time. It checks a chain of **caches** first — browser cache, then the operating system, then your ISP's **resolver**. Only on a full miss does the resolver walk the hierarchy: root servers → `.com` servers → the **authoritative** server that actually owns the answer. Each answer carries a **TTL** (time to live) that says how long it may be cached — which is why DNS changes "take a while to propagate."

## Step 2: TCP/IP — open a connection

With an IP address in hand, your machine opens a connection.

- **IP** moves **packets** — small chunks of data — hop by hop across routers toward the destination address. It promises nothing: packets can arrive late, out of order, or not at all.
- **TCP** sits on top and adds the guarantees: every packet acknowledged, lost ones re-sent, everything reassembled in order. Reliability built on an unreliable substrate.

Opening a TCP connection takes a **three-way handshake** — SYN, SYN-ACK, ACK — which costs **one full round trip** before a single byte of your actual data moves.

## Step 3: TLS — make it private

For `https://`, a **TLS handshake** runs next: the server presents a **certificate** proving it really is `example.com`, and both sides agree on keys to encrypt everything that follows. That's roughly **one more round trip**. Every modern site pays this toll — which is one reason connections get *reused* instead of re-opened per request.

## Step 4: talk

Only now does the browser send the actual **HTTP request** (`GET /`), and the server sends back HTML. The whole trip:

```
you press Enter
     │
     ▼
┌─────────┐  1. "example.com?"           ┌──────────────┐
│ browser │─────────────────────────────►│ DNS resolver │
│         │◄─────────────────────────────│  (+ caches)  │
└────┬────┘      "93.184.216.34"         └──────────────┘
     │
     │  2. TCP handshake ──── 1 round trip
     │  3. TLS handshake ──── ~1 more round trip
     │  4. GET / ──────────── the actual request, at last
     ▼
┌──────────┐
│  server  │ ── HTML comes back; browser renders it
└──────────┘
```

Notice the shape: **two-plus round trips of overhead before any real work**. If the server is across an ocean, that overhead alone is a third of a second.

## The physical constants

These are the latency numbers behind every design decision — the system-design equivalent of knowing that gravity is 9.8 m/s². Rough orders of magnitude are all you need:

| Operation | Cost |
|-----------|------|
| L1 cache reference | ~1 ns |
| Main memory reference | ~100 ns |
| SSD random read | ~100 μs |
| Read 1 MB sequentially from memory | ~250 μs |
| Round trip within a datacenter | ~500 μs |
| Read 1 MB from SSD | ~1 ms |
| Disk seek (spinning disk) | ~10 ms |
| Round trip across a continent/ocean | ~150 ms |

Read it as ratios, not digits: **memory beats disk by ~100,000×**, and a cross-continent round trip costs ~300× a trip within the datacenter. Caching exists because of the first ratio. CDNs — copies of your data parked near users — exist because of the second. When a later lesson adds a box to a diagram, come back here and find the row it's fighting.

## Check Yourself

- [ ] I can narrate "what happens when you press Enter" in four steps — DNS, TCP, TLS, HTTP — without notes.
- [ ] I can explain why DNS is fast in practice (caches + TTLs) even though the full lookup walks a hierarchy.
- [ ] I know roughly what memory, SSD, disk seek, and a cross-ocean round trip each cost — and which ratio justifies caching.

---

**Up next:** [HTTP & APIs](00b-http-apis.md) — the language spoken over that hard-won connection: verbs, status codes, and what "idempotent" buys you.

[← Interview Roadmap](../../interview.md) · [🗺 Interview Roadmap](../../interview.md) · [Next →](00b-http-apis.md)
