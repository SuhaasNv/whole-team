#!/usr/bin/env python3
"""Repository checks for the whole-team skill and plugin. Needs PyYAML.

Checks: SKILL.md frontmatter against the Agent Skills rules, SKILL.md length,
relative links, contents sections in long reference files, command and agent
frontmatter, plugin and marketplace manifests, templates used by wt.py, and
house style (no em dashes).

Run from the repository root: python3 tools/validate.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import List, Optional, Tuple

import yaml

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "plugins" / "whole-team"
SKILLS = PLUGIN / "skills"
NAME_RULE = re.compile(r"^[a-z0-9-]{1,64}$")
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
MAX_SKILL_LINES = 500
CONTENTS_THRESHOLD = 100

errors: List[str] = []


def fail(message: str) -> None:
    errors.append(message)


def frontmatter(path: Path) -> Tuple[Optional[dict], str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if not match:
        fail(f"{path.relative_to(ROOT)}: no YAML frontmatter")
        return None, text
    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError as error:
        fail(f"{path.relative_to(ROOT)}: frontmatter is not valid YAML: {error}")
        return None, match.group(2)
    if not isinstance(data, dict):
        fail(f"{path.relative_to(ROOT)}: frontmatter is not a mapping")
        return None, match.group(2)
    return data, match.group(2)


def check_skill(skill_dir: Path) -> None:
    skill_file = skill_dir / "SKILL.md"
    rel = skill_file.relative_to(ROOT)
    if not skill_file.is_file():
        fail(f"{skill_dir.relative_to(ROOT)}: no SKILL.md")
        return
    data, body = frontmatter(skill_file)
    if data is None:
        return
    name = data.get("name", "")
    description = data.get("description", "")
    if not isinstance(name, str) or not NAME_RULE.match(name):
        fail(f"{rel}: name must be 1-64 lowercase letters, digits or hyphens")
    elif any(word in name for word in ("anthropic", "claude")):
        fail(f"{rel}: name must not contain reserved words")
    elif name != skill_dir.name:
        fail(f"{rel}: name '{name}' does not match directory '{skill_dir.name}'")
    if not isinstance(description, str) or not description.strip():
        fail(f"{rel}: description is required")
    else:
        if len(description) > 1024:
            fail(f"{rel}: description is {len(description)} characters (max 1024)")
        if re.search(r"<[^>]+>", description):
            fail(f"{rel}: description must not contain XML tags")
    lines = body.count("\n") + 1
    if lines > MAX_SKILL_LINES:
        fail(f"{rel}: body is {lines} lines (max {MAX_SKILL_LINES})")

    for reference in sorted((skill_dir / "reference").glob("*.md")):
        text = reference.read_text(encoding="utf-8")
        if text.count("\n") > CONTENTS_THRESHOLD and "## Contents" not in text:
            fail(f"{reference.relative_to(ROOT)}: over {CONTENTS_THRESHOLD} lines without a '## Contents' section")
        linked = f"reference/{reference.name}"
        if linked not in body:
            fail(f"{rel}: does not link {linked} (keep references one level deep)")

    sys.path.insert(0, str(skill_dir / "scripts"))
    try:
        import wt  # type: ignore
    except ImportError:
        return
    docs = wt.STRICT_DOCS + wt.UI_DOCS + wt.ASSESSMENT_DOCS
    for _, template in docs:
        if template and not (skill_dir / "templates" / template).is_file():
            fail(f"{rel}: wt.py uses missing template {template}")


def check_links(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    for target in LINK.findall(text):
        if re.match(r"^[a-z]+:", target) or target.startswith("#"):
            continue
        clean = target.split("#", 1)[0]
        if clean and not (path.parent / clean).exists():
            fail(f"{path.relative_to(ROOT)}: broken link {target}")


def check_commands_and_agents() -> None:
    for command in sorted((PLUGIN / "commands").glob("*.md")):
        data, _ = frontmatter(command)
        if data is not None and not data.get("description"):
            fail(f"{command.relative_to(ROOT)}: description is required")
    for agent in sorted((PLUGIN / "agents").glob("*.md")):
        data, _ = frontmatter(agent)
        if data is None:
            continue
        for key in ("name", "description"):
            if not data.get(key):
                fail(f"{agent.relative_to(ROOT)}: {key} is required")
        if data.get("name") and data["name"] != agent.stem:
            fail(f"{agent.relative_to(ROOT)}: name '{data['name']}' does not match file name")


def check_manifests() -> None:
    try:
        plugin = json.loads((PLUGIN / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
        market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f".claude-plugin: {error}")
        return
    entries = [p for p in market.get("plugins", []) if p.get("name") == plugin.get("name")]
    if not entries:
        fail("marketplace.json: no entry for the plugin in plugin.json")
        return
    if entries[0].get("version") != plugin.get("version"):
        fail(f"version mismatch: plugin.json {plugin.get('version')} vs marketplace.json {entries[0].get('version')}")
    source = entries[0].get("source", "")
    if not isinstance(source, str) or (ROOT / source).resolve() != PLUGIN.resolve():
        fail(f"marketplace.json: source {source!r} does not point at plugins/whole-team")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8") if (ROOT / "CHANGELOG.md").exists() else ""
    if f"## {plugin.get('version')}" not in changelog:
        fail(f"CHANGELOG.md: no '## {plugin.get('version')}' entry")


def check_licenses() -> None:
    root_license = (ROOT / "LICENSE").read_bytes()
    for copy in (PLUGIN / "LICENSE", SKILLS / "whole-team" / "LICENSE"):
        if not copy.is_file() or copy.read_bytes() != root_license:
            fail(f"{copy.relative_to(ROOT)}: missing or different from the root LICENSE")


def check_style(path: Path) -> None:
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if "—" in line:
            fail(f"{path.relative_to(ROOT)}:{number}: em dash (house style: use a colon, comma or middle dot)")


def main() -> int:
    for skill_dir in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        check_skill(skill_dir)
    markdown = [p for p in ROOT.rglob("*.md") if ".git" not in p.parts]
    for path in markdown:
        check_links(path)
        check_style(path)
    check_commands_and_agents()
    check_manifests()
    check_licenses()
    for message in errors:
        print(f"error  {message}")
    print(f"validate: {len(errors)} error(s) in {len(markdown)} markdown files")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
