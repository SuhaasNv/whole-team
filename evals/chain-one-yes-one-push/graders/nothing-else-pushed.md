---
type: regex
target: { source: file, path: pushed.log }
pattern: 'refs/heads/(main|dev)$|us-021|refs/tags/'
flags: m
match: not_contains
---
