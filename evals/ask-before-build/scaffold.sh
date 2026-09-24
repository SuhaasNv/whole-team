#!/usr/bin/env bash
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

sed -i.bak 's/"checkpoints": "phase"/"checkpoints": "every-step"/' .whole-team.json && rm .whole-team.json.bak
sed -i.bak 's/Checkpoints:\*\* phase/Checkpoints:** every-step/' CLAUDE.md && rm CLAUDE.md.bak
git add -A && git commit -q -m "chore: checkpoints every-step"
