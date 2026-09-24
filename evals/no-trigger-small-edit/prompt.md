---
description: A trivial edit in a project without whole-team should not start the process.
plugins: ['../../plugins/whole-team']
runs: 3
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Bash]
tags: [prompt-only]
---

In a Python file, how do I rename a local variable called tmp to total in a five-line function? Just tell me the edit.
