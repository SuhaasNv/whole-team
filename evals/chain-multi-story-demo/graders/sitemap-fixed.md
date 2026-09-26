---
type: regex
target: { source: file, path: app/site.py }
pattern: 'pages = \["home", "about"\]\s*$'
flags: m
match: not_contains
---
