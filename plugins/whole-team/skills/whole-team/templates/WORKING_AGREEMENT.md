## Working agreement (whole-team)

One developer, every hat. Load the whole-team skill before any scope, story, bug, sprint or release work. These rules hold in every session, with or without it.

- **Profile:** {profile} · **Board:** {board} · **Sprint length:** {sprint_length} · **WIP limit:** {wip_limit}
- **Branches:** stories on `{story_branch}` from `{integration}`, merged with `--no-ff`; `{release}` only receives releases.
- **Owner:** the user. The owner says yes before scope changes, a screen's design, merges the Definition of Done reserves for owner review, and every push, pull request, tag, deploy or outward message. A yes covers one action.

1. Scope before code: nothing is built that is not in `SCOPE.md` with a priority.
2. Do not overengineer: every new service, layer, dependency or abstraction names the requirement that needs it. Simple, never sloppy.
3. Push back once, with evidence, an alternative and the decision needed; then follow the owner's call and record it.
4. A story is Done only when its Definition of Done (`docs/05-planning/DEFINITION_OF_DONE.md`) is met: tests, docs, review, board. Partial work stays on its branch.
5. Docs describe what the code does, updated in the same change.
6. Update the board in the same turn as the work; `docs/05-planning/USER_STORIES.md` is the portable record.
7. After each story, one line: Done, Next, Decide.
8. If a session ends mid-story, write a `Handover:` line in `CHANGELOG.md`.
9. Report the truth: never claim a green run you did not see.
