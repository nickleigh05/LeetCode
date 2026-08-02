# 00f. Foundations Drills

*Reading about systems is not the same as reasoning about them. This lesson makes you do it.*

[← Prev](00e-estimation.md) · [🗺 Interview Roadmap](../../interview.md) · [Next →](01-design-framework.md)

---

Lessons 00a–00e gave you the vocabulary. These drills make you *use* it — out loud if you can, because that's how the interview works. Attempt each one fully before opening the answer; a peeked answer teaches nothing.

## Trace a Request

**Drill 1 — cold start.** On a brand-new laptop you type `https://newsite.example` and press Enter. List every network step before the first byte of HTML arrives.

<details>
<summary><strong>Answer</strong></summary>

1. **DNS** — browser cache misses (new laptop), OS cache misses, so the resolver walks the hierarchy: root → `.example` TLD → authoritative server → IP address comes back (and gets cached with a TTL).
2. **TCP handshake** — SYN, SYN-ACK, ACK: one round trip, connection open.
3. **TLS handshake** — certificate verified, keys agreed: roughly one more round trip.
4. **HTTP** — `GET /` finally goes out; the server responds with HTML.

Bonus points for noting the shape: two-plus round trips of pure overhead before any content, which is why connections are reused and why a far-away server feels slow even when it's fast. ([00a](00a-internet.md))
</details>

**Drill 2 — the dropped POST.** Your phone app sends `POST /orders` to buy a concert ticket. The connection dies before any response arrives. Did the order go through? What should the app do?

<details>
<summary><strong>Answer</strong></summary>

**You cannot know.** The request may have died on the way *in* (no order exists) or the response died on the way *out* (the order exists and you paid). Both look identical from the client.

Blind retry is wrong — POST is **not idempotent**, so a retry risks two tickets. Not retrying is also wrong — maybe there's no order at all. The fix: the app attaches an **idempotency key** (a unique ID generated per purchase attempt) and retries freely; the server recognizes a key it has already processed and returns the original result instead of ordering twice. GET/PUT/DELETE could have been retried without ceremony — this dance is the price of POST. ([00b](00b-http-apis.md))
</details>

## Estimate

**Drill 3 — photo app.** 10M DAU, each uploads 2 photos/day at ~2 MB each. Find upload QPS (average and peak), storage/day, and storage/year.

<details>
<summary><strong>Answer</strong></summary>

```
uploads/day = 10M × 2              = 20M
upload QPS  = 20M ÷ 100K           ≈ 200        peak ≈ 600
storage/day = 20M × 2 MB           = 40 TB/day
storage/yr  = 40 TB × 400          ≈ 16 PB      call it ~15 PB/year
```

200 QPS is trivial; **15 PB/year is the design driver** — blob storage, and probably a conversation about compression and cold tiers.
</details>

**Drill 4 — feed reads.** 50M DAU open their feed 5×/day; each open fetches 20 posts at ~1 KB per post. Find read QPS and response bandwidth.

<details>
<summary><strong>Answer</strong></summary>

```
opens/day = 50M × 5                = 250M
read QPS  = 250M ÷ 100K            ≈ 2,500      peak ≈ 7,500
payload   = 20 × 1 KB              = 20 KB per response
bandwidth = 2,500 × 20 KB          = 50 MB/s    (peak ~150 MB/s)
```

Note the asymmetry versus a write path: feeds are **read-heavy**, usually by 10–100×, which is why caching shows up in every feed design.
</details>

**Drill 5 — URL shortener.** 100M new short links per year, each record ~500 bytes. Find write QPS and storage after 10 years.

<details>
<summary><strong>Answer</strong></summary>

```
write QPS = 100M ÷ 3×10⁷ s/year    ≈ 3 QPS (!)
storage   = 100M × 500 B           = 50 GB/year → 500 GB in 10 years
```

Both numbers are tiny — a decade of TinyURL's writes fits on a laptop. The lesson: **run the envelope before assuming you need scale.** The hard part of a URL shortener is the *read* path and its availability, not the writes. ([00e](00e-estimation.md))
</details>

## Pick a Database

For each, name a data model (relational / document / key-value), and — the part that's actually graded — the *reason*.

**Drill 6 — bank transfers.** Moving money between accounts; a debit without its matching credit is a lawsuit.

<details>
<summary><strong>Answer</strong></summary>

**Relational**, no hesitation. You need **ACID transactions** — atomicity makes debit + credit one all-or-nothing unit, isolation stops concurrent transfers from double-spending a balance, durability means "transfer complete" survives a crash. The data is also rigidly structured and heavily relational (accounts ↔ ledger entries). This is the guarantee-shaped problem from [00d](00d-databases-101.md).
</details>

**Drill 7 — session store.** Millions of lookups/sec of "is this session token valid, and whose is it?"; sessions expire after 30 minutes; losing one just means a user logs in again.

<details>
<summary><strong>Answer</strong></summary>

**Key-value, in memory** (Redis-style). The access pattern is exactly one operation — `token → session` — so a giant hash map is the perfect shape; TTL expiry is built in; and since loss is cheap, you can trade durability for memory-speed reads. This is also the shared store that keeps your app servers stateless ([00c](00c-servers-scaling.md)).
</details>

**Drill 8 — product catalog.** Millions of products where every category has different attributes — laptops have RAM, shoes have sizes — and each product page reads the whole record at once.

<details>
<summary><strong>Answer</strong></summary>

**Document store** is the textbook answer: each product is a self-contained blob with its own shape, read as one unit, essentially never joined — flexibility is the whole requirement. A defensible alternative: relational with a JSON column for the variable attributes, keeping ACID for inventory and orders. Either passes *if you argue it*; "MongoDB because it's fast" fails with either database.
</details>

## Check Yourself

- [ ] I answered every drill before opening the details block — honestly.
- [ ] I can narrate Drill 2's ambiguity (request died vs response died) and the idempotency-key fix without notes.
- [ ] My estimation answers matched to within one order of magnitude, using one-significant-figure arithmetic.
- [ ] For each database drill I gave a *reason* tied to guarantees, access pattern, or data shape — not a brand name.

---

**Up next:** [The Design Framework](01-design-framework.md) — foundations done. Now the repeatable four-step method for driving an actual 45-minute design interview.

[← Prev](00e-estimation.md) · [🗺 Interview Roadmap](../../interview.md) · [Next →](01-design-framework.md)
