---
type: llm
weight: 2
---

PASS if the reply asks the owner, in one batch, at least: which ceremony profile (lite, standard or strict) or recommends one, and where to track stories with the options GitHub Projects, Linear, Jira, Notion and a local board (recommending GitHub Projects or asking), plus sprint length or branching.
FAIL if it asks nothing about where stories should be tracked, or asks its questions one at a time across several messages, or claims to have connected a board.
