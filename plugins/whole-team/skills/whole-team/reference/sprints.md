# Sprints and ceremonies

## Contents
- Cadence
- Sprint planning
- Daily start
- Refinement
- Change control during a sprint
- Mid-sprint check
- Sprint review
- Retrospective
- Sprint close
- When the sprint is failing

Keep each ceremony short. Each one exists so the owner knows the goal, what is in the sprint, what changed and why.

## Cadence

| Event | When | Time (1-day sprint / 1-week sprint) | Output |
|-------|------|-------------------------------------|--------|
| Sprint planning | Start of sprint | 15 min / 45 min | Goal, committed stories, cut order; owner yes |
| Daily start | Start of each session | 2 min | Status line to the owner |
| Refinement | Before planning; whenever a story is unclear | 10 min / 30 min | Ready stories |
| Mid-sprint check | Halfway | 5 min | Risks cut or simplified now |
| Sprint review | End of sprint | 15 min / 30 min | Goal demonstrated; owner accepts stories |
| Retrospective | After review | 5 min / 20 min | Actions with owners |
| Sprint close | After retro | 10 min | Ritual below; `docs: close sprint N` |

Remind the owner when a sprint is ending and the review, retro or close has not run.

## Sprint planning

Inputs: `wt.py status`, `wt.py lint`, last sprint's retrospective actions, the backlog, `SCOPE.md`.

```
Sprint N planning
- [ ] Last retro's actions: each done, carried over or dropped (update RETROSPECTIVES.md)
- [ ] Slipped stories from last sprint considered first
- [ ] Goal: one sentence a user would understand ("An operator can submit an application")
- [ ] Stories pulled in dependency order; each meets the Definition of Ready
- [ ] Capacity: sum of sizes ≤ 70% of the sprint's focused hours (the rest is reserve)
- [ ] Exit criteria: what will be demonstrated at the review
- [ ] Cut order: what goes first if the sprint runs late
- [ ] SPRINTS.md updated; stories' Sprint field set; board mirrors it
- [ ] Owner says yes to the plan
```

Set `sprint.current` in `.whole-team.json` to N.

## Daily start

At the start of every session, before any work:
1. Run `wt.py status`.
2. If there is an open `Handover:` line, resume from it.
3. One line to the owner: `Sprint 2, day 3: US-021 in review, US-022 next. Goal on track. Decide: none.`

## Refinement

A story is ready (Definition of Ready) when:
- it is written as `As a <persona>, I want <capability>, so that <value>` and a user or tester could see the value;
- every acceptance criterion is testable and includes a failure case, plus an authorization case where data is owned;
- it is sized, and fits in one sprint (ideally half a day or less; otherwise split it, see [requirements-and-stories.md](requirements-and-stories.md));
- its dependencies are Done or planned earlier in the same sprint;
- screens: the design is approved, or approving it is the story's first task;
- open questions are answered, or recorded as assumptions.

Do not pull a story that is not ready into a sprint.

## Change control during a sprint

Never add a new request mid-sprint (a feature, a "quick change", an idea) silently:
1. Write it as a story (or a bug) and size it.
2. Tell the owner the trade: "Adding US-031 (3 h) means dropping US-027 (3 h) from this sprint, or taking US-031 next sprint."
3. On a yes, update the sprint plan, the board and the `SCOPE.md` decision log.

Exceptions: fix a bug that breaks the critical journey now; raise a security issue immediately.

## Mid-sprint check

Halfway through: is the goal still reachable? If not, propose the cut from the cut order with the numbers, get a yes, and update `SCOPE.md`, the sprint plan and the board. One line to the owner either way.

## Sprint review

1. Run `wt.py sprint N` for planned, shipped and not done.
2. Demonstrate the sprint goal end to end: locally in early sprints, on the deployed environment once it exists. Walk the exit criteria.
3. For each story marked Done, the owner accepts or rejects it. Move a rejected story back to In progress with the reason.
4. Note feedback as new or changed stories for refinement; build nothing during the review.

## Retrospective

Add an entry to `docs/05-planning/RETROSPECTIVES.md` (in `lite`, three lines in `CHANGELOG.md`):
- Goal met, partly met or not met; planned vs done from `wt.py sprint N`.
- Went well, slowed us, surprised us: a few honest lines each, about the process, not only the code.
- **Actions:** one to three concrete changes, each an unchecked item with an owner and "check at Sprint N+1 planning". An action is a change in how you work ("add a seed script before planning", "size stories with tests included"), not a wish.
- Last sprint's actions: done, carried over, or dropped, each with a word on why.

Draft the whole entry from what you already know, show it, then ask the owner what to add. `wt.py status` counts open actions until they are checked.

## Sprint close

A sprint is closed when:
1. The sprint goal is demonstrable end to end.
2. Every story marked Done meets the story Definition of Done and was accepted at the review. Others move back to In progress or to the next sprint, never marked Done "mostly".
3. The full test suite is green locally and CI is green on the last commit.
4. The critical journey still works; a regression blocks the close.
5. `CHANGELOG.md` has the sprint entry; the retrospective is written.
6. The board matches `USER_STORIES.md`.

```
Sprint N close
- [ ] Full test suite (and e2e) green; CI green on the last commit
- [ ] wt.py lint: no errors
- [ ] git log since sprint start: conventional messages; nothing claiming Done left unmerged
- [ ] Unfinished stories: Sprint = N+1, "slipped from Sprint N: <reason>" in their notes and on the board; partial work stays on its branch
- [ ] Board mirrors USER_STORIES.md (wt.py kanban for a local board)
- [ ] CHANGELOG.md: "## Sprint N: <date>" with Goal, Shipped, Slipped, Retro link
- [ ] Retrospective entry written with actions
- [ ] SCOPE.md re-read: still true? Update MUST/SHOULD/DEFERRED and the decision log
- [ ] Commit: "docs: close sprint N"
- [ ] Tell the owner: goal met or not, what slipped, the top retro action, next sprint's proposed goal
```

CHANGELOG entry:

```markdown
## Sprint 2: 2026-03-14

Goal: the review loop closes (met). Planned 5, done 4, slipped 1.

Shipped
- US-020 officer queue
- US-021 feedback on sections and documents

Slipped
- US-024 revision compare: to Sprint 3, diff of document metadata took longer than sized

Retro: docs/05-planning/RETROSPECTIVES.md#sprint-2-retro (action: seed script before Sprint 3 planning)
```

## When the sprint is failing

At the mid-sprint check or earlier: propose the cut from the cut order to the owner with the capacity numbers, get a yes, update `SCOPE.md`, the sprint plan and the board, and continue. Meet a smaller goal rather than miss a larger one.
