---
description: "Fix a bug: reproduce it in a failing test, smallest fix, review, merge"
argument-hint: "<what is broken>"
---

Load the whole-team skill. Follow the Bugs section of reference/story-loop.md and reference/branching.md: branch `fix/<slug>` from the integration branch (or `hotfix/<slug>` from the release branch for a released version, only with the owner's yes), reproduce the bug in a failing test first, make the smallest fix that turns it green without touching unrelated code, run the full verification, get an independent review, then merge locally with --no-ff. Do not push without the owner's yes.

Bug: $ARGUMENTS
