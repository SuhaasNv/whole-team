# Scoping and pushback

## Contents
- When this applies
- Step 1: Read the brief like an assessor
- Step 2: Do the capacity math
- Step 3: Choose the slice (MoSCoW and cut order)
- Step 4: Push back
- Assessments and take-home tasks
- Beyond the brief
- Examples

## When this applies

A brief, assessment, take-home task, client spec, RFP, a large feature request, or any "build X by <date>". Also any time mid-project when a new ask would push committed work out of the time box.

The scope decision is the most valuable thing you produce in the first hour. A narrow build that is complete, tested and deployed beats a wide build that is half-working, and evaluators know this.

## Step 1: Read the brief like an assessor

Read it twice. Fill `docs/01-discovery/BRIEF_ANALYSIS.md` (run `wt.py init --brief`, or `--assessment`; on an existing project it adds the flag and the missing files. For a small brief in a `lite` project, a short version at the top of `SCOPE.md` is enough):

| Section | What goes in it |
|---------|-----------------|
| Explicit requirements | Each one quoted or paraphrased with its location in the brief (section, bullet). Number them B1, B2, ... |
| What is being evaluated | The grading criteria, stated or implied. Briefs often grade judgement, code quality, tests, docs and production readiness more than feature count. |
| Constraints | Time box, stack, deliverables (README, video, deployed URL), submission format |
| Implied requirements | Things the brief assumes without saying: roles imply authentication and authorization; "status" implies a state machine; uploads imply validation and storage; "production ready" implies CI, health checks, error handling, secrets management |
| Ambiguities | Anything with two readings that cost differently. Write both readings and the cost of each. |
| Contradictions | Requirements that cannot both be true as written |
| Risks | Unknown APIs, third-party quotas, data you do not have, parts you have never built |

## Step 2: Do the capacity math

1. **Time box in focused hours.** Calendar time × realistic focus. A "3-day" task alone is about 3 × 7 = 21 hours, not 72.
2. **Reserve 30 percent** for setup, tests, docs, deployment, review and the unexpected. In an assessment these are graded, so they are not optional.
3. **Size every candidate item** in hours (S = 1 to 2, M = 3 to 5, L = 6 to 10; anything bigger is split or cut). Include its tests and docs in the size.
4. **Compare.** If the MUST items exceed 70 percent of the time box, the scope is wrong. Cut before starting, not at midnight on the last day.

Show the math to the user in a small table. Numbers make pushback a shared fact instead of an opinion.

## Step 3: Choose the slice

Prefer depth over breadth. **The recommended slice must fit:** add up its sizes and show the sum next to the hours available (`slice 14 h ≤ 15 h available`). If it does not fit, cut whole features, not quality: do not drop the UI, the tests or the deployment to squeeze more features in when the brief grades quality or expects a product people use. Pick the thinnest vertical slice that:
- exercises the hardest and most valued parts of the brief end to end,
- has every screen paired with the thing that consumes it (no dead ends),
- can be finished, tested, documented and deployed inside 70 percent of the time box.

Write `SCOPE.md`:
- **Decision in one line.** "Build A and B as one tested, deployed slice; defer C."
- **Why this scope.** Two or three sentences tying the choice to what is evaluated.
- **MUST / SHOULD / COULD / DEFERRED / MOCKED**, each row linked to the brief (B-number). SHOULD rows name their simplification. DEFERRED and MOCKED rows say *what production would need*, so a deferral reads as judgement, not omission.
- **Assumptions**, numbered (A1, A2, ...). Each is something you decided because the brief did not say.
- **Cut order**: what goes first if time runs short. Decided now, calmly.
- **Decision log**: dated one-liners each time scope changes.

## Step 4: Push back

Push back when:
- the ask does not fit the capacity math,
- the ask is ambiguous and the readings differ in cost by more than a few hours,
- the requested *solution* is a poor route to the stated *goal* (for example "add microservices" when the goal is "handle more users"),
- the ask trades away security, data integrity or tests,
- the ask is overengineering for the current need ([right-sizing.md](right-sizing.md)).

How to push back: one message, this shape, no lecture:

```
Recommendation: <what you suggest>
Why: <evidence: capacity table, brief reference, risk>
What we give up: <honest cost of your recommendation>
Alternative: <the user's version, and what it would take>
Decision needed: <the exact question, with options>
```

Then:
- If the owner agrees, update `SCOPE.md` and the decision log.
- If the owner overrules, record their decision and the stated risk in the decision log, then commit fully to it. Do not relitigate.
- Never silently build less than asked, or more.

## Assessments and take-home tasks

- The scope decision is itself graded. Make `SCOPE.md` short, confident and easy to find from the README.
- If there is a channel to the assessor, draft up to five clarifying questions in the first hour for the user to send (never send them yourself). If not, turn each open question into a numbered assumption and move on.
- Start with a walking skeleton (story 000): runnable app, database, health check, CI, deploy target. It de-risks everything else.
- Deliver the core loop polished before touching extras. Evaluators open the main path first.
- Keep `docs/10-reviews/TRACEABILITY.md` current: every brief item (B-number) maps to requirement, story, test and where it is shown, or to its DEFERRED row. Before submission, re-read the brief line by line against it.
- `AI_USAGE.md`: what the AI did, what you checked, what you changed. Many briefs ask for it; honesty here is a strength.

## Beyond the brief

Extras are allowed only when every MUST is Done and green. Label them "beyond the brief" with the reason (a real user need, not decoration). Cheap hooks that make a later extra additive (an enum value, an interface at a real seam) are fine early; the feature itself waits.

## Examples

**Capacity pushback.** The brief lists three use cases in three days.

```
Recommendation: build use cases 1 and 2 as one tested, deployed loop; defer use case 3 with a written design.
Why: sized at 26 h, 22 h and 18 h against ~15 h of build time after the 30% reserve (table above). 1 and 2 are two halves of one loop and hold the hardest parts the brief names (revisions, diffing, audit trail).
What we give up: use case 3 is described, not built. The state machine will already contain its states, so adding it later is additive.
Alternative: all three at demo quality: no E2E tests, no deployment, thin docs.
Decision needed: A) slice 1+2 (recommended)  B) all three, reduced quality
```

**Overengineering pushback.** The user asks for Kubernetes and a message queue on a two-user internal tool.

```
Recommendation: one container on a managed platform, background work in-process.
Why: no requirement names the load or failure mode a queue or cluster would solve; each adds a day of setup and a new way to fail.
What we give up: horizontal scaling we do not need yet.
Alternative: K8s + queue: about 2 days, before any feature ships.
Decision needed: A) simple deploy now, revisit at a named trigger (e.g. p95 > 500 ms or jobs > 1 min)  B) K8s + queue now
```

**Ambiguity pushback.** "Users can export their data."

```
Two readings: (1) a CSV download of their records (~2 h) or (2) a full GDPR-style export of everything including files (~1.5 days).
Recommendation: (1) now, recorded as assumption A4; (2) listed under DEFERRED with what it would need.
Decision needed: is (1) enough for this release?
```
