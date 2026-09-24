# Contributing

Thanks for helping. whole-team is small on purpose, and I merge changes that keep it small first.

## Ground rules

- **Behaviour changes need an eval.** Add or update a case in `tools/gen_evals.py`, run `python3 tools/gen_evals.py`, show it fails before your change and passes after, and note the run in the results table in `evals/README.md`.
- **Keep `SKILL.md` short.** It is loaded whenever the skill triggers. Detail goes in a `reference/` file that `SKILL.md` links to itself (one level deep).
- **No tool-specific assumptions in the skill text.** Say "the platform's question tool" rather than naming one agent's tool, unless the text sits in a section marked as Claude Code only.
- **The script stays standard library only** and keeps its tests green.
- **House style:** plain words, no em dashes, forward slashes in paths.
- **Three copies of the license** (repository root, `plugins/whole-team/`, and the skill folder, so each installs self-contained) must stay identical; `tools/validate.py` checks it.
- **A new slash command** also goes in the `/whole-team:help` table and the README.

## Layout

```
.claude-plugin/marketplace.json     the marketplace (points at plugins/whole-team)
plugins/whole-team/                 the plugin that gets installed
  .claude-plugin/plugin.json
  skills/whole-team/                the Agent Skill (SKILL.md, reference/, templates/, scripts/)
  commands/                         slash commands
  agents/                           the reviewer agent
evals/  examples/  tools/           development only; not installed
```

## Before opening a pull request

```bash
python3 -m pip install pyyaml
python3 tools/validate.py
python3 -m unittest discover -s plugins/whole-team/skills/whole-team/scripts
claude plugin validate .        # if you have Claude Code
```

Bump the version in both `plugins/whole-team/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` and add a `CHANGELOG.md` entry when the change is user-visible.

Be kind, give feedback on the work and not the person, and help newcomers. This project follows the [Contributor Covenant 2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct/); report problems to the maintainer through [GitHub](https://github.com/SuhaasNv).
