"""Tests for wt.py. Run: python3 -m unittest discover -s skills/whole-team/scripts"""

from __future__ import annotations

import contextlib
import io
import json
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import wt  # noqa: E402

STORIES = """# User stories

## E0: Foundation

### US-000: As a developer, I want a runnable skeleton, so that features build on a working base.
- Acceptance criteria:
  - Given a clean clone, when I follow the README, then the app starts.
- Priority: MUST · Sprint: 1 · Status: Done
- Depends on: none · Requirements: FR-001
- Tests: tests/test_health.py

## E1: Submission

### US-001: As an operator, I want to create an application, so that I can apply.
- Acceptance criteria:
  - Given I am logged in, when I click New, then a draft exists.
- Priority: MUST · Sprint: 1 · Status: Not started
- Depends on: US-000 · Requirements: FR-002
- Tests:

### US-002: As an operator, I want to upload documents, so that the officer can check them.
- Acceptance criteria:
  - Given a draft, when I upload a PDF, then it is listed.
- Priority: SHOULD · Sprint: 2 · Status: Not started
- Depends on: US-001 · Requirements: FR-002
- Tests:
"""

REQUIREMENTS = """# Requirements

| ID | Requirement | Source | Priority |
|----|-------------|--------|----------|
| FR-001 | Skeleton runs | B1 | MUST |
| FR-002 | Create application | B2 | MUST |
| FR-003 | Export data | B3 | COULD |
| FR-004 | Old idea, Dropped: out of scope | B4 | COULD |
"""


def run(argv: list) -> tuple:
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = wt.main(argv)
    return code, out.getvalue()


class ParseTests(unittest.TestCase):
    def test_parses_fields(self) -> None:
        stories = wt.parse_stories(STORIES)
        self.assertEqual([s.id for s in stories], ["US-000", "US-001", "US-002"])
        first = stories[0]
        self.assertEqual(first.priority, "MUST")
        self.assertEqual(first.sprint, "1")
        self.assertEqual(first.status, "Done")
        self.assertEqual(first.requirements, ["FR-001"])
        self.assertEqual(first.depends, [])
        self.assertEqual(first.tests, "tests/test_health.py")
        self.assertTrue(first.has_criteria)
        self.assertEqual(first.epic, "E0: Foundation")
        self.assertEqual(stories[1].depends, ["US-000"])
        self.assertEqual(stories[1].tests, "")
        self.assertEqual(stories[1].short_title, "create an application")

    def test_missing_criteria(self) -> None:
        text = "### US-009: As a user, I want x, so that y.\n- Acceptance criteria:\n- Priority: MUST · Sprint: 1 · Status: Not started\n"
        story = wt.parse_stories(text)[0]
        self.assertFalse(story.has_criteria)

    def test_pipe_separator(self) -> None:
        text = "### US-009: As a user, I want x, so that y.\n- Acceptance criteria: works\n- Priority: COULD | Sprint: 3 | Status: In progress\n"
        story = wt.parse_stories(text)[0]
        self.assertEqual((story.priority, story.sprint, story.status), ("COULD", "3", "In progress"))
        self.assertTrue(story.has_criteria)

    def test_stories_inside_code_fences_are_ignored(self) -> None:
        text = "# Stories\n\n```markdown\n### US-999: As a user, I want an example, so that people copy it.\n- Priority: MUST · Sprint: 1 · Status: Done\n```\n\n" + STORIES
        ids = [s.id for s in wt.parse_stories(text)]
        self.assertNotIn("US-999", ids)
        self.assertEqual(ids, ["US-000", "US-001", "US-002"])

    def test_placeholder_requirement_rows_need_no_coverage(self) -> None:
        found = wt.parse_requirements("| FR-001 | TODO(whole-team) | B1 | MUST |\n| SEC-001 | Real | x | MUST |\n")
        self.assertEqual(found, {"FR-001": False, "SEC-001": True})

    def test_sprint_length_normalized(self) -> None:
        self.assertEqual(wt.normalize_sprint_length("7"), "7 days")
        self.assertEqual(wt.normalize_sprint_length("1"), "1 day")
        self.assertEqual(wt.normalize_sprint_length(" 2 weeks "), "2 weeks")

    def test_requirements_dropped(self) -> None:
        found = wt.parse_requirements(REQUIREMENTS)
        self.assertEqual(found, {"FR-001": True, "FR-002": True, "FR-003": True, "FR-004": False})

    def test_next_story_respects_dependencies(self) -> None:
        upcoming, blocked = wt.next_story(wt.parse_stories(STORIES))
        self.assertEqual(upcoming.id, "US-001")
        self.assertEqual([(s.id, w) for s, w in blocked], [("US-002", ["US-001"])])


class ProjectTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.cwd = os.getcwd()
        os.chdir(self.root)

    def tearDown(self) -> None:
        os.chdir(self.cwd)
        self.tmp.cleanup()

    def write(self, relative: str, text: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def test_init_lite_creates_docs_and_never_overwrites(self) -> None:
        self.write("SCOPE.md", "mine\n")
        code, out = run(["init", "--profile", "lite"])
        self.assertEqual(code, 0)
        self.assertEqual((self.root / "SCOPE.md").read_text(), "mine\n")
        self.assertIn("exists   SCOPE.md", out)
        for relative, _ in wt.LITE_DOCS:
            self.assertTrue((self.root / relative).exists(), relative)
        self.assertFalse((self.root / wt.REQUIREMENTS_PATH).exists())
        config = json.loads((self.root / ".whole-team.json").read_text())
        self.assertEqual(config["profile"], "lite")
        self.assertEqual(config["branches"]["integration"], "dev")

    def test_init_strict_assessment_ui(self) -> None:
        code, _ = run(["init", "--profile", "strict", "--assessment", "--ui", "--board", "notion", "--trunk"])
        self.assertEqual(code, 0)
        for relative in ["docs/09-uat/UAT_PLAN.md", "docs/04-design/DESIGN.md", "AI_USAGE.md", "docs/01-discovery/BRIEF_ANALYSIS.md", "docs/README.md"]:
            self.assertTrue((self.root / relative).exists(), relative)
        index = (self.root / "docs/README.md").read_text()
        self.assertIn("[docs/09-uat/UAT_PLAN.md](09-uat/UAT_PLAN.md)", index)
        self.assertIn("[SCOPE.md](../SCOPE.md)", index)
        config = json.loads((self.root / ".whole-team.json").read_text())
        self.assertEqual(config["branches"]["integration"], "main")
        self.assertEqual(config["viewports"], [390, 1024, 1280])

    def test_init_again_adds_flags_and_upgrades_profile(self) -> None:
        run(["init", "--profile", "lite"])
        code, out = run(["init", "--brief", "--profile", "standard"])
        self.assertEqual(code, 0)
        self.assertIn("profile lite -> standard", out)
        self.assertIn("brief on", out)
        config = json.loads((self.root / ".whole-team.json").read_text())
        self.assertEqual((config["profile"], config["brief"]), ("standard", True))
        self.assertTrue((self.root / "docs/01-discovery/BRIEF_ANALYSIS.md").exists())
        self.assertTrue((self.root / wt.REQUIREMENTS_PATH).exists())

    def test_init_again_applies_board_trunk_and_sprint_length(self) -> None:
        run(["init", "--profile", "lite", "--board", "local", "--sprint-length", "7"])
        config = json.loads((self.root / ".whole-team.json").read_text())
        self.assertEqual(config["sprint"]["length"], "7 days")
        code, out = run(["init", "--board", "github", "--trunk", "--sprint-length", "2 weeks"])
        self.assertEqual(code, 0)
        self.assertIn("board local -> github", out)
        self.assertIn("integration branch dev -> main", out)
        self.assertIn("sprint length 7 days -> 2 weeks", out)
        config = json.loads((self.root / ".whole-team.json").read_text())
        self.assertEqual(config["board"]["tool"], "github")
        self.assertEqual(config["branches"]["integration"], "main")
        self.assertEqual(config["profile"], "lite")

    def test_checkpoints_default_and_change(self) -> None:
        run(["init", "--profile", "lite"])
        config = json.loads((self.root / ".whole-team.json").read_text())
        self.assertEqual(config["checkpoints"], "every-step")
        code, out = run(["init", "--checkpoints", "phase"])
        self.assertIn("checkpoints every-step -> phase", out)
        code, out = run(["status"])
        self.assertIn("checkpoints phase", out)

    def test_docs_index_regenerated_keeping_statuses_and_extra_rows(self) -> None:
        run(["init", "--profile", "standard"])
        index = self.root / "docs/README.md"
        text = index.read_text().replace(
            "| [SCOPE.md](../SCOPE.md) | to be written |", "| [SCOPE.md](../SCOPE.md) | written |"
        ) + "| [docs/extra/NOTES.md](extra/NOTES.md) | written |\n"
        index.write_text(text)
        run(["init", "--assessment"])
        text = index.read_text()
        self.assertIn("| [SCOPE.md](../SCOPE.md) | written |", text)
        self.assertIn("[AI_USAGE.md](../AI_USAGE.md) | to be written", text)
        self.assertIn("[docs/10-reviews/TRACEABILITY.md]", text)
        self.assertIn("| [docs/extra/NOTES.md](extra/NOTES.md) | written |", text)

    def test_standard_has_use_cases_and_retros(self) -> None:
        run(["init", "--profile", "standard"])
        self.assertTrue((self.root / "docs/02-requirements/USE_CASES.md").exists())
        self.assertTrue((self.root / wt.RETROS_PATH).exists())
        self.assertFalse((self.root / "docs/09-uat/UAT_PLAN.md").exists())

    def test_wrong_separator_gets_a_hint(self) -> None:
        run(["init", "--profile", "lite"])
        self.write(wt.STORIES_PATH, STORIES.replace("Priority: MUST · Sprint: 1 · Status: Not started", "Priority: MUST, Sprint: 1, Status: Not started"))
        code, out = run(["lint"])
        self.assertEqual(code, 1)
        self.assertIn("separate fields with ' · '", out)

    def test_sprint_report_and_retro_actions(self) -> None:
        run(["init", "--profile", "standard"])
        self.write(wt.STORIES_PATH, STORIES.replace("Status: Not started\n- Depends on: US-000", "Status: Dropped\n- Depends on: US-000"))
        code, out = run(["sprint", "1"])
        self.assertEqual(code, 0)
        self.assertIn("Sprint 1: planned 1 · done 1 · not done 0 · dropped 1", out)
        self.assertIn("- US-000", out)
        retros = self.root / wt.RETROS_PATH
        retros.write_text(retros.read_text() + "\n## Sprint 1 retro\n\n### Actions\n- [ ] add a seed script (owner: me)\n- [x] done thing\n")
        code, out = run(["status"])
        self.assertIn("Retro actions open: 1", out)
        self.assertIn("Sprint 1: 1/1 stories done", out)

    def test_fresh_init_lints_with_warnings_only(self) -> None:
        run(["init", "--profile", "standard"])
        code, out = run(["lint"])
        self.assertEqual(code, 0, out)
        self.assertIn("placeholder", out)
        code, out = run(["lint", "--release"])
        self.assertEqual(code, 1)
        self.assertIn("MUST story is Not started", out)

    def test_lint_catches_story_problems(self) -> None:
        run(["init", "--profile", "standard"])
        self.write(wt.REQUIREMENTS_PATH, REQUIREMENTS)
        bad = STORIES + """
### US-001: As a duplicate, I want trouble, so that lint fails.
- Acceptance criteria: yes
- Priority: MUST · Sprint: 1 · Status: Not started

### US-003: Upload tweaks
- Acceptance criteria:
- Priority: HIGH · Sprint: 2 · Status: Doing
- Depends on: US-099 · Requirements: FR-999

### US-004: As an operator, I want to finish, so that it is done.
- Acceptance criteria: works
- Priority: MUST · Sprint: 1 · Status: Done
- Depends on: US-001
- Tests:
"""
        self.write(wt.STORIES_PATH, bad)
        code, out = run(["lint"])
        self.assertEqual(code, 1)
        for expected in [
            "duplicate ID",
            "no acceptance criteria",
            "priority 'HIGH'",
            "status 'Doing'",
            "depends on unknown US-099",
            "references FR-999",
            "Done but the Tests line is empty",
            "Done but its dependency US-001 is Not started",
            "title is not",
            "FR-003 is not covered",
        ]:
            self.assertIn(expected, out)
        self.assertNotIn("FR-004 is not covered", out)

    def test_status_reports_next_and_handover(self) -> None:
        run(["init", "--profile", "lite"])
        self.write(wt.STORIES_PATH, STORIES)
        self.write("CHANGELOG.md", "# Changelog\n\nHandover (2026-01-02): US-001 half done, run pytest next.\n")
        code, out = run(["status"])
        self.assertEqual(code, 0)
        self.assertIn("Stories: 3 total · Not started 2 · Done 1", out)
        self.assertIn("MUST done: 1/2", out)
        self.assertIn("Next up: US-001", out)
        self.assertIn("Blocked: US-002 waits on US-001", out)
        self.assertIn("Handover (2026-01-02)", out)

    def test_status_without_config_points_to_intake(self) -> None:
        code, out = run(["status"])
        self.assertEqual(code, 0)
        self.assertIn("intake", out)

    def test_release_gate_blocks_open_handover_and_sync(self) -> None:
        run(["init", "--profile", "lite"])
        done = re.sub(r"- Tests:[ \t]*$", "- Tests: tests/x.py", STORIES.replace("Status: Not started", "Status: Done"), flags=re.MULTILINE)
        self.write(wt.STORIES_PATH, done)
        for relative, _ in wt.LITE_DOCS:
            path = self.root / relative
            path.write_text(path.read_text().replace(wt.PLACEHOLDER, "filled"))
        self.write("CHANGELOG.md", "# Changelog\n\n- Board sync pending: US-002 Done\n- Handover: US-002 left\n")
        code, out = run(["lint", "--release"])
        self.assertEqual(code, 1)
        self.assertIn("Board sync pending", out)
        self.assertIn("open Handover", out)
        self.write("CHANGELOG.md", "# Changelog\n\n- Handover (resolved): US-002 left\n")
        code, out = run(["lint", "--release"])
        self.assertEqual(code, 0, out)

    def test_kanban_and_agreement(self) -> None:
        run(["init", "--profile", "lite", "--board", "github"])
        self.write(wt.STORIES_PATH, STORIES)
        code, _ = run(["kanban"])
        self.assertEqual(code, 0)
        board = (self.root / wt.KANBAN_PATH).read_text()
        self.assertIn("## Done (1)", board)
        self.assertIn("## Not started (2)", board)
        self.assertIn("**US-001** create an application · MUST · Sprint 1", board)
        code, out = run(["agreement"])
        self.assertEqual(code, 0)
        self.assertIn("**Profile:** lite · **Board:** github", out)
        self.assertIn("**Checkpoints:** every-step", out)
        self.assertIn("`feat/us-{id}-{slug}` from `dev`", out)
        self.assertNotIn("{profile}", out)

    def test_root_found_from_subdirectory(self) -> None:
        run(["init", "--profile", "lite"])
        sub = self.root / "src" / "deep"
        sub.mkdir(parents=True)
        os.chdir(sub)
        code, out = run(["status"])
        self.assertEqual(code, 0)
        self.assertIn("profile lite", out)


if __name__ == "__main__":
    unittest.main()
