# Independent review

The author of a change never reviews it alone. Use the `whole-team-reviewer` agent if installed; otherwise start a fresh subagent with the prompt below, filled in. The reviewer reads and runs; it does not edit.

## Reviewer prompt

```
You are an independent reviewer for story <US-id>: "<story title>".

Inputs:
- Diff: run `git diff <integration-branch>...HEAD` in <repo path>
- Acceptance criteria: <paste from USER_STORIES.md>
- Definition of Done: <repo path>/docs/05-planning/DEFINITION_OF_DONE.md
- Scope: <repo path>/SCOPE.md

Check, with evidence (file:line or command output):
1. Each acceptance criterion: met, partly met, or not met. Name the test that proves it.
2. Tests: exist at the right layer, would fail if the feature broke, cover one failure case and one authorization case where data is owned. Run them.
3. Correctness: edge cases, error handling, transactions, state transitions, off-by-one, null handling, concurrency where relevant.
4. Security: server-side authorization, input validation, secrets, injection, what is logged.
5. Right-sizing: anything not required by the acceptance criteria (extra abstractions, dependencies, config, features), and any unrelated change in the diff (copy, styling, formatting, comments, files the story does not need).
6. Docs: every triggered update in the hats table was made, and the docs describe what the code does.
7. Definition of Done: each item met or not.

Do not edit files. Do not comment on style unless it hides a bug.

Output:
VERDICT: PASS or FIX FIRST
MUST FIX
- <file:line> <problem> <smallest fix>
SHOULD FIX
- ...
NOTES
- ...
```

## After the review

- Fix every MUST FIX, re-run verification, and re-review if a fix was more than a few lines.
- For each SHOULD FIX: fix it, or write one line on why not (add it as a candidate story if it matters).
- Record the verdict in the story notes or the merge commit body.
