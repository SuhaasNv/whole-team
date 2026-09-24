# Definition of Ready and Definition of Done

## Definition of Ready

A story enters a sprint only when:
- [ ] It reads `As a <persona>, I want <capability>, so that <value>`, and the value is visible to a user or tester.
- [ ] Every acceptance criterion is testable, with at least one failure case and, where data is owned, one authorization case.
- [ ] It is sized and fits in one sprint (split it otherwise).
- [ ] Its dependencies are Done or planned earlier in the same sprint.
- [ ] Screens: the design is approved, or approving it is the first task.
- [ ] Open questions are answered or recorded as assumptions in `SCOPE.md`.

# Definition of Done

A story is Done only when every applicable item is true. "Works on my machine" is the start, not the end. Tailor this list to the project at intake, then treat it as a contract.

## Functional
- [ ] Every acceptance criterion is demonstrably met, each by a named test or a recorded manual check.
- [ ] The diff contains only what the story needs (no unrelated copy, styling, formatting or files).
- [ ] The critical journey still works end to end.

## Correctness and safety
- [ ] Input validated on the server (and on the client for forms).
- [ ] Authorization enforced on the server for every new or changed endpoint; tested with the wrong role and the wrong owner.
- [ ] Errors use the project's error shape with the right status code; no stack traces in responses.
- [ ] Multi-step writes are transactional.

## Tests
- [ ] Unit tests for new rules and state transitions.
- [ ] Integration tests for new endpoints against a real database.
- [ ] End-to-end test updated if the critical journey changed.
- [ ] Everything green locally and in CI.

## Code quality
- [ ] Typed; linter and type checker clean.
- [ ] Module boundaries respected.
- [ ] No debug logging, commented-out code or unused files.
- [ ] Nothing beyond the acceptance criteria (right-sizing checklist passed).
- [ ] Independent review done; every must-fix resolved.

## UI (stories with a screen)
- [ ] Design approved by the owner before code.
- [ ] Loading, empty, error and success states.
- [ ] Checked at every target viewport with no horizontal scroll.
- [ ] Keyboard reachable, visible focus, labelled inputs, colour never the only signal.

## Security
- [ ] No secrets committed; `.env.example` updated for new variables.
- [ ] Logs carry identifiers, not personal data or secrets.

## Docs and board
- [ ] Every triggered update from the hats table made in the same branch.
- [ ] Story status and `Tests:` line filled in `USER_STORIES.md`; board updated.

## DoD debt (brownfield only)

Items the codebase cannot meet yet, each with a story or an accepted reason.
