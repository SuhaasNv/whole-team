---
type: regex
target: { source: file, path: docs/05-planning/USER_STORIES.md }
pattern: 'US-020[\s\S]*?Status: Done'
match: not_contains
---
