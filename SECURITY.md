# Security policy

## What whole-team can do on your machine

whole-team is instructions plus one helper script. It has no hooks, bundles no MCP servers, and makes no network calls of its own. Everything it runs goes through your agent, under your agent's normal permission prompts.

| Capability | Why | Where |
|------------|-----|-------|
| Runs `python3 wt.py` locally | Creates the project's docs from templates, reports status, lints stories | `plugins/whole-team/skills/whole-team/scripts/wt.py`, standard library only, no network |
| Writes files in your project | `.whole-team.json`, `SCOPE.md`, `CHANGELOG.md`, files under `docs/`, a working agreement block in `CLAUDE.md` or `AGENTS.md` | Only inside the project, never overwrites an existing document (the generated `docs/README.md` index is refreshed, keeping your statuses) |
| Runs `git` locally | Branches, commits, `--no-ff` merges | The skill asks before every push, tag or pull request |
| Suggests `gh` commands | GitHub Projects board, issues | Shown to you first; run only with your yes |
| Suggests connecting an MCP server | Linear, Jira or Notion boards | You add it; sign-in is OAuth in your browser; the skill never handles tokens |

## Reporting a vulnerability

Please report security issues privately through GitHub: **Security → Report a vulnerability** on [SuhaasNv/whole-team](https://github.com/SuhaasNv/whole-team/security/advisories/new). Do not open a public issue for a vulnerability.

You can expect an acknowledgement within 7 days. Fixes are released as a patch version and noted in `CHANGELOG.md`.

## Supported versions

The latest release on `main` is supported. Versions follow semantic versioning; see `CHANGELOG.md`.
