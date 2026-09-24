# Requirements, use cases, stories, Definition of Done, sprints

## Contents
- Personas
- Requirements
- Use cases (standard and strict)
- Epics and user stories
- Splitting stories
- Backlog
- Definition of Ready and Definition of Done
- Sprint plan

## Personas

List every distinct role with what they want, what they must never see or do, and what they are accountable for. Never collapse two roles into one to save time; permissions are where real bugs live. A system actor (a scheduled job, an AI model) is listed too, with what it may and may not change.

## Requirements

`docs/02-requirements/REQUIREMENTS.md`. Each requirement is one testable sentence with an ID and a source:

| ID | Requirement | Source | Priority |
|----|-------------|--------|----------|
| FR-001 | An operator can save an application as a draft and return to it later | Brief B3 | MUST |
| NFR-001 | p95 API latency under 300 ms at 20 concurrent users | Assumption A2 | SHOULD |
| SEC-001 | Operators can read only their own applications | Implied by roles | MUST |

Prefixes: `FR` functional, `NFR` non-functional, `SEC` security, `UX` experience, `AI` model behaviour, `OPS` operations. Add others only if needed. IDs are never reused or renumbered; a removed requirement is marked `Dropped` with a reason.

## Use cases (standard and strict)

`docs/02-requirements/USE_CASES.md`, one per goal an actor achieves: actor, trigger, preconditions, main flow (numbered), alternative and error flows, postconditions, requirement IDs. Group them like the epics so the board, use cases and stories line up.

## Epics and user stories

`docs/05-planning/USER_STORIES.md`. `wt.py` parses this exact shape, so keep it:

```markdown
## E1: Submission

### US-010: As an operator, I want to create an application, so that I can start my licence request.
- Acceptance criteria:
  - Given I am logged in as an operator, when I choose "New application", then a draft is created and I land on its form.
  - Given another operator's draft ID, when I open it, then I get 404 and nothing is revealed.
- Priority: MUST · Sprint: 1 · Status: Not started
- Depends on: US-001 · Requirements: FR-001, SEC-001
- Tests: 
```

Before writing a story, check the request for readings that differ in cost ("export their data": a CSV of records, or everything including files?). Name the readings with rough sizes, recommend one, write the story for it, and record the other as an assumption or a DEFERRED item.

Rules:
- **Story 000 is the walking skeleton:** app runs, database migrates, health check answers, CI runs, one deploy works. Everything else builds on it.
- **Acceptance criteria are testable** and include at least one edge or failure case and, where data is owned, one authorization case.
- **Status** is one of: `Not started`, `In progress`, `In review`, `Done`, `Dropped`.
- **Sprint** is a number, or `Backlog` for stories not yet planned.
- Separate the fields on the Priority line with ` · ` (a middle dot); `wt.py` reads that shape.
- **Priority** follows `SCOPE.md`: `MUST`, `SHOULD`, `COULD`, `DEFERRED`.
- **Tests:** stays empty until Done, then names the test files or test IDs that prove the criteria.
- Optional lines `Board:` (external key) and `Branch:` may follow `Tests:`.
- IDs are stable; leave gaps rather than renumber. Dropped stories stay in the file with a reason.
- Check each story against INVEST: independent, negotiable, valuable, estimable, small, testable.

## Splitting stories

A story fits in one sprint and ideally in half a day. If it does not, split along the value, never along the layers:
- by workflow step (create, then edit, then submit)
- by role (operator view, then officer view)
- by path (happy path first, then edge cases, then error recovery)
- by data variation (one document type, then all)
- by quality level (works, then fast, then polished) only when each level is shippable

"Backend for X" and "frontend for X" are not separate stories unless each delivers something a user or tester can see.

## Backlog

Stories not yet planned into a sprint live in `USER_STORIES.md` with `Sprint: Backlog`. Ideas that are not yet stories (a drive-by refactor you noticed, tech debt, a user's wish) go as one-line bullets under the `## Backlog: candidates` heading at the end of the file, each with its source. Refinement turns candidates into stories or drops them.

## Definition of Ready and Definition of Done

`docs/05-planning/DEFINITION_OF_DONE.md` (template provided) holds both. **Ready** is the gate into a sprint (details in [sprints.md](sprints.md), Refinement); **Done** is the gate out. Tailor it at intake to the stack and profile, then treat it as a contract. It covers: acceptance criteria met, tests at the right layers, critical journey green, authorization tested, validation, error shape, docs updated per the hats table, no secrets, UI states and viewports for screens, board updated. A story that fails one item is not Done, however close it is.

For brownfield projects, the DoD starts at what the codebase can meet today and ratchets up; list the gap under "DoD debt".

## Sprint plan

`docs/05-planning/SPRINTS.md` (standard and strict) holds each sprint's goal, stories, sizes, exit criteria and cut order. How to plan, review and close a sprint: [sprints.md](sprints.md).

After writing or changing stories, run `wt.py lint` and mirror the stories on the board ([board-setup.md](board-setup.md)).
