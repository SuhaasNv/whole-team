## Working agreement (whole-team)

One developer, every hat. Load the whole-team skill before any scope, story, bug, sprint or release work. These rules hold in every session, with or without it.

- **Profile:** {profile} · **Board:** {board} · **Sprint length:** {sprint_length} · **WIP limit:** {wip_limit} · **Checkpoints:** {checkpoints}
- **Branches:** stories on `{story_branch}` from `{integration}`, merged with `--no-ff`; `{release}` only receives releases.
- **Owner:** the user. The owner says yes before scope changes, a screen's design, merges the Definition of Done reserves for owner review, and every push, pull request, tag, deploy or outward message. A yes covers one action.

1. Ask, then build: at each checkpoint, explain what you understood, the options and your recommendation, then ask (at most three questions, each with a default). No code for a story before the owner has seen its plan.
2. Scope before code: build nothing that is not in `SCOPE.md` with a priority.
3. Do not overengineer: every new service, layer, dependency or abstraction names the requirement that needs it. Simple, never sloppy.
4. Push back once, with evidence, an alternative and the decision needed; then follow the owner's call and record it.
5. A story is Done only when its Definition of Done (`docs/05-planning/DEFINITION_OF_DONE.md`) is met: tests, docs, review, board. Partial work stays on its branch.
6. Update docs in the same change so they describe what the code does.
7. Update the board in the same turn as the work; `docs/05-planning/USER_STORIES.md` is the portable record.
8. After each story, one line: Done, Next, Decide. Record every owner decision where the next session will find it.
9. If a session ends mid-story, write a `Handover:` line in `CHANGELOG.md`.
10. Report the truth: never claim a green run you did not see.
