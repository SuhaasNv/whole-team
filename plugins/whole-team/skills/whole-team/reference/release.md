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

`docs/09-uat/UAT_PLAN.md` (strict): scenarios written from the user's view, one per critical path and role, each with steps, expected result, actual result, pass or fail, date and environment. Run them yourself on the deployed environment with a browser tool if available; the owner runs the ones that need their judgement.

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
