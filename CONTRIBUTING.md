# Contributing

Thanks for helping. whole-team is small on purpose, and I merge changes that keep it small first.

## Ground rules

- **Behaviour changes need an eval.** Add or update a case in `tools/gen_evals.py`, run `python3 tools/gen_evals.py`, show it fails before your change and passes after, and add the run to the results table in `evals/README.md`.
- **Keep `SKILL.md` short.** Agents load it every time the skill triggers. Detail goes in a `reference/` file that `SKILL.md` links to directly (one level deep).
- **Don't name one agent's tools in the skill text.** Write "the platform's question tool", unless the section is marked Claude Code only.
- **`wt.py` stays standard library only**, and its tests stay green.
- **House style:** plain words, no em dashes, forward slashes in paths.
- **Keep the three license copies identical** (repository root, `plugins/whole-team/`, and the skill folder, so each installs self-contained). `tools/validate.py` checks this.
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

For a user-visible change, add a `CHANGELOG.md` entry and bump the version in both `plugins/whole-team/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`.

Be kind, and critique the work rather than the person. This project follows the [Contributor Covenant 2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct/); report problems to me through [GitHub](https://github.com/SuhaasNv).
