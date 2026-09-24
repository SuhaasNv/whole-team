---
description: "Choose or connect a board (GitHub Projects, Linear, Jira, Notion or local) and sync it with USER_STORIES.md"
argument-hint: "[github | linear | jira | notion | local]"
---

Load the whole-team skill, then follow reference/board-setup.md. If no board is chosen yet, recommend one with a one-line reason and ask. To connect, show the exact command and let the owner run it or approve it; never handle tokens. Once connected, record the identifiers in .whole-team.json and sync: every story in docs/05-planning/USER_STORIES.md exists on the board with the same ID, title, status, priority and sprint. Report what you created or changed.

Board: $ARGUMENTS
