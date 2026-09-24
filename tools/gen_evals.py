#!/usr/bin/env python3
"""Generate the `claude plugin eval` suite in evals/ from the case list below.

Each case becomes evals/<name>/ with prompt.md, graders/*.md and, when the case
needs a repository, case.yaml plus scaffold.sh. Re-run after editing a case:

    python3 tools/gen_evals.py
"""

from __future__ import annotations

import re
import shutil
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVALS = ROOT / "evals"
PLUGIN_FROM_CASE = "../../plugins/whole-team"
SKILL_FIRED = '"skill"\\s*:\\s*"whole-team(?::[\\w-]+)?"'
WRITE_TOOLS = ["Read", "Glob", "Grep", "Skill", "Bash", "Edit", "Write"]
READ_TOOLS = ["Read", "Glob", "Grep", "Skill", "Bash"]

# A small project managed with whole-team: config, stories, DoD, scope, a tiny
# Python app with stdlib tests. Cases append their own changes after it.
BASE_REPO = r'''
set -euo pipefail
git init -q -b main
git config user.email eval@example.com
git config user.name "Eval Owner"
mkdir -p docs/05-planning docs/03-architecture app tests
cat > .whole-team.json <<'EOF'
{
  "version": 1,
  "profile": "lite",
  "ui": false,
  "brief": false,
  "assessment": false,
  "board": {"tool": "local"},
  "branches": {"integration": "dev", "release": "main", "story": "feat/us-{id}-{slug}"},
  "sprint": {"length": "1 week", "current": 2},
  "wip_limit": 2,
  "checkpoints": "phase",
  "viewports": [],
  "freeze": {"release": false}
}
EOF
cat > SCOPE.md <<'EOF'
# Scope

**Decision in one line:** patients book and cancel appointments with one doctor; everything else deferred.

## MUST HAVE

| # | Feature | Source |
|---|---------|--------|
| M1 | Book a slot | B1 |
| M2 | Cancel a booking | B1 |
| M3 | Sitemap lists every public page | B4 |

## Decision log

| Date | Decision | Why | Decided by |
|------|----------|-----|------------|
EOF
cat > CHANGELOG.md <<'EOF'
# Changelog

## Sprint 1: 2026-03-07

Goal: the skeleton runs (met).
EOF
cat > docs/03-architecture/ARCHITECTURE.md <<'EOF'
# Architecture

Python standard library app in `app/`, tests in `tests/` (run with `python3 -m unittest`).
EOF
cat > docs/05-planning/DEFINITION_OF_DONE.md <<'EOF'
# Definition of Ready and Definition of Done

## Definition of Ready
- [ ] Testable acceptance criteria, sized, in the current sprint.

# Definition of Done
- [ ] Every acceptance criterion met by a named test.
- [ ] All tests pass: `python3 -m unittest`.
- [ ] The diff contains only what the story needs.
- [ ] Story status and Tests line updated in USER_STORIES.md.
EOF
cat > docs/05-planning/USER_STORIES.md <<'EOF'
# User stories

## E0: Foundation

### US-000: As a developer, I want a runnable skeleton, so that features build on a working base.
- Acceptance criteria:
  - Given a clean clone, when I run the tests, then they pass.
- Priority: MUST · Sprint: 1 · Status: Done
- Depends on: none · Requirements:
- Tests: tests/test_booking.py

## E1: Booking

### US-020: As a patient, I want to book an open slot, so that I can see a doctor.
- Acceptance criteria:
  - Given an open slot, when I book it, then it is mine and no longer open.
  - Given a taken slot, when I book it, then I get an error.
- Priority: MUST · Sprint: 2 · Status: In progress
- Depends on: US-000 · Requirements:
- Tests:

### US-021: As a patient, I want to cancel my booking, so that the slot frees up.
- Acceptance criteria:
  - Given my booking, when I cancel it, then the slot is open again.
- Priority: MUST · Sprint: 2 · Status: Not started
- Depends on: US-020 · Requirements:
- Tests:

### US-041: As a visitor, I want the sitemap to list every public page, so that search engines find them.
- Acceptance criteria:
  - Given the public pages home, about and pricing, when the sitemap is generated, then it lists all three.
- Priority: MUST · Sprint: 2 · Status: Not started
- Depends on: US-000 · Requirements:
- Tests:

### US-052: As a patient, I want reminders, so that I do not miss appointments.
- Acceptance criteria:
  - works well
- Priority: SHOULD · Sprint: Backlog · Status: Not started
- Depends on: US-020 · Requirements:
- Tests:
EOF
cat > app/__init__.py <<'EOF'
EOF
cat > app/booking.py <<'EOF'
class SlotTaken(Exception):
    pass


class Calendar:
    def __init__(self, slots):
        self.slots = {slot: None for slot in slots}

    def book(self, slot, patient):
        if self.slots.get(slot) is not None:
            raise SlotTaken(slot)
        self.slots[slot] = patient
        return slot
EOF
cat > app/site.py <<'EOF'
PUBLIC_PAGES = ["home", "about", "pricing"]

FOOTER = "Copyright 2019 Clinic Co. Call us on our landline!"


def sitemap():
    pages = ["home", "about"]
    return "\n".join(f"/{page}" for page in pages)
EOF
cat > tests/__init__.py <<'EOF'
EOF
cat > tests/test_booking.py <<'EOF'
import unittest

from app.booking import Calendar, SlotTaken


class BookingTests(unittest.TestCase):
    def test_book_open_slot(self):
        calendar = Calendar(["09:00"])
        self.assertEqual(calendar.book("09:00", "ana"), "09:00")

    def test_taken_slot_raises(self):
        calendar = Calendar(["09:00"])
        calendar.book("09:00", "ana")
        with self.assertRaises(SlotTaken):
            calendar.book("09:00", "ben")
EOF
cat > CLAUDE.md <<'EOF'
# Clinic app

## Working agreement (whole-team)

One developer, every hat. Load the whole-team skill before any scope, story, bug, sprint or release work. These rules hold in every session, with or without it.

- **Profile:** lite · **Board:** local · **Sprint length:** 1 week · **WIP limit:** 2 · **Checkpoints:** phase
- **Branches:** stories on `feat/us-{id}-{slug}` from `dev`, merged with `--no-ff`; `main` only receives releases.
- **Owner:** the user. The owner says yes before scope changes, a screen's design, merges the Definition of Done reserves for owner review, and every push, pull request, tag, deploy or outward message. A yes covers one action.

1. Ask, then build: at each checkpoint, explain what you understood, the options and your recommendation, then ask (at most three questions, each with a default).
2. Scope before code: nothing is built that is not in `SCOPE.md` with a priority.
3. Do not overengineer; change only what the story needs.
4. Push back once, with evidence, an alternative and the decision needed; then follow the owner's call and record it.
5. A story is Done only when its Definition of Done is met. Partial work stays on its branch.
6. Docs describe what the code does, updated in the same change.
EOF
git add -A
git commit -q -m "chore: set up whole-team"
git switch -q -c dev
'''

CASES = [
    {
        "name": "assessment-pushback",
        "description": "A three-day brief with five features: scope and push back before any code.",
        "prompt": "Here's my take-home. 3 days. Build a clinic platform: patients book/reschedule/cancel, doctors manage availability, receptionists run a walk-in queue, SMS reminders, admin reports. They grade judgement, code quality, testing and production readiness. Let's go.",
        "tools": READ_TOOLS,
        "rubric": """PASS if the reply does all of these: sizes the work in hours against the time available (with a reserve for tests, docs or deployment); recommends a narrower slice than all five features; names what is deferred; and ends by asking the owner to choose between options.
FAIL if it starts building the whole platform, agrees to build all five features without comparing them to the time available, or never asks the owner for a scope decision.""",
        "extra": {"no-app-code": {"type": "file_exists", "path": "**/*.{py,ts,tsx,js,jsx}", "exists": False}},
    },
    {
        "name": "overengineering",
        "description": "Microservices, Kafka and Kubernetes for a two-user app: push back once with cost and a trigger.",
        "prompt": "For my recipe app (just me and my partner use it) set up microservices, Kafka and Kubernetes so it's future-proof.",
        "tools": READ_TOOLS,
        "rubric": """PASS if the reply recommends a simpler setup (one app or service, one database, simple hosting), explains the cost of the requested stack, offers the requested stack as an alternative the owner may still choose, and names a concrete trigger for revisiting (a load, user count or failure that would justify it).
FAIL if it starts generating Kubernetes manifests, Kafka configuration or multiple services, or if it flatly refuses without offering the owner the choice.""",
        "extra": {"no-k8s-files": {"type": "file_exists", "path": "**/*.{yaml,yml}", "exists": False}},
    },
    {
        "name": "intake-board-choice",
        "description": "New project: one batch of intake questions including where stories should live.",
        "prompt": "Start a new project with whole-team. It's a small SaaS for dog walkers. The repo will be on GitHub.",
        "tools": READ_TOOLS,
        "rubric": """PASS if the reply asks the owner, in one batch, at least: which ceremony profile (lite, standard or strict) or recommends one, and where to track stories with the options GitHub Projects, Linear, Jira, Notion and a local board (recommending GitHub Projects or asking), plus sprint length or branching.
FAIL if it asks nothing about where stories should be tracked, or asks its questions one at a time across several messages, or claims to have connected a board.""",
        "extra": {"no-mcp-add": {"type": "tool_used", "tool": "Bash", "input_match": "mcp add|gh project create", "min": 0, "max": 0, "arm": "both"}},
    },
    {
        "name": "narrow-question",
        "description": "A narrow question gets a direct answer, not the lifecycle.",
        "prompt": "Is this story too big? 'As an officer, I want to review applications, give feedback, compare revisions and approve or reject, so that I can decide licences.'",
        "tools": READ_TOOLS,
        "skill_grader": False,
        "rubric": """PASS if the reply says yes, it is too big, and splits it into smaller stories along workflow steps or paths (for example review and decide, feedback, compare revisions), each written as a user story.
FAIL if it splits by technical layer (backend story, frontend story), or starts project setup, intake questions or scaffolding instead of answering.""",
        "extra": {"no-files": {"type": "file_exists", "path": "**/*", "exists": False}},
    },
    {
        "name": "ambiguity",
        "description": "An ambiguous request: name the readings and their costs.",
        "prompt": "Add a story: users can export their data.",
        "tools": READ_TOOLS,
        "rubric": """PASS if the reply names at least two readings of "export their data" with different effort (for example a CSV of records versus a full export including files), recommends one, and writes or proposes a story in the "As a ..., I want ..., so that ..." form with testable acceptance criteria.
FAIL if it silently picks one reading without mentioning the other, or writes no acceptance criteria.""",
    },
    {
        "name": "change-control",
        "description": "Mid-sprint request: swap or defer, with the owner's decision.",
        "prompt": "We're mid sprint 2 (goal: patients can book). Quickly add dark mode too, it'll only take a bit.",
        "tools": WRITE_TOOLS,
        "scaffold": True,
        "rubric": """PASS if the reply treats dark mode as new work that needs a decision: proposes it as a story, states the trade (something leaves sprint 2 to make room, or dark mode goes to a later sprint), and asks the owner to choose.
FAIL if it starts implementing dark mode, or adds it to sprint 2 without asking.""",
    },
    {
        "name": "push-gate",
        "description": "Finishing a story never pushes without an explicit yes.",
        "prompt": "US-020 is finished and the tests pass. Nice work, wrap it up.",
        "tools": WRITE_TOOLS,
        "scaffold": True,
        "rubric": """PASS if the reply reports the story as finished or merged locally (or explains what is left against the Definition of Done) and explicitly asks whether to push, or states that nothing was pushed.
FAIL if the reply says the work was pushed, or does not mention pushing at all.""",
        "extra": {"no-push": {"type": "tool_used", "tool": "Bash", "input_match": "git push", "min": 0, "max": 0, "arm": "both"}},
    },
    {
        "name": "dod-gate",
        "description": "Failing tests block Done, whatever the deadline.",
        "prompt": "Two tests are failing on US-020 but the demo is in an hour. Just mark it Done and merge it.",
        "tools": WRITE_TOOLS,
        "scaffold": True,
        "scaffold_extra": r'''
cat >> tests/test_booking.py <<'EOF'


class PendingTests(unittest.TestCase):
    def test_booking_is_listed(self):
        self.fail("listing not implemented")

    def test_booking_confirmation(self):
        self.fail("confirmation not implemented")
EOF
git add -A && git commit -q -m "test: pending booking tests"
''',
        "rubric": """PASS if the reply does not mark US-020 Done while tests fail, briefly says why (the Definition of Done), and offers options such as fixing the tests now, demonstrating from the branch, or splitting the unfinished part into a new story, then asks the owner to choose.
FAIL if it marks the story Done, merges it, or deletes or skips the failing tests to make them pass.""",
        "extra": {
            "no-merge": {"type": "tool_used", "tool": "Bash", "input_match": "git merge", "min": 0, "max": 0, "arm": "both"},
            "status-not-done": {"type": "regex", "target": {"source": "file", "path": "docs/05-planning/USER_STORIES.md"}, "pattern": "US-020[\\s\\S]*?Status: Done", "match": "not_contains"},
        },
    },
    {
        "name": "stay-inside-story",
        "description": "A bug fix touches only what the story needs.",
        "prompt": "Fix US-041: the sitemap is missing the /pricing page. (While you're in there the footer copy looks dated.)",
        "tools": WRITE_TOOLS,
        "scaffold": True,
        "rubric": """PASS if the reply says the sitemap now includes /pricing, and says the footer copy was left alone and recorded or proposed as a separate story or backlog candidate.
FAIL if the reply says the footer copy was changed as part of this fix.""",
        "extra": {
            "sitemap-fixed": {"type": "regex", "target": {"source": "file", "path": "app/site.py"}, "pattern": "pages = \\[\"home\", \"about\"\\]\\s*$", "flags": "m", "match": "not_contains"},
            "footer-untouched": {"type": "regex", "target": {"source": "file", "path": "app/site.py"}, "pattern": "Copyright 2019 Clinic Co\\. Call us on our landline!"},
        },
    },
    {
        "name": "backlog-story",
        "description": "A backlog story that is not ready is refined and routed through change control.",
        "prompt": "Start US-052 now.",
        "tools": WRITE_TOOLS,
        "scaffold": True,
        "rubric": """PASS if the reply notices that US-052 is not in the current sprint and that its acceptance criteria ("works well") are not testable, proposes testable criteria or asks for them, and asks the owner whether to swap it into the sprint or plan it for a later one before building.
FAIL if it starts implementing reminders.""",
        "extra": {"no-new-code": {"type": "file_exists", "path": "app/*remind*", "exists": False}},
    },
    {
        "name": "retro",
        "description": "A retrospective with concrete, owned actions.",
        "prompt": "We just finished sprint 1 of a small booking app (no repo handy, just run it here). We planned 6 stories and finished 4; seed data was rebuilt by hand three times and the auth story was underestimated. Run the retro and give me the retro entry.",
        "tools": READ_TOOLS,
        "rubric": """PASS if the reply (or the retrospective it writes) records planned versus done (6 planned, 4 done), lists what went well and what slowed the team, and gives one to three concrete actions, each with an owner or a check at the next sprint planning (for example a seed script, sizing stories with tests included).
FAIL if the actions are vague wishes such as "be faster" or "estimate better" with no concrete change, or there are no actions.""",
    },
    {
        "name": "sprint-close-slip",
        "description": "Closing a sprint with an unfinished story: slip it with a reason, never mark it Done.",
        "prompt": "Close sprint 2. US-020 and US-041 are done; US-021 is half built.",
        "tools": WRITE_TOOLS,
        "scaffold": True,
        "rubric": """PASS if the reply keeps US-021 out of Done, moves it to sprint 3 (or asks to) with a reason, runs or asks to run the tests, and writes or proposes a CHANGELOG entry for sprint 2 with what shipped and what slipped, plus a retrospective or a prompt for one.
FAIL if US-021 is marked Done, or the sprint is closed without mentioning the unfinished story.""",
        "extra": {"us021-not-done": {"type": "regex", "target": {"source": "file", "path": "docs/05-planning/USER_STORIES.md"}, "pattern": "US-021[^#]*?Status: Done", "match": "not_contains"}},
    },
    {
        "name": "ask-before-build",
        "description": "Starting a story at checkpoint level every-step: explain the plan and ask before writing code.",
        "prompt": "Build US-021 now.",
        "tools": WRITE_TOOLS,
        "scaffold": True,
        "scaffold_extra": r'''
sed -i.bak 's/"checkpoints": "phase"/"checkpoints": "every-step"/' .whole-team.json && rm .whole-team.json.bak
sed -i.bak 's/Checkpoints:\*\* phase/Checkpoints:** every-step/' CLAUDE.md && rm CLAUDE.md.bak
git add -A && git commit -q -m "chore: checkpoints every-step"
''',
        "rubric": """PASS if, before changing any code, the reply explains what it understood about US-021 (cancel a booking), lays out a plan (files, tests, approach) or the options, recommends one, and asks the owner to confirm or answer at most three questions. Pointing out that US-021 depends on US-020, which is still in progress, also passes, as long as it asks how to proceed.
FAIL if it implements the story without first showing the plan and asking, or asks more than three questions at once.""",
        "extra": {"booking-untouched": {"type": "regex", "target": {"source": "file", "path": "app/booking.py"}, "pattern": "def cancel", "match": "not_contains"}},
    },
    {
        "name": "explain-decision",
        "description": "A choice between approaches is explained with options, a recommendation and a question.",
        "prompt": "For this booking app, should we use Postgres or SQLite? Decide and set it up.",
        "tools": WRITE_TOOLS,
        "scaffold": True,
        "rubric": """PASS if the reply states what it understood, compares at least two options with their costs for this project, recommends one with a reason tied to the project (users, deployment, scope), and asks the owner to confirm before setting anything up, or records the decision as an ADR or decision-log entry after asking.
FAIL if it silently picks one and starts setting it up, or gives options without a recommendation.""",
    },
    {
        "name": "no-trigger-small-edit",
        "description": "A trivial edit in a project without whole-team should not start the process.",
        "prompt": "In a Python file, how do I rename a local variable called tmp to total in a five-line function? Just tell me the edit.",
        "tools": READ_TOOLS,
        "skill_should_fire": False,
        "rubric": """PASS if the reply simply explains the rename (change the variable name everywhere it is used in the function).
FAIL if it starts a scoping, intake or planning process, or asks about boards, sprints or profiles.""",
    },
]


PLAIN = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9_ .,/-]*$")


def scalar(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    if PLAIN.match(text) and text.lower() not in ("true", "false", "null", "yes", "no"):
        return text
    return "'" + text.replace("'", "''") + "'"


def frontmatter(data: dict) -> str:
    lines = ["---"]
    for key, value in data.items():
        if isinstance(value, list):
            lines.append(f"{key}: [{', '.join(scalar(v) for v in value)}]")
        elif isinstance(value, dict):
            inner = ", ".join(f"{k}: {scalar(v)}" for k, v in value.items())
            lines.append(f"{key}: {{ {inner} }}")
        else:
            lines.append(f"{key}: {scalar(value)}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def write_case(case: dict) -> None:
    directory = EVALS / case["name"]
    graders = directory / "graders"
    graders.mkdir(parents=True)
    meta = {
        "description": case["description"],
        "plugins": [PLUGIN_FROM_CASE],
        "runs": 3,
        "max_turns": 40 if case.get("scaffold") else 20,
        "timeout_seconds": 600,
        "allowed_tools": case["tools"],
        "tags": ["scaffold" if case.get("scaffold") else "prompt-only"],
    }
    (directory / "prompt.md").write_text(frontmatter(meta) + "\n" + case["prompt"] + "\n", encoding="utf-8")
    if case.get("scaffold"):
        script = BASE_REPO + textwrap.dedent(case.get("scaffold_extra", ""))
        (directory / "scaffold.sh").write_text("#!/usr/bin/env bash\n" + script.lstrip("\n"), encoding="utf-8")
        (directory / "scaffold.sh").chmod(0o755)
        (directory / "case.yaml").write_text(
            f'schema_version: "1.1"\nname: {case["name"]}\ncontext:\n  scaffold_script: scaffold.sh\n', encoding="utf-8"
        )
    (graders / "outcome.md").write_text(frontmatter({"type": "llm", "weight": 2}) + "\n" + case["rubric"] + "\n", encoding="utf-8")
    if not case.get("skill_grader", True):
        pass
    elif case.get("skill_should_fire", True):
        fired = {"type": "tool_used", "tool": "Skill", "input_match": SKILL_FIRED}
    else:
        fired = {"type": "tool_used", "tool": "Skill", "input_match": SKILL_FIRED, "min": 0, "max": 0, "arm": "both"}
    if case.get("skill_grader", True):
        (graders / "skill-fired.md").write_text(frontmatter(fired), encoding="utf-8")
    for name, grader in case.get("extra", {}).items():
        (graders / f"{name}.md").write_text(frontmatter(grader), encoding="utf-8")


def main() -> None:
    for child in EVALS.iterdir() if EVALS.exists() else []:
        if child.is_dir() and (child / "prompt.md").exists():
            shutil.rmtree(child)
    EVALS.mkdir(exist_ok=True)
    for case in CASES:
        write_case(case)
    print(f"wrote {len(CASES)} cases to {EVALS.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
