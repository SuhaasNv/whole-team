---
description: "Turn the agreed scope into requirements, use cases and ready user stories, and mirror them on the board"
argument-hint: "[epic or area to plan, optional]"
---

Load the whole-team skill, then follow reference/requirements-and-stories.md. Starting from SCOPE.md: personas, requirements with IDs, use cases grouped by epic (standard and strict), user stories in the exact format with testable acceptance criteria, story 000 as the walking skeleton if it does not exist, and a Definition of Ready and Done tailored to this project. Put stories not yet planned into a sprint as `Sprint: Backlog`. Run `wt.py lint`, fix every error, then mirror new or changed stories on the board (reference/board-setup.md). Finish by suggesting /whole-team:sprint to plan the next sprint.

If the project has no .whole-team.json, do the task anyway in the same formats (stories in `docs/05-planning/USER_STORIES.md`, or in the reply if there is no repository) and offer /whole-team:start in one line at the end.

Focus: $ARGUMENTS
