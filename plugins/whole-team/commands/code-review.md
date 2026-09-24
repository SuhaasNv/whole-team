---
description: "Independent code review of the current branch against the story's acceptance criteria and the Definition of Done"
argument-hint: "[US-id]"
---

Use the whole-team skill and follow reference/review.md. Review the current branch against the integration branch for story $ARGUMENTS (if empty, infer the story from the branch name). Use the whole-team-reviewer agent if available, otherwise a fresh subagent with the reviewer prompt; never review your own change alone. Present the verdict and the MUST FIX list, then ask whether to fix them now.
