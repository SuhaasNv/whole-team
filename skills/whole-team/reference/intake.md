# Intake

Goal: from nothing to a configured project in one round of questions. Look before you ask; ask only what the repo cannot tell you.

## 1. Look first (read-only)

- `README*`, `CLAUDE.md`, `AGENTS.md`, `.cursorrules`, existing `docs/`
- Package and build files (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `pom.xml`, `Dockerfile`, compose files, CI workflows)
- `git log --oneline -20`, branch names, remote (`git remote -v`): is it on GitHub?
- Is there a UI? Tests? CI? A deploy target?
- Is there a brief, assessment or spec file in the repo or in the user's message?

Classify: **greenfield** (empty or near-empty repo) or **brownfield** (working code). Brownfield continues in [brownfield.md](brownfield.md) after the questions below.

## 2. Ask one batch

Use the platform's question tool if it has one (multiple choice, recommendation first); otherwise a short numbered list. Skip any question the repo already answered and state what you inferred instead.

1. **What are we building, for whom, and by when?** Or: paste the brief. (If a brief exists, the next step is [scoping-and-pushback.md](scoping-and-pushback.md), not more questions.)
2. **Profile:** lite, standard or strict. Recommend from signals:
   - assessment, take-home, client handover, regulated domain: `strict` (or `standard` if the time box is under two days)
   - real users or a portfolio piece: `standard`
   - prototype, weekend, internal tool: `lite`
3. **Where should stories and use cases live?** Offer: GitHub Projects, Linear, Jira, Notion, or a local markdown board. Recommend what the user or their team already uses; if nothing, GitHub Projects when the repo is on GitHub, else local. Say that the markdown file stays the portable record either way. Details and connection steps: [board-setup.md](board-setup.md).
4. **Sprint length:** default one-day sprints for projects of a week or less, one-week sprints for longer ones.
5. **Branching:** recommend `main` (releases) + `dev` (integration) + one branch per story, merged with `--no-ff`. Offer trunk-based (short branches straight into `main`) for lite projects. Brownfield: keep what the repo already does. Details: [branching.md](branching.md).
6. **Viewports to verify (UI only):** default 390, 1024 and 1280 px.

Do not ask about tech stack preferences the user has not raised unless the choice blocks the first story; propose a boring default in the architecture step instead.

## 3. Configure

```bash
python3 <skill-dir>/scripts/wt.py init --profile <p> [--ui] [--brief] [--assessment] [--trunk] --board <github|linear|jira|notion|local>
```

This writes `.whole-team.json` and the profile's documents from templates (skipping any that exist). Then:

- Connect the board: [board-setup.md](board-setup.md). Record its identifiers in `.whole-team.json` under `board`.
- Run `wt.py agreement` and append its output to the project's `CLAUDE.md` (Claude Code) or `AGENTS.md` (other agents). Show the user the block; it is their project's rulebook.
- If `dev` does not exist and the user chose it: `git switch -c dev` from `main`.

## 4. Hand off

One line to the user: profile, board, sprint length, and the next step (scoping if there is a brief, otherwise requirements and stories). Then continue.
