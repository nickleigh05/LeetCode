# 00c. Servers, Statelessness & Scaling

*One server handles the first thousand users. The whole discipline of system design is what you do about user 1,000,001.*

[← Prev](00b-http-apis.md) · [🗺 Interview Roadmap](../../interview.md) · [Next →](00d-databases-101.md)

---

## Client and server are roles, not machines

A **client** asks; a **server** answers. That's it. Your browser is a client of a web server; that web server is a *client* of a database. Any box in a diagram can wear both hats at once — keep this in mind and big architectures stop looking mysterious, because every arrow is just the request/response pair from [00b](00b-http-apis.md).

Two server flavors you'll hear named:

- **Web server** — speaks HTTP, serves static files, terminates TLS, forwards the interesting requests onward (nginx is the classic).
- **App server** — runs *your code*: validates the request, applies business logic, talks to the database.

In small systems they're one process. In interviews, draw them as one box labeled "app servers" unless asked — nobody wants the nginx config.

## Two ways to scale

Your single server is pegged at 100% CPU. Options:

```
VERTICAL — buy a bigger box            HORIZONTAL — buy more boxes
┌──────────┐       ┌────────────┐      ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐
│  4 CPUs  │  ──►  │  64 CPUs   │      │ srv │ │ srv │ │ srv │ │ srv │
│  16 GB   │       │  512 GB    │      └─────┘ └─────┘ └─────┘ └─────┘
└──────────┘       └────────────┘         identical clones, side by side
ceiling: biggest machine money buys    ceiling: much, much higher
single point of failure: still yes     one dies? the others shrug
```

**Vertical scaling** (scale *up*) is the right first move — zero code changes, no new complexity. But it hits a hard ceiling, the price curve goes superlinear, and you still have exactly one machine to lose. **Horizontal scaling** (scale *out*) is how every large system works: many cheap, identical, disposable servers. The catch is that horizontal scaling only works if any clone can serve any request — which brings us to the real subject of this lesson.

## Statelessness — the property that makes clones possible

Suppose your server keeps the user's session — "logged in as Ada, cart has 3 items" — in its own memory. Now Ada's *next* request **must** land on that same server, or she's mysteriously logged out. You've created **sticky sessions**: the load balancer has to remember who belongs where, a server crash logs out everyone it was holding, and you can't drain a machine for deploys without breaking users mid-session.

The fix is to make servers **stateless**: no request-to-request memory lives on the server itself. Push the state *out* — sessions into a shared cache, data into the database, the user's identity into a signed token the client carries with every request. Now every server is interchangeable:

```
stateful  ✗  request must find "its" server   (servers are pets — named, irreplaceable)
stateless ✓  any request → any server          (servers are cattle — numbered, replaceable)
```

Stateless services scale horizontally by doing nothing at all: traffic doubles, you launch more copies; a copy dies, you shoot it and launch another. **State didn't disappear — it moved** to databases and caches, which is exactly why the rest of this track is mostly about *those*.

## The load balancer — one box, for now

Something has to spread incoming requests across the clones. That's the **load balancer**:

```
                    ┌──────────┐ ──► server A
   clients ───────► │ load     │ ──► server B      each request → some
                    │ balancer │ ──► server C      healthy server
                    └──────────┘ ──► server D
```

It distributes requests (round-robin is the default mental model), **health-checks** the servers, and quietly stops sending traffic to dead ones. For now, treat it as a single magic box you draw in front of any horizontally-scaled tier. How it picks a server, how *it* avoids being the single point of failure, and layer-4 vs layer-7 — all of that is the deep dive in lesson 03. Resist the urge to explain it before then; in an interview, "requests hit a load balancer in front of N stateless app servers" is a complete, correct sentence.

## Check Yourself

- [ ] I can explain why an app server is a *client* of the database without hesitating.
- [ ] I can give one real advantage and one real limit of vertical scaling.
- [ ] I can explain sticky sessions — what causes them, why they hurt, and where the state should move instead.
- [ ] I can draw the clients → load balancer → stateless servers picture and say why "any request → any server" is the whole point.

---

**Up next:** [Databases from First Principles](00d-databases-101.md) — the place all that displaced state actually went, and what an index really is under the hood.

[← Prev](00b-http-apis.md) · [🗺 Interview Roadmap](../../interview.md) · [Next →](00d-databases-101.md)
