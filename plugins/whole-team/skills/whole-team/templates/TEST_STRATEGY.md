# Test strategy

Tests aim at risk, not at a coverage number.

| Layer | Covers | Tool | Command | Blocks CI |
|-------|--------|------|---------|-----------|
| Unit | Domain rules, state transitions, parsing | TODO(whole-team) | | yes |
| Integration | Endpoints against a real database, authorization | TODO(whole-team) | | yes |
| End to end | The critical journey, as Playwright tests | TODO(whole-team) Playwright | | yes |
| UAT | Scenarios from the user's view, before each release | Claude in Chrome (recorded) or Playwright | | release gate |

## Critical journey

TODO(whole-team): the one path that must never break, step by step.

## Test data

TODO(whole-team): seed script, fixtures, how to reset.
