# User stories

Story format: `### US-xxx: As a <persona>, I want <capability>, so that <value>.` The board mirrors this file one to one (same ID, same title). Status: Not started, In progress, In review, Done, Dropped. Priority: MUST, SHOULD, COULD, DEFERRED. Sprint: a number, or Backlog. Definition of Ready and Done: `DEFINITION_OF_DONE.md`.

## E0: Foundation

### US-000: As a developer, I want a runnable skeleton with a database, health check, CI and one deploy, so that every feature builds on a working base.
- Acceptance criteria:
  - Given a clean clone, when I follow the README, then the app starts and the health check returns 200.
  - Given the database is down, when the health check runs, then it returns 503.
  - Given a push, when CI runs, then lint, typecheck and tests run and block on failure.
- Priority: MUST · Sprint: 1 · Status: Not started
- Depends on: none · Requirements: 
- Tests: 

## Backlog: candidates

Ideas that are not stories yet (improvements noticed during a story, tech debt, requests). Refinement turns them into stories or drops them. One line each, with its source.

- 
