---
type: llm
weight: 2
---

PASS if the reply says yes, it is too big, and splits it into smaller stories along workflow steps or paths (for example review and decide, feedback, compare revisions), each written as a user story.
FAIL if it splits by technical layer (backend story, frontend story), or starts project setup, intake questions or scaffolding instead of answering.
