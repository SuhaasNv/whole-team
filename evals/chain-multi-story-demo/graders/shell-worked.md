---
type: regex
target: { source: file, path: '.git/logs/HEAD' }
pattern: '\t(commit|commit \(merge\)|merge [^:]+): (?!chore: set up whole-team|chore: release script and checklist|test: open slots listing)'
---
