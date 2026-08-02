# 00b. HTTP & APIs

*Every service you'll ever design speaks HTTP to someone. Know the anatomy, the verbs, and the three ways to push data back.*

[← Prev](00a-internet.md) · [🗺 Interview Roadmap](../../interview.md) · [Next →](00c-servers-scaling.md)

---

## Anatomy of a request

HTTP is plain text with a strict shape. A request is a **method + path**, some **headers** (metadata), and an optional **body**. The response mirrors it: a **status code**, headers, body.

```
REQUEST                              RESPONSE
─────────────────────────           ─────────────────────────
GET /users/42 HTTP/1.1              HTTP/1.1 200 OK
Host: api.example.com               Content-Type: application/json
Authorization: Bearer eyJh…         Cache-Control: max-age=60
Accept: application/json
                                    {"id": 42, "name": "Ada"}
(blank line = end of headers)
```

That's the whole protocol at interview level: *ask with a verb, answer with a number*.

## The verbs

**REST** is the convention of treating your API as **resources** (nouns in the URL) acted on by HTTP **verbs**:

| Verb | Means | Idempotent? |
|------|-------|-------------|
| GET | read — never changes anything | yes |
| POST | create / "do a thing" | **no** |
| PUT | replace this resource entirely | yes |
| PATCH | update part of it | not guaranteed |
| DELETE | remove it | yes |

**Idempotent** = sending the request twice has the same effect as sending it once. `DELETE /users/42` twice still leaves 42 deleted. `POST /orders` twice buys two tickets. This isn't pedantry — networks fail mid-request, clients **retry**, and retrying a non-idempotent request is how people get double-charged. The standard fix: the client sends an **idempotency key** (a unique ID per logical operation) and the server ignores duplicates. Say those two sentences in an interview and you sound like you've been paged at 3am.

## Status codes

You need about eight, and the first digit carries most of the meaning — **2xx: fine, 3xx: look elsewhere, 4xx: you messed up, 5xx: I messed up.**

| Code | Meaning |
|------|---------|
| 200 / 201 | OK / created |
| 301 | moved permanently (redirect) |
| 400 | bad request — malformed input |
| 401 / 403 | who are you? / I know who you are, and no |
| 404 | not found |
| 429 | too many requests — you're being rate-limited |
| 500 / 503 | server error / temporarily overloaded |

## Pagination

Nobody returns 10 million rows in one response. Two schemes:

- **Offset**: `GET /posts?page=3&limit=50`. Simple, but page 3 shifts if rows are inserted meanwhile, and databases get slow skipping huge offsets.
- **Cursor**: `GET /posts?after=post_988&limit=50` — "give me 50 starting after this one." Stable under inserts, fast at any depth. What every large API (and every feed you'll design) uses.

## When request/response isn't enough

HTTP is client-asks, server-answers. But chat apps, live scores, and notifications need the **server** to initiate. Three options, in escalating order of commitment:

| Technique | How it works | Use when |
|-----------|--------------|----------|
| **Long-polling** | client asks; server *holds* the request open until there's news, then client immediately re-asks | you need server push but must stay plain-HTTP |
| **SSE** (server-sent events) | one long-lived response the server keeps appending to — one-way, server → client | live feeds, notifications, progress bars |
| **WebSockets** | handshake upgrades the connection to a persistent **two-way** pipe | chat, multiplayer, anything truly interactive |

Rule of thumb: reach for the cheapest that works — polling → SSE → WebSockets. Persistent connections are stateful, and lesson [00c](00c-servers-scaling.md) explains why state makes scaling harder.

## gRPC, in one paragraph

Between your *own* services (server talking to server), JSON-over-HTTP is bulkier than needed. **gRPC** sends binary **protobuf** messages over HTTP/2 — smaller payloads, strict schemas, generated client code. Interview soundbite: *REST for public APIs, gRPC for internal service-to-service calls.* That namecheck is all most interviews want.

## Check Yourself

- [ ] I can sketch a raw HTTP request and response from memory — verb, path, headers, blank line, body.
- [ ] I can say which verbs are idempotent, why it matters for retries, and what an idempotency key does.
- [ ] I can explain cursor vs offset pagination and which one a feed should use.
- [ ] I can rank long-polling, SSE, and WebSockets and pick the right one for chat vs notifications.

---

**Up next:** [Servers, Statelessness & Scaling](00c-servers-scaling.md) — what's actually answering those requests, and the one property that lets you clone it a thousand times.

[← Prev](00a-internet.md) · [🗺 Interview Roadmap](../../interview.md) · [Next →](00c-servers-scaling.md)
