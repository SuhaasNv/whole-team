# Eval results

Each run: a fresh agent with the skill loaded, in a scratch repository, given the case's query. Graded against every `expected_behavior` line.

| Date | Skill version | Model | Cases | Passed | Notes |
|------|---------------|-------|-------|--------|-------|
| 2026-09-24 | 0.1.0 (pre-release) | Claude Sonnet 5 | assessment-pushback, overengineering, intake-board-choice, narrow-question | 4/4 | Found five points of friction, all fixed before release: routing precedence when two rows match, a build request before setup, the first commit on `main`, the sprint length unit, lint noise from template example rows |
