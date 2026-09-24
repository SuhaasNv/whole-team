---
type: regex
target: { source: file, path: docs/05-planning/USER_STORIES.md }
pattern: 'US-021[^#]*?Status: Done'
match: not_contains
---
