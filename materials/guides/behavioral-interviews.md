# Behavioral Interviews

*Half the onsite, graded by someone who never saw your code. The method is a story bank, and it's an hour a week.*

Strong candidates fail loops on this half constantly — not because their experience is thin, but because they're retrieving stories live under pressure while the well-prepared candidate is *performing* one they've told five times. The fix is the same as for coding: build a small set of reusable pieces, drill them, rehearse the delivery. This guide is the behavioral analog of the [coding choreography](interview-guide.md).

## What's actually being graded

Not the events of the story — the *you* revealed by them:

1. **Ownership** — do you talk about what *you* did, or hide inside "we"? Say "I" for your actions, "we" for the team's outcome. Interviewers notice the candidate who can't produce a single first-person verb.
2. **Judgment** — did you weigh options, or did things just happen to you? The word "because" is your friend: "I chose X because Y."
3. **Growth** — failure questions aren't traps; they're checking whether experience changes your behavior. A failure story with no changed behavior afterward is a red flag; one with a specific change is a green one.
4. **Collaboration signal** — would this person be good to work with when something goes wrong? That's the real question under every conflict prompt.

## STAR, without the corporate varnish

Every answer is the same shape — **Situation, Task, Action, Result** — and the most common failure is spending the whole answer in S:

- **Situation** (~20 seconds): the minimum context for the story to make sense. Not the org chart, not the product history.
- **Task** (~10 seconds): what *you* specifically were on the hook for.
- **Action** (~60–90 seconds): the bulk. What you did, step by step, with the reasoning. This is the only part that scores.
- **Result** (~20 seconds): what happened, ideally with a number — and one sentence of what you'd do differently or learned.

Two to three minutes total, then *stop talking*. A crisp answer invites follow-ups; follow-ups are where you shine. A rambling answer eats the round.

## The story bank

You don't prep answers to 100 questions — you prep **6–8 stories** and route every question to one of them. Nearly all behavioral prompts collapse into a handful of categories:

| Category | The prompt sounds like… |
|----------|-------------------------|
| Conflict | "Disagreed with a teammate/manager…" |
| Failure | "A time you failed / missed a deadline / shipped a bug…" |
| Leadership / initiative | "Led without authority / went beyond your role…" |
| Ambiguity | "Unclear requirements / had to decide with incomplete info…" |
| Pressure | "Tight deadline / competing priorities…" |
| Influence | "Convinced someone / changed a decision…" |
| Proudest work | "Most impactful project / most proud of…" |
| Growth | "Hardest feedback you've received / a skill you had to build…" |

Build the bank as a matrix — stories down the side, categories across the top — and check every box at least once (good stories cover two or three):

```markdown
| Story                        | Conflict | Failure | Leadership | Ambiguity | Pressure | Influence | Proudest | Growth |
|------------------------------|----------|---------|------------|-----------|----------|-----------|----------|--------|
| Migration that went sideways |          |    ✓    |            |     ✓     |    ✓     |           |          |   ✓    |
| Disagreement over the API    |    ✓     |         |            |           |          |     ✓     |          |        |
| The intern project I rescued |          |         |     ✓      |     ✓     |          |           |    ✓     |        |
| ...                          |          |         |            |           |          |           |          |        |
```

Copy that into a file and fill it from your own history. Student or new grad? Course projects, internships, hackathons, group work, and jobs outside tech all count — the categories care about your behavior, not the org that hosted it.

For each story, write **bullets, not a script**: five to seven beats you reliably hit. Scripts sound like scripts, and the first follow-up question derails them.

## How to practice

- **Say them aloud.** Same principle as [narrating code practice](interview-guide.md) — the gap between "I know this story" and "I can tell it in two minutes" is real and only closes out loud. One story a day alongside your DSA drilling is plenty.
- **Record one occasionally.** You'll hear the rambling S and the missing R immediately. Painful, effective.
- **Drill the routing.** Have someone fire random prompts from the category table; your job is picking the right story in five seconds and landing it in three minutes. Routing is the skill the matrix builds.
- **Refresh the R.** Results with numbers ("cut the build from 40 to 12 minutes") are remembered; results like "it went well" are not. Dig the numbers out of old tickets and dashboards *now*, before you've forgotten them.

## Level expectations

The same categories get graded on different scope:

- **Junior / new grad:** stories about your own work — a bug you owned, feedback you absorbed, a deadline you managed. Nobody expects you to have led an org.
- **Mid:** stories where you influenced beyond your own tasks — unblocking a teammate, pushing back on a spec, owning a feature end to end.
- **Senior:** stories about multiplying others — mentoring, resolving cross-team conflict, making a call under ambiguity that others followed. If you're interviewing senior with only solo-work stories, that gap — not your algorithms — is the likely rejection.

Also prepare the two non-STAR staples: **"why this company?"** (a real answer needs one specific thing about them — product, scale, stack) and **"questions for me?"** (always have two; asking about team practices or the interviewer's own experience beats asking things the careers page answers).

**Related:** [interview-guide](interview-guide.md) · [interview-loop](interview-loop.md) · [🎯 Interview Roadmap](../../interview.md)
