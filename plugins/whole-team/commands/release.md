---
description: "Prepare a release or hand-in: release lint, notes, UAT, traceability, then ask before anything leaves the machine"
argument-hint: "[version, e.g. v0.2.0]"
---

Load the whole-team skill (it holds the rules, the reference files and the wt.py script), then follow reference/release.md for $ARGUMENTS. Respect the freeze in .whole-team.json. Run `wt.py lint --release` first. Every push, pull request, tag and deploy needs the owner's yes in that turn.
