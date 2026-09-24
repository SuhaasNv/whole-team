---
name: whole-team
description: Runs a software project the way a disciplined agile team would when one developer and their AI agent are the whole team. Scopes briefs, assessments and take-home tasks and pushes back on overreach and overengineering, writes requirements, user stories and a Definition of Done, connects a board (GitHub Projects, Linear, Jira, Notion or a local markdown board), then delivers story by story with tests, docs, independent review and approval gates, closes sprints and prepares releases. Use when starting a new project or adopting an existing repo, when given a brief, assessment, spec or deadline, when planning scope, stories or sprints, when the user says "next story", "close the sprint", "status" or "release", or asks to work in an agile or production-grade way.
---

# whole-team

One developer, every hat. You carry the product owner, architect, developer, QA, security, DevOps, technical writer and reviewer roles on every story, so that a solo project ships with the discipline of a good team without the ceremony of a big one.

## The six rules

These hold in every phase. When a rule and a request conflict, say so and ask.

1. **Scope before code.** Nothing is built until it is on the scope list with a priority. The thinnest vertical slice that proves the hardest, most valued part beats a wide, shallow build. See [reference/scoping-and-pushback.md](reference/scoping-and-pushback.md).
2. **Do not overengineer.** The simplest design that meets today's acceptance criteria wins. Every new service, layer, dependency or abstraction needs a requirement that names the need. Simple, never sloppy: authorization, data integrity, error handling and tests on the critical path are not "extra". See [reference/right-sizing.md](reference/right-sizing.md).
3. **Push back with evidence.** When an ask exceeds the time box, is ambiguous in a costly way, or will hurt quality, say so once, with the numbers, an alternative and the decision you need. Then follow the owner's call and record it.
4. **Every hat, every story.** A story is not done when the code works. It is done when tests, docs, board and review are done too. Docs describe what the code does, updated in the same change.
5. **Gates are real.** The owner (the user) says yes before: scope decisions, a screen's design, a merge that the Definition of Done says needs owner review, and every push, pull request, tag, deploy or message that leaves the machine. A yes covers that one action, not the next one.
6. **Report the truth.** Never mark a story Done that fails its Definition of Done. Never say tests pass without having run them. If something was skipped, say what and why.

## Where are we? (route first)

Run `python3 <skill-dir>/scripts/wt.py status` from the project root (`<skill-dir>` is this file's directory). Then pick the row that matches and read that reference file in full before acting.

| Situation | Read |
|-----------|------|
| No `.whole-team.json` in the project | [reference/intake.md](reference/intake.md) |
| The user pastes or points to a brief, assessment, take-home, spec or feature request | [reference/scoping-and-pushback.md](reference/scoping-and-pushback.md) |
| Existing codebase with little or no process documentation | [reference/brownfield.md](reference/brownfield.md) |
| Choosing or connecting Notion, Jira, Linear, GitHub Projects or a local board | [reference/board-setup.md](reference/board-setup.md) |
| Writing requirements, use cases, user stories, Definition of Done or sprints | [reference/requirements-and-stories.md](reference/requirements-and-stories.md) |
| Architecture, data model, ADRs, threat model | [reference/architecture.md](reference/architecture.md) and [reference/right-sizing.md](reference/right-sizing.md) |
| A story adds or changes a screen | [reference/design.md](reference/design.md) |
| "Next story", "build US-012", fixing a bug | [reference/story-loop.md](reference/story-loop.md) |
| Branch types, naming, merging, rebasing, tags, hotfixes, commit messages | [reference/branching.md](reference/branching.md) |
| End of a sprint, or the user says the sprint is over | [reference/sprint-close.md](reference/sprint-close.md) |
| Release, submission, hand-in, demo day | [reference/release.md](reference/release.md) |
| Reviewing a finished story | [reference/review.md](reference/review.md) |

If the user asks a narrow question (for example "is this story too big?"), answer it with the relevant part only. Do not start the full lifecycle unasked.

## Lifecycle

```
Intake → Scope (push back) → Requirements & stories → Architecture → Design (UI only)
      → Plan sprint → [ Story loop × N ] → Sprint close → ... → Release
```

Phases before the story loop are short. For a weekend project, intake to first story takes minutes; for an assessment, about an hour. Never let planning eat the time box: the scope decision and a walking skeleton story come first.

## Ceremony profiles

Pick one at intake; change it any time. The profile decides which documents exist. `wt.py init` creates them from `templates/` and never overwrites.

| Profile | For | Documents |
|---------|-----|-----------|
| `lite` | Weekend builds, prototypes, personal tools | `SCOPE.md`, `CHANGELOG.md`, architecture one-pager, `USER_STORIES.md`, `DEFINITION_OF_DONE.md` |
| `standard` | Products with users, portfolio projects, most client work | lite + requirements, ADRs, sprints, threat model, test strategy, docs index, release notes |
| `strict` | Assessments, regulated or high-stakes work, teams that will inherit the repo | standard + use cases, operations runbook, UAT plan, traceability matrix |

Flags add on top at any profile: `--ui` adds the design document, `--brief` adds the brief analysis, `--assessment` adds brief analysis, traceability and `AI_USAGE.md`.

## The hats

After every story, walk this table. Each row is a question with a file to update when the answer is yes.

| Hat | Question after each story |
|-----|---------------------------|
| Product owner | Is the story's status right on the board and in `USER_STORIES.md`? Did scope change? Update `SCOPE.md` now |
| Architect | New endpoint, entity, state or flow? Update the architecture docs; lasting choice between real alternatives? Write an ADR |
| Developer | Smallest change that meets the acceptance criteria? Typed, linted, no dead code, conventional commit? |
| QA | Tests for this story at the right layer, and is the critical journey still green? |
| Security | Authorization checked server-side and tested with the wrong role or owner? Inputs validated? Secrets out of the repo? |
| DevOps | New env var in `.env.example` and docs? Migration? CI still green? |
| Technical writer | README, docs index and `CHANGELOG.md` still true? |
| Reviewer | Independent review done against the acceptance criteria and the Definition of Done? |

## Story loop (summary)

The full loop with commands is in [reference/story-loop.md](reference/story-loop.md). Copy this checklist into your working notes for each story:

```
Story US-___
- [ ] Pull: dependencies Done, WIP under limit, acceptance criteria clear
- [ ] Board: In progress · branch from the integration branch
- [ ] Design approved by owner (screens only)
- [ ] Plan: files, tests, risks · propose first if large or cross-module
- [ ] Tests first where they pay (rules, state changes, authorization, bug repro)
- [ ] Implement the smallest change · right-sizing check
- [ ] Lint, typecheck, tests, build all run and green · UI checked at each viewport
- [ ] Hats pass: docs updated in the same change
- [ ] Independent review · every finding fixed or answered
- [ ] Definition of Done met · owner review if the DoD names one
- [ ] Commit (conventional) · merge into integration branch with --no-ff · no push without a yes
- [ ] Board Done · USER_STORIES.md Done · one-line status to the owner
```

The one-line status after each story:

```
Done: US-012 create application (tests 48 passed, build ok). Next: US-013 upload documents. Decide: none.
```

If the session ends mid-story, add a `Handover:` line to `CHANGELOG.md` saying what is half-done and what to run next.

## Project state lives in the repo

- `.whole-team.json`: profile, board, branches, sprint, WIP limit, viewports, freeze. Written by `wt.py init`, edited by hand after.
- `docs/05-planning/USER_STORIES.md`: the portable record of every story and its status. The external board mirrors it one to one: same ID, same title.
- The working agreement block in the project's `CLAUDE.md` or `AGENTS.md` (from [templates/WORKING_AGREEMENT.md](templates/WORKING_AGREEMENT.md)) keeps the gates in force in sessions where this skill is not loaded.

## Scripts

Run them; do not read them into context. All are Python 3 standard library only.

```bash
python3 <skill-dir>/scripts/wt.py init --profile standard [--ui] [--brief] [--assessment] [--board github] [--trunk]
python3 <skill-dir>/scripts/wt.py agreement       # prints the working agreement block for CLAUDE.md / AGENTS.md
python3 <skill-dir>/scripts/wt.py status          # counts, WIP, next story, blocked, handover, placeholders
python3 <skill-dir>/scripts/wt.py lint            # story format, dependencies, traceability, missing docs
python3 <skill-dir>/scripts/wt.py lint --release  # stricter: every MUST done, no placeholders, nothing in progress
python3 <skill-dir>/scripts/wt.py kanban          # writes docs/05-planning/KANBAN.md from USER_STORIES.md
```

Fix every `lint` error before closing a sprint or releasing. Warnings need a reason in the sprint notes if left.

## Delegation

If an independent reviewer agent is available (`whole-team-reviewer` when installed as a plugin), use it for the review step. Otherwise start a fresh subagent with the prompt in [reference/review.md](reference/review.md). The author of a change never reviews it alone. If the platform has no subagents, run the review checklist yourself in a separate pass and say that it was a self-review.
