# 03. Design Typeahead / Autocomplete — Mid

The Design Ladder works like the DSA practice sets: attempt first, then peek. Work the design on paper against the [framework template](../appendix/templates/system-design/template.md) for a full 45 minutes before opening any step below — the struggle *is* the practice.

[← Back to the lesson](../system-design/02-caching.md) · [🗺 Interview Roadmap](../../interview.md)

---

## The prompt

> "Design the autocomplete for a search box — as the user types, show the top suggestions for what they've typed so far, like Google's search bar."

Typical follow-up constraints when you ask (and you should ask — that's Step 1):

- The suggestion corpus is built from real queries — **~5B searches/day** feed it.
- Return the **top 5–10** suggestions per prefix, ranked by popularity.
- **< 100ms** end-to-end per keystroke, or the suggestions feel laggy and useless.
- A daily refresh of rankings is fine; surfacing trending queries faster is a follow-up, not the baseline.

Why this design? It's the [trie lesson](../learning/09-tries.md) wearing infrastructure clothes — and the honest comparison between "the data structure I'd use in a coding round" and "the precomputed table I'd actually ship" is exactly the judgment interviewers are probing for.

<details>
<summary>Step 1 — Requirements & API</summary>

**Functional:**
- Given a prefix, return the top 5–10 completed queries, ranked by historical popularity.
- Suggestions update as the corpus changes (daily is acceptable).
- (Confirm scope) personalization, trending queries, filtering offensive suggestions — usually follow-ups, not baseline.

**Non-functional:**
- **Read-dominated to an extreme degree** — every keystroke is a read; writes are an offline pipeline. This is a caching problem before it's anything else.
- < 100ms per keystroke including network; the server's share is maybe 20–40ms.
- Availability over freshness: stale-by-a-day suggestions are fine, *no* suggestions feel broken.

**API sketch:**

```
GET /api/suggest?q=how+to+t
  returns 200: { "suggestions": [
    "how to tie a tie",
    "how to train your dragon",
    "how to type faster", ...
  ] }
```

One decision worth saying out loud: **the client debounces.** Fire the request ~100–200ms after the user pauses, not on every keystroke — a fast typist generates 10 keystrokes/s and most intermediate prefixes are never seen. Cutting request volume 5–10× *before the design starts* is the cheapest optimization in the whole system, and saying it first shows you think end-to-end.
</details>

<details>
<summary>Step 2 — Estimates</summary>

Keep it to one-significant-figure math (the [estimation recipes](../system-design/00e-estimation.md)):

- **Read QPS:** 5B searches/day, each preceded by say ~4 suggest requests after debouncing → 20B/day ≈ 20B / 86,400s ≈ **200K QPS**, peak ~500K/s. This is a *big* read load — no single anything survives it; caching and replication are mandatory, not optional.
- **Corpus size:** of 5B daily searches, maybe ~100M distinct queries worth suggesting. At ~50 bytes each ≈ **5 GB of raw queries**.
- **Precomputed table:** each query has as many prefixes as characters (~20), so ~2B prefix entries; each stores ~10 suggestions ≈ 500 bytes → **~1 TB**. Too big for one machine's RAM — but shards across ~10 nodes at 100 GB each, or far less if you only precompute prefixes up to ~6 chars and let longer prefixes filter client-side.
- **Skew:** prefix popularity is brutally power-law — "a", "the", "how to" dominate. A small cache of the hottest few million prefixes (a few GB) absorbs the vast majority of the 200K QPS.

The numbers just decided the architecture: precompute offline (writes are a batch job, not a hot path), shard the table, and put a cache in front sized to exploit the skew.
</details>

<details>
<summary>Step 3 — High-level design</summary>

```
 keystroke (debounced)
      │        browser cache / CDN edge — hottest prefixes
      ▼              │
 ┌─────────┐   ┌─────▼──────┐    ┌──────────────────────┐
 │ Client  │──►│ Suggest    │───►│ Prefix store (shard-  │
 │         │◄──│ service +  │    │ ed KV): prefix →      │
 └─────────┘   │ hot cache  │    │ [top-10 suggestions]  │
               └────────────┘    └──────────▲───────────┘
                                            │ daily publish
               ┌────────────────────────────┴───────────┐
               │ Offline pipeline: query logs → count/  │
               │ aggregate → rank → build prefix table  │
               └────────────────────────────────────────┘
```

**The read path:** client debounces → CDN/browser cache for the very hottest prefixes → suggest service checks its in-memory cache → on miss, one key-value lookup in the sharded prefix store. Every hop is a straight cache lookup — that's how you hit the latency budget.

**The data-structure decision** — the heart of this design; compare honestly:

1. **A live trie** — the DSA answer. Walk the prefix, collect completions. Naively, collecting top-k below a node means exploring the whole subtree — far too slow — so real trie designs have **each node cache its own top-k list**, updated as counts change. Now reads are O(prefix length), but updates must propagate up every ancestor's cached list, the structure must fit in RAM and be replicated/sharded, and concurrent update-while-serving gets hairy. Workable; operationally sharp-edged.
2. **A precomputed prefix → top-k table** — flatten the trie: for every prefix, precompute its top 10 into a giant hash map, rebuilt offline daily and published to a sharded KV store. Reads are one exact-key lookup — the simplest, fastest possible read path — and the "hard" ranking work runs as a batch job where failures are retried, not user-visible.

Pick the **precomputed table**. The requirements said daily refresh is fine — that concession is exactly what lets you trade the trie's update capability for a dumber, faster read path. Say the bridge out loud: *the table is a trie with every path materialized*; you'd revisit the live trie (or a hybrid) if freshness requirements tightened to minutes.

**The pipeline:** query logs → aggregate counts (MapReduce/Spark-style batch over the day's 5B queries) → rank per prefix → build table shards → publish atomically (build new, flip a pointer — never mutate the live table in place).

**Sharding:** by prefix (hash of the first few characters, or range). Watch the **hot shard**: single-letter prefixes like "a" and "s" carry wildly more traffic than "xq". Answer: the cache layer absorbs hot prefixes before they hit shards, and the hottest handful can be replicated to every node outright.
</details>

<details>
<summary>Step 4 — Deep dives & what interviewers probe</summary>

**"Where does caching happen?"** — Layers, and name all of them: client debounce (avoid the request), browser cache (same user retypes), CDN edge for the globally hottest prefixes (`GET /suggest?q=a` is identical for everyone — perfectly cacheable with a short TTL), the suggest service's in-memory hot set, then the store. Each layer strips traffic before the next — this is the [caching lesson](../system-design/02-caching.md) as a whole system.

**"What about trending queries — a news event breaks and the daily rebuild is 20 hours away?"** — Bolt on a small real-time path: a streaming job counts queries over the last ~10 minutes, keeps a modest set of spiking queries, and the suggest service **merges** trending hits into the precomputed top-10 at read time. Don't rebuild the table faster; augment it — batch for the base, stream for the delta.

**"Personalized suggestions?"** — Keep the shared table as the candidate source, then re-rank the top ~50 candidates per user at request time using a small per-user profile (recent searches). Precomputing per-user tables for hundreds of millions of users is the wrong answer — say why: the storage multiplies by users while most of the win comes from cheap re-ranking.

**"A prefix returns something offensive."** — Filtering belongs in the offline pipeline (blocklist + classifier before publish), plus a fast-path suppression list the service checks at read time for same-day takedowns. Nice signal to raise it before the interviewer does.

**Common mistakes at this design:**
- Answering "trie" and stopping — without top-k-per-node caching a live trie can't meet the latency, and without owning update propagation it isn't a real design.
- No client debounce — volunteering 10× the necessary load.
- Ignoring prefix skew — sharding evenly by hash and then acting surprised that the "a" shard melts.
- Rebuilding or mutating the live table in place instead of build-and-swap.
</details>

---

**Next on the ladder:** [Design a Top-K Leaderboard →](04-top-k-leaderboard.md) — top-k again, but now the counts change in real time and the heap pattern takes center stage.
