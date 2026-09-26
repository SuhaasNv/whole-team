---
description: 'The owner approves one push up front: exactly that push happens, later work stays local.'
plugins: ['../../plugins/whole-team']
runs: 3
max_turns: 120
timeout_seconds: 1500
allowed_tools: [Read, Glob, Grep, Skill, Bash, Edit, Write]
tags: [scaffold, chain]
---

Fix US-041 on its story branch, and once the tests pass push that branch to origin. Then start on US-021.
