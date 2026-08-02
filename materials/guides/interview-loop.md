# The Interview Loop

*What actually happens between "a recruiter emailed me" and an offer — stage by stage, with what each one really grades.*

Candidates prepare for interviews; loops are what companies actually run. Knowing the shape — who you'll talk to, what each conversation is for, where people exit the funnel — turns a months-long anxiety fog into a sequence of known events you can prep for individually. The stages below are the big-tech default; startups compress or skip some, which is exactly why you ask (see the checklist at the bottom).

## The shape of the funnel

| Stage | Typically | What's graded | Prep with |
|-------|-----------|---------------|-----------|
| Recruiter screen | 30 min call | Interest, logistics, level fit | This guide |
| Phone screen | 45–60 min, 1–2 coding problems | Coding at the bar | [The Coding Interview](interview-guide.md) |
| Onsite: coding ×2 | 45 min each | Problem solving, communication | [DSA Roadmap](../../roadmap.md) + [interview-guide](interview-guide.md) |
| Onsite: system design | 45–60 min | Trade-off reasoning at your level | [SD track](../../interview.md#pillar-3--system-design) |
| Onsite: behavioral | 45 min | Ownership, judgment, collaboration | [behavioral-interviews](behavioral-interviews.md) |
| Debrief + committee | You're not in the room | The written record of all of the above | Done already — or not |

The funnel is steep: most candidates exit at the phone screen, and most onsite rejections cite the round the candidate didn't prepare — usually behavioral or system design, almost never "one more hard LeetCode problem would have saved it."

## Recruiter screen

A 30-minute conversation with a non-engineer whose job is filling the pipeline with plausible candidates. It is not technical and you cannot ace it — but you can fumble it by being unable to say what you want, or by letting the level conversation happen *to* you.

- Have a 60-second "tell me about yourself": current role/status → one or two concrete things you've built → why you're looking. That's it.
- **Level is set here.** If you're borderline mid/senior, this call often decides which loop you get. Know what level you're targeting and say so.
- Ask what the process looks like — number of rounds, formats, timeline. This is expected, not pushy.
- Nothing said here helps you much, but contradicting it later (comp expectations, availability, level) hurts. Be consistent.

## Phone screen

One or two coding problems in a shared editor (CoderPad-style, usually no autocomplete), 45–60 minutes, camera on. The bar is "clearly worth a full onsite": a working solution to a LeetCode-medium-grade problem, narrated well, tested unprompted.

Everything in [the coding choreography](interview-guide.md) applies from minute one — restate, clarify, brute force, sign-off, narrate, test. Screeners grade fewer dimensions than onsite interviewers, and working-code-plus-clear-thinking dominates. Practice in a bare editor at least a few times first; discovering you can't remember [`heapq`](../syntax/heapq-module.md)'s argument order live is a bad time.

## The onsite

Three to five rounds, back to back, each with a different interviewer scoring independently — which has two useful consequences. First, **a bad round is one data point, not a verdict**; loops forgive one weak coding round with strong everything-else constantly. Reset between rounds like a goalie after a goal. Second, **you must re-establish context every round**: the next interviewer hasn't read the last one's notes, so your setup, your questions, your energy start fresh each time.

- **Coding rounds (usually two):** same skill as the phone screen at slightly higher difficulty or with follow-ups. One is sometimes themed (debugging, refactoring, OOP-flavored) — the choreography doesn't change.
- **System design (mid-level and up; sometimes lighter for juniors):** the round where level is truly decided. Run [the framework](../system-design/01-design-framework.md); the grading is trade-offs stated aloud, not the "right" architecture. Junior loops that include it grade fundamentals and structure, not distributed-systems depth.
- **Behavioral (at least one; sometimes woven into every round's first ten minutes):** the [story bank](behavioral-interviews.md), routed and delivered. At many companies this round carries veto power that surprises people — treat it as a full technical round in prep weight.
- Every round ends with "questions for me?" — have two ready and vary them; interviewers compare notes on candidates who asked everyone the same thing.

## Debrief & decision

After the onsite, each interviewer submits written feedback and a score, then a debrief meeting (or hiring committee at larger companies) weighs the packet. Useful things to know about a room you'll never sit in:

- **The written record is the whole game.** "Solved it after a hint, tested unprompted, clear communicator" is what survives to the committee — a specific, quotable performance beats a vaguely fine one.
- **One strong champion matters.** A round where an interviewer genuinely enjoyed working with you often outweighs a mediocre-everywhere packet. This is why communication is graded everywhere: it's what makes champions.
- **Borderline packets get resolved by level**, not rejected outright — the mid/senior candidate with a shaky design round gets offered mid. If that happens, it's a data point about which pillar to strengthen, not a scam.
- Decisions typically land inside one to two weeks; a delay usually means scheduling or headcount noise, not a coded message. One polite nudge after a week of silence is fine.

## Ask the recruiter (before you prep)

Five minutes of questions reallocates weeks of prep:

- [ ] How many rounds, and what format is each? ("Two coding, one design, one behavioral" changes everything.)
- [ ] Is there a system design round at my level? What depth is expected?
- [ ] What editor/environment for coding rounds? Autocomplete or bare?
- [ ] Language constraints, if any?
- [ ] Timeline — when would the onsite be, and when do decisions come?

Then split your remaining prep time across the [three pillars](../../interview.md) in proportion to what they told you — not in proportion to which pillar you enjoy practicing.

**Related:** [interview-guide](interview-guide.md) · [behavioral-interviews](behavioral-interviews.md) · [🎯 Interview Roadmap](../../interview.md)
