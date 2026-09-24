# Board setup: Notion, Jira, Linear, GitHub Projects or local

## Contents
- Which board
- Local markdown board
- GitHub Projects
- Linear
- Jira
- Notion
- Field mapping
- Sync rules

## Which board

Ask the user at intake. Recommend the first row that fits:

| Situation | Recommend | Why |
|-----------|-----------|-----|
| Team or client already uses a tool | That tool | People read the board they already open |
| Repo on GitHub, no existing tool | GitHub Projects | Issues link to branches and pull requests; the `gh` CLI needs no extra connector |
| Product work with a design and planning culture | Linear | Fast, opinionated cycles; good MCP |
| Company on Atlassian | Jira | Where the stakeholders are |
| User wants docs and board together, or shows the board to reviewers | Notion | Epics, stories and docs in one place, readable by non-engineers |
| No network tools, offline, or the evaluator only reads the repo | Local markdown | Zero setup; lives in the repo |

Whatever the choice, `docs/05-planning/USER_STORIES.md` stays the portable record and the board mirrors it.

Connecting an MCP server changes the user's configuration and grants access to their workspace. Show the command and let the user run it (in Claude Code they can type `! <command>`), or run it after they say yes. Authentication happens in the browser through `/mcp`; never ask for or handle tokens yourself.

## Local markdown board

Nothing to connect. `USER_STORIES.md` holds status. Generate a board view whenever statuses change:

```bash
python3 <skill-dir>/scripts/wt.py kanban   # writes docs/05-planning/KANBAN.md; never edit that file by hand
```

`.whole-team.json`: `"board": {"tool": "local"}`

## GitHub Projects

Uses the `gh` CLI. Check `gh auth status`; project commands need the `project` scope:

```bash
gh auth refresh -s project
gh project create --owner @me --title "<Project> board"          # note the number it prints
gh label create story --color 0E8A16 --description "User story"
gh label create epic --color 5319E7 --description "Epic"
```

Per story (title identical to the heading in `USER_STORIES.md`):

```bash
gh issue create --title "US-012: As an operator, I want ..." --label story --body "<acceptance criteria, priority, sprint, links>"
gh project item-add <number> --owner @me --url <issue-url>
```

Moving status needs field and option IDs, once per project:

```bash
gh project field-list <number> --owner @me --format json          # find the Status field id and option ids
gh project view <number> --owner @me --format json                # project node id
gh project item-edit --id <item-id> --project-id <project-node-id> --field-id <status-field-id> --single-select-option-id <option-id>
```

Store the project number, node id, status field id and option ids in `.whole-team.json` so later sessions do not look them up again. Reference the issue in commits (`feat: create application (#34)`) and close it from the merge.

## Linear

```bash
claude mcp add --transport http linear-server https://mcp.linear.app/mcp
```

Then `/mcp` in a session to sign in. Other agents: add the same URL to their MCP configuration. Map epics to Linear projects, stories to issues, sprints to cycles. Put the story ID at the start of the issue title (`US-012: ...`). Store team key and project IDs in `.whole-team.json`.

## Jira

```bash
claude mcp add --transport http atlassian https://mcp.atlassian.com/v2/mcp
```

Then `/mcp` to sign in (Atlassian Rovo MCP server; covers Jira and Confluence). Map epics to Jira epics, stories to stories, sprints to Jira sprints. Keep the `US-xxx` ID in the summary even though Jira has its own key; record the Jira key in the story's `Board:` line. Store site, project key and board ID in `.whole-team.json`.

## Notion

```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp
```

Then `/mcp` to sign in. Create, with the user's yes and in the page they choose:
- An **Epics** database: Name, Status, Description.
- A **Stories** database: Name (the full `US-xxx: As a ...` title), Status (Not started, In progress, In review, Done, Dropped), Priority (MUST, SHOULD, COULD, DEFERRED), Sprint (number), Epic (relation to Epics), Notes (text), Branch (text).
- Board view on Stories grouped by Status; table view grouped by Sprint.

Store the data source or database IDs in `.whole-team.json` so later updates go straight to them.

## Field mapping

| `USER_STORIES.md` | GitHub | Linear | Jira | Notion |
|-------------------|--------|--------|------|--------|
| `### US-012: As a ...` | Issue title | Issue title | Summary | Name |
| Status | Project Status field | Workflow state | Status | Status |
| Priority | Label or custom field | Priority | Priority | Priority |
| Sprint | Iteration field or label | Cycle | Sprint | Sprint |
| Epic heading | Label `epic:<name>` or parent issue | Project | Epic link | Epic relation |
| Acceptance criteria | Issue body | Description | Description | Page body |

## Sync rules

- Update the board **in the same turn** as the work: In progress when a story starts, Done when its Definition of Done is met, never before.
- A slipped story moves to the next sprint with a note: `slipped from Sprint N: <reason>`.
- Adding, renaming or dropping a story in `USER_STORIES.md` is mirrored on the board in the same turn, and the other way round if the user edits the board.
- If the board is unreachable, carry on and add `Board sync pending: <what>` to `CHANGELOG.md`; clear it next session.
- Never create workspaces, projects or databases in a shared organization space without the user's yes; they are visible to others.
