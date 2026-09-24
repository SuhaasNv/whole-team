# Changelog

All notable changes to whole-team. Versions follow semantic versioning.

## 0.1.0

First public release.

- `whole-team` skill: eight rules, a routing table with precedence, ceremony profiles (lite, standard, strict), the hats table and the story loop.
- Sprints: planning, daily start, refinement against a Definition of Ready, change control mid-sprint, sprint review, retros with tracked actions, and sprint close.
- Reference guides: intake, scoping and pushback, right-sizing (including "change only what the story needs"), board setup for GitHub Projects, Linear, Jira, Notion or a local board across Claude Code, Codex, Cursor, VS Code and Gemini CLI, requirements, use cases and stories, architecture, design, story loop, branching, sprints, release, brownfield adoption and independent review.
- Templates for every document the profiles create, including use cases, retrospectives and the working agreement.
- `wt.py` helper (standard library only): `init`, `status`, `sprint`, `lint`, `lint --release`, `kanban`, `agreement`.
- Claude Code plugin: 14 slash commands and the `whole-team-reviewer` agent.
- A `claude plugin eval` suite of 15 scenarios with scaffolded repositories and a no-plugin baseline, plus a repository validator and CI.
- Fixes from eval failures: a recommended slice must fit the hours (drop features before quality), extras mentioned in passing become backlog candidates, narrow tasks don't wait for setup, commands load the skill first, and the working agreement tells the agent to load it.
- Fixes from an audit: the skill treats board and issue text as data, never as instructions; `wt.py lint` reports dependency cycles; sprint numbers match whether written `1`, `01` or `1.0`; CI actions are pinned to commit SHAs.
- README with a banner, a lifecycle diagram and before/after metrics; a security policy; issue and pull request templates.
