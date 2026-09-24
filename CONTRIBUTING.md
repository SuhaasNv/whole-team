# Contributing

Thanks for helping. whole-team is small on purpose; changes that keep it small are the easiest to accept.

## Ground rules

- **Behaviour changes need an eval.** Add or update a case in `evals/evals.json` that fails before your change and passes after it, and note the run in `evals/RESULTS.md`.
- **Keep `SKILL.md` short.** It is loaded whenever the skill triggers. Detail goes in a `reference/` file linked directly from `SKILL.md` (one level deep).
- **No tool-specific assumptions in the skill text.** Say "the platform's question tool" rather than naming one agent's tool, unless the text is inside a clearly marked Claude Code section.
- **The script stays standard library only** and keeps its tests green.
- **House style:** plain words, no em dashes, forward slashes in paths.

## Before opening a pull request

```bash
python3 -m pip install pyyaml
python3 tools/validate.py
python3 -m unittest discover -s skills/whole-team/scripts
claude plugin validate .        # if you have Claude Code
```

Bump the version in both `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` and add a `CHANGELOG.md` entry when the change is user-visible.
