# Release, submission, hand-in

Everything in this file leaves the machine or changes what users see. Every push, pull request, tag, deploy and message needs the owner's yes in that turn.

## Freeze

The owner can freeze the release branch (for example while an assessor reviews a submission). While `.whole-team.json` has `"freeze": {"release": true}`, do not open pull requests into it, tag, deploy to production or hotfix. Work continues on the integration branch. A request that would touch the release branch is answered with the freeze, not carried out, until the owner lifts it in so many words.

## Release checklist

```
Release vX.Y.Z
- [ ] wt.py lint --release: no errors (every MUST Done, nothing In progress, no template placeholders)
- [ ] Full test suite and e2e green; CI green on the integration branch
- [ ] Version bumped everywhere the project stores it
- [ ] RELEASE_NOTES.md entry in the users' words: new, improved, known limitations
- [ ] CHANGELOG.md milestone entry
- [ ] UAT scenarios run on the deployed pre-release environment; results recorded with date
- [ ] Traceability re-checked: every brief item or requirement maps to a story and a test, or to a DEFERRED row
- [ ] Docs index truthful: every document listed exists and describes what exists
- [ ] Rollback plan written: previous version, how to redeploy it, migration safety
- [ ] Owner yes → pull request integration → release; merge when green
- [ ] Owner yes → tag vX.Y.Z on the merge commit; deploy; health check green
- [ ] Smoke test the production URL: login per role, the critical journey
```

## Versioning

Semantic versioning. Before 1.0.0, a minor bump per release is fine. Show the version in the app (footer or about screen) so a bug report names it.

## UAT

`docs/09-uat/UAT_PLAN.md` (strict; a short list in `TEST_STRATEGY.md` otherwise): scenarios written from the user's view, one per critical path and role, each with steps, expected result, actual result, pass or fail, date, environment and evidence.

**Run them in a real browser, and record them.** Recommend the owner's best option at the first UAT, and explain why:

| Tool | Use it for | Set up |
|------|------------|--------|
| **Claude in Chrome** (the agent drives the owner's own browser) | Walking each scenario like a user would, including logged-in flows, and recording a GIF of each run as evidence | Install the extension from claude.com/claude-in-chrome; in Claude Code run `/chrome` (or start with `claude --chrome`). Needs a Claude Pro, Max, Team or Enterprise login |
| **Playwright** (scripted, repeatable) | Turning each passed scenario into an end-to-end test that runs in CI on every change | Claude Code: `/plugin install playwright@claude-plugins-official` for the browser tools; in the project: `npm init playwright@latest` (or `pip install pytest-playwright`) for the test suite |

How a UAT run goes:
1. Show the owner the scenarios you will run and on which environment; ask for a yes (a run can create data on that environment).
2. For each scenario: drive the browser step by step, compare with the expected result, save the evidence (a GIF or screenshots named `UAT-03-<slug>`), and fill the row: actual, pass or fail, date, environment.
3. A failure becomes a bug (`fix/` branch, failing test first). Never mark a failed scenario passed.
4. For each passed scenario that is not yet automated, write or extend a Playwright test so the next release checks it without a human. Keep the scripts in the repository (`e2e/` or `tests/e2e/`) and run them in CI.
5. Scenarios that need human judgement (copy, look and feel, legal wording) go to the owner with the evidence attached.

Never enter real passwords, payment details or personal data during UAT: use the seeded demo accounts.

## Production readiness (strict)

A short honest review before the first production release: security controls in place, monitoring and alerting, backups, error handling, performance under expected load, known limitations. Anything missing is written down with its risk; do not hide gaps.

## Assessment or client hand-in

```
Hand-in
- [ ] README: what it is, live URL, demo accounts per role, setup from a clean clone, environment variables, how to run tests, architecture summary, scope decision (link SCOPE.md), AI usage, what I would do next
- [ ] Clean-clone test: clone into a temp directory, follow the README exactly, app runs and tests pass
- [ ] SCOPE.md, TRACEABILITY.md, AI_USAGE.md current
- [ ] Deployed URL works in a private window; seeded demo data present
- [ ] No secrets in history (secret scan), no debug logs, no dead code
- [ ] Re-read the brief line by line against TRACEABILITY.md one last time
- [ ] Owner yes → push, tag, submit
```

"What I would do next" is a strength, not an admission: list the deferred items with what each would need, in priority order.
