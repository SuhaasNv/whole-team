---
type: llm
weight: 2
---

PASS if the reply states what it understood, compares at least two options with their costs for this project, recommends one with a reason tied to the project (users, deployment, scope), and asks the owner to confirm before setting anything up, or records the decision as an ADR or decision-log entry after asking.
FAIL if it silently picks one and starts setting it up, or gives options without a recommendation.
