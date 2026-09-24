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

Only when the user wants to set up a project. Do a narrow task (write a story, split one, answer a question) first and offer setup in one line at the end.

Use the platform's question tool if it has one (multiple choice, recommendation first); otherwise a short numbered list. Skip any question the repo already answered and state what you inferred instead.

1. **What are we building, for whom, and by when?** Or: paste the brief. If the message already contains a brief or a build request, scope it and push back first ([scoping-and-pushback.md](scoping-and-pushback.md)) and put the remaining questions below at the end of that same reply.
2. **Ceremony profile: lite, standard or strict** (name all three and recommend one). Recommend from signals:
   - assessment, take-home, client handover, regulated domain: `strict` (or `standard` if the time box is under two days)
   - real users or a portfolio piece: `standard`
   - prototype, weekend, internal tool: `lite`
3. **Where should stories and use cases live?** Offer: GitHub Projects, Linear, Jira, Notion, or a local markdown board. Recommend what the user or their team already uses; if nothing, GitHub Projects when the repo is on GitHub, else local. Tell them the markdown file stays the portable record either way. Details and connection steps: [board-setup.md](board-setup.md).
4. **Sprint length:** default one-day sprints for projects of a week or less, one-week sprints for longer ones (pass it as `--sprint-length "1 day"`, `"1 week"`, `"2 weeks"`).
5. **Branching:** recommend `main` (releases) + `dev` (integration) + one branch per story, merged with `--no-ff`. Offer trunk-based (short branches straight into `main`) for lite projects. Brownfield: keep what the repo already does. Details: [branching.md](branching.md).
6. **Viewports to verify (UI only):** default 390, 1024 and 1280 px.
7. **How often should I stop and ask?** `every-step` (default: explain and ask at every step), `phase` (only at phase boundaries) or `gates` (only for approvals). See [checkpoints.md](checkpoints.md).

Do not ask about tech stack preferences the user has not raised unless the choice blocks the first story; propose a boring default in the architecture step instead.

## 3. Configure

```bash
python3 <skill-dir>/scripts/wt.py init --profile <p> [--ui] [--brief] [--assessment] [--trunk] [--checkpoints <level>] --board <github|linear|jira|notion|local>
```

This writes `.whole-team.json` and the profile's documents from templates (skipping any that exist). Then:

- Connect the board: [board-setup.md](board-setup.md). Record its identifiers in `.whole-team.json` under `board`.
- Run `wt.py agreement` and append its output to the project's `CLAUDE.md` (Claude Code) or `AGENTS.md` (other agents). Show the user the block; it is their project's rulebook.
- Commit the scaffolding: `chore: set up whole-team`. In a new repository this first commit goes on `main` because no other branch exists yet; it is the one allowed direct commit to `main`. Then, if the owner chose `main` + `dev`, create `dev` from it: `git switch -c dev`. In an existing repository, commit on a `chore/whole-team-setup` branch from the integration branch instead.

## 4. Hand off

One line to the user: profile, board, sprint length, and the next step (scoping if there is a brief, otherwise requirements and stories). Then continue.
