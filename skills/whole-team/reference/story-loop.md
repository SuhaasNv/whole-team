# Story loop

## Contents
- 1. Pull
- 2. Start
- 3. Plan
- 4. Build
- 5. Verify
- 6. Hats pass
- 7. Review
- 8. Done and merge
- 9. Report
- Bugs
- Interrupted sessions

Branch names and the integration branch come from `.whole-team.json` (defaults: story branch `feat/us-<id>-<slug>`, integration `dev`, release `main`). Branch types, merge strategy, rebasing and recovery: [branching.md](branching.md).

## 1. Pull

- Take the next story from `wt.py status` (lowest sprint, dependencies Done, not blocked) unless the user named one.
- WIP limit: if two stories are already In progress, finish one first.
- Read its acceptance criteria. If any is vague or untestable, fix it with the owner now; do not guess.

## 2. Start

```bash
git switch <integration> && git pull --ff-only   # skip pull if there is no remote
git switch -c feat/us-<id>-<slug>
```

- Set the story to `In progress` in `USER_STORIES.md` and on the board in the same turn.
- Screens: the design must already be approved ([design.md](design.md)). If not, that is the first task.

## 3. Plan

Write a short plan: files you expect to touch, tests you will add, risks (migrations, shared state, auth, public API changes). If the change is large (roughly more than 50 changed lines, or more than one module) and the approach was not already agreed, show the plan and wait for a yes before coding. Run the checklist in [right-sizing.md](right-sizing.md) against the plan.

## 4. Build

- **Tests first where they pay:** domain rules, state transitions, authorization, parsing, and every bug (reproduce it in a failing test first). For UI wiring and glue, writing the test right after is fine.
- Make the smallest change that satisfies the acceptance criteria. No drive-by refactors; note them as candidate stories instead.
- Match the surrounding code's naming, structure and comment density.
- Commit in small conventional commits as you go (`feat:`, `fix:`, `test:`, `docs:`, `chore:`, `refactor:`), subject under about 50 characters, body only for the why.

## 5. Verify

Run everything the project has, and read the output:
- lint, typecheck, unit and integration tests, build
- end-to-end tests if the critical journey is affected
- screens: open the app, check each changed screen at each viewport, all states, keyboard path; take screenshots
- migrations: apply on a fresh database, and roll back if the project supports it

Paste the decisive lines (pass counts, build result) into your notes. If something fails, fix it or stop and report it; never mark Done on a red run.

## 6. Hats pass

Walk the table and update each file whose trigger fired, in the same branch:

| Trigger | Update |
|---------|--------|
| New or changed endpoint | Architecture API table (with roles) + an authorization test |
| Schema change | Migration + data model doc |
| New or changed status transition | State machine doc + a test per new row |
| New environment variable | `.env.example`, README, operations doc |
| Lasting choice between alternatives | New or superseding ADR |
| Scope changed (added, cut, deferred) | `SCOPE.md` + decision log + board |
| Security control added or changed | Threat model |
| Screen added or changed | `DESIGN.md` (screens, states) |
| AI prompt, model or provider change | AI docs and evaluation |
| CI, deploy or monitoring change | Operations doc |
| Anything a user or evaluator will notice | README if the setup or usage changed |

## 7. Review

Get an independent review against the acceptance criteria and the Definition of Done ([review.md](review.md)). Fix every finding marked must-fix; answer the rest in one line each (fixed, or why not). Re-run verification after fixes.

## 8. Done and merge

- Check every Definition of Done item. If the DoD names an owner review (a design pass, an acceptance run), get the yes first.
- Fill the story's `Tests:` line; set `Status: Done`.
- Merge locally:

```bash
git switch <integration>
git merge --no-ff feat/us-<id>-<slug> -m "feat: <story title, short> (US-<id>)"
```

- Board to Done in the same turn.
- **Do not push** unless the user says yes in this turn. Ask: "Push dev to origin?" A previous yes does not carry over.
- Partial work never merges. A story that is not whole stays on its branch, In progress, even across a sprint close.

## 9. Report

One line:

```
Done: US-<id> <title> (<test result>, <build result>). Next: US-<id> <title>. Decide: <anything the owner must choose, or none>.
```

## Bugs

Bugs found before release: a `fix/<slug>` branch from the integration branch, a failing test that reproduces the bug, the minimal fix, the same verify and review steps. Bugs in a released version: `hotfix/<slug>` from the release branch, merged into release and integration, only with the owner's yes.

## Interrupted sessions

If the session ends mid-story, add to `CHANGELOG.md`:

```
Handover (<date>): US-<id> on feat/us-<id>-<slug>: <what is done>, <what is left>, next command: <command>.
```

`wt.py status` shows the latest handover line, so the next session starts there.
