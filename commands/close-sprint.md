---
description: "Run the sprint close ritual: tests, board, CHANGELOG, scope check, retro"
argument-hint: "[sprint number]"
---

Use the whole-team skill and follow reference/sprint-close.md for sprint $ARGUMENTS (default: the current sprint in .whole-team.json). Never mark a story Done that fails its Definition of Done; move unfinished stories to the next sprint with a reason. Then increment `sprint.current` in .whole-team.json.
