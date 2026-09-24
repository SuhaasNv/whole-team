# Sprint rhythm and close

## Rhythm

| Event | When | Output |
|-------|------|--------|
| Planning | Start of sprint | Goal in one sentence; stories pulled in dependency order within capacity; cut order confirmed |
| Mid-sprint check | Halfway | Anything at risk is cut or simplified now, from the cut order; `SCOPE.md` updated if scope moved; one-line note to the owner |
| Review | End of sprint | Demonstrate the sprint goal end to end (locally, or on the deployed URL once it exists) |
| Close | Right after review | The ritual below |
| Retro | Part of close | One line each: what slowed us, what we change next sprint |

Remind the owner when a sprint is ending and the close has not run.

## Sprint Definition of Done

A sprint is closed when:
1. The sprint goal is demonstrable end to end.
2. Every story marked Done meets the story Definition of Done. Stories that do not are moved back to In progress or to the next sprint, never marked Done "mostly".
3. The full test suite is green locally and CI is green on the last commit.
4. The critical journey still works; a regression blocks the close.
5. `CHANGELOG.md` has the sprint entry.
6. The board matches `USER_STORIES.md`.

## Close ritual

```
Sprint N close
- [ ] Full test suite (and e2e) green; CI green on the last commit
- [ ] wt.py lint: no errors
- [ ] git log since sprint start: conventional messages, nothing unmerged that claims Done
- [ ] Stories: Done where the DoD is met; unfinished moved to Sprint N+1 with "slipped from Sprint N: <reason>"
- [ ] Board mirrors USER_STORIES.md (wt.py kanban for a local board)
- [ ] CHANGELOG.md: "## Sprint N: <date>" with Shipped / Slipped / Retro
- [ ] SCOPE.md re-read: still true? Update MUST/SHOULD/DEFERRED and the decision log
- [ ] Commit: "docs: close sprint N"
- [ ] Tell the owner: goal met or not, what slipped, next sprint's goal
```

## CHANGELOG entry

```markdown
## Sprint 2: 2026-03-14

Goal: the review loop closes (met).

Shipped
- US-020 officer queue
- US-021 feedback on sections and documents

Slipped
- US-024 revision compare: slipped to Sprint 3, diff of document metadata took longer than sized

Retro
- Slowed us: seed data was rebuilt by hand three times.
- Change: add a seed script before Sprint 3 planning.
```

## When the sprint is clearly failing

At the mid-sprint check, if the goal cannot be met: propose the cut from the cut order to the owner with the capacity numbers, get a yes, update `SCOPE.md` and the board, and continue. A smaller goal met is better than a larger goal missed.
