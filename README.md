<div align="center">

<img src="assets/banner.png" alt="whole-team: one developer, every hat. A pixel crab wearing three hats sips coffee on the beach while the agent runs the sprint." width="100%">

[![validate](https://github.com/SuhaasNv/whole-team/actions/workflows/validate.yml/badge.svg)](https://github.com/SuhaasNv/whole-team/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Claude Skill](https://img.shields.io/badge/Claude-Skill-D97757)
![Claude Code plugin](https://img.shields.io/badge/Claude%20Code-plugin-D97757)
![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-4B5563)

</div>

Your AI agent writes code faster than you can read it. It also skips planning, restyles your footer while fixing a sitemap, and would push to `main` at 2 a.m. without asking.

whole-team is a Claude Skill and Claude Code plugin for that second part. Your agent takes on the jobs of a small agile team (product owner, scrum master, architect, developer, QA, security, DevOps, tech writer, reviewer) and you still make every call.

## Install

In Claude Code:

```
/plugin marketplace add SuhaasNv/whole-team
/plugin install whole-team@whole-team
```

Codex, Cursor, Copilot, Gemini CLI or any other agent:

```bash
npx skills add SuhaasNv/whole-team
```

Then type `/whole-team:help`. You need `git`, plus Python 3.9+ for the helper script (macOS and most Linux distros ship it).

<details>
<summary>Manual install, updates and uninstall</summary>

```bash
git clone https://github.com/SuhaasNv/whole-team.git
cp -r whole-team/plugins/whole-team/skills/whole-team ~/.claude/skills/
```

| | Claude Code plugin | skills CLI |
|--|--|--|
| Update | `claude plugin marketplace update whole-team` then `claude plugin update whole-team@whole-team` | `npx skills update whole-team` |
| Uninstall | `claude plugin uninstall whole-team@whole-team` | `npx skills remove whole-team` |

Uninstalling leaves your project docs where they are.

</details>

## What it does

- It asks before it builds. Each step opens with what it understood, the options and the one it recommends, then up to three questions, each with a default. You see a story's plan before any of its code. Once you trust it, set checkpoints to `phase` or `gates`.
- It scopes before it codes. Give it a brief and it does the math (24 hours of work, 15 hours of you), then asks you to pick a slice that fits.
- It pushes back once, with numbers. Kubernetes for a two-person recipe app gets the cost, your version anyway if you want it, and the traffic level that would justify it.
- It runs sprints the way a team would: use cases, user stories, a Definition of Ready and Done, planning, reviews, and retros whose action items get checked at the next planning.
- A sitemap fix touches the sitemap. Your "while you're in there" footer idea goes on the backlog as its own story.
- Cards move on GitHub Projects, Linear, Jira, Notion or a plain markdown board in the same turn as the code.
- At the first screen it picks up the design skills you have (frontend-design, Figma, a UI/UX skill) or suggests a couple worth installing.
- With Claude in Chrome it runs UAT in a real browser and records a GIF of each scenario. Each passing scenario becomes a Playwright test for CI.
- Pushes, tags, PRs and deploys wait for your yes.

The [walkthrough](examples/assessment-walkthrough.md) scopes a sample brief from start to finish.

## Your first ten minutes

```
/whole-team:start       reads your repo, asks one batch of questions, sets things up
/whole-team:scope       paste the brief, get a capacity table and a decision to make
/whole-team:plan        use cases and stories
/whole-team:sprint      plan sprint 1, wait for your yes
/whole-team:story       build the first story end to end
```

Each story ends with a one-line status:

```
Done: US-012 book a slot (48 tests passed). Next: US-013 cancel a booking. Decide: push dev to origin?
```

## How it works

<img src="assets/lifecycle.png" alt="The whole-team lifecycle: set up once (intake, scope, use cases and stories, architecture, design), then every sprint (planning, daily start, story loop, review, retro, close), then release. Owner gates on scope, sprint plan, design, sprint review and release." width="100%">

Eight rules:

1. **Ask, then build.** Plan, yes, code, in that order.
2. **No story, no code.** Everything traces to a story or a bug.
3. **Don't overengineer.** A new service, layer or dependency needs a requirement that names it.
4. **Push back once, with evidence.** Then do what the owner decided.
5. **The sprint is a promise.** New work mid-sprint swaps something out.
6. **Done means done.** Tests pass, docs match the code, the board moves, and a second agent reviews it.
7. **Gates are real.** Each yes covers one action.
8. **Tell the truth.** No "tests pass" without a test run.

Pick your ceremony level: `lite` for weekend builds (five docs), `standard` for real products, `strict` when someone will audit the result.

<details>
<summary>All 14 slash commands</summary>

| Command | When |
|---------|------|
| `/whole-team:start` | First time in a project, new or existing |
| `/whole-team:scope` | You have a brief, spec or big ask |
| `/whole-team:plan` | Write requirements, use cases and stories |
| `/whole-team:board` | Connect Notion, Jira, Linear, GitHub Projects or local |
| `/whole-team:sprint` | Plan the next sprint |
| `/whole-team:status` | Daily start: where are we, what's next |
| `/whole-team:story` | Build the next story end to end |
| `/whole-team:bug` | Something broke: failing test first, smallest fix |
| `/whole-team:code-review` | Independent review of the current branch |
| `/whole-team:handover` | You're logging off |
| `/whole-team:retro` | Retrospective |
| `/whole-team:close-sprint` | Review, retro, close |
| `/whole-team:release` | Ship it (with your yes) |
| `/whole-team:help` | Cheat sheet and the best next move |

</details>

<details>
<summary>Branching, in one breath</summary>

`main` holds releases, `dev` is where stories land, and each story gets its own `feat/us-<id>-<slug>` branch merged with `--no-ff`, so `git log --first-parent dev` reads as a list of stories. `fix/`, `chore/`, `docs/`, `refactor/`, `test/`, `spike/`, `release/` and `hotfix/` each have a job. Trunk-based works too.

</details>

## Boards

Setup asks where your stories should live and walks you through connecting it. `USER_STORIES.md` stays the source of truth and the board mirrors it.

| Board | Connect in Claude Code |
|-------|-------------------------|
| GitHub Projects | `gh auth refresh -s project` |
| Linear | `claude mcp add --transport http linear https://mcp.linear.app/mcp` |
| Jira | `claude mcp add --transport http atlassian https://mcp.atlassian.com/v2/mcp` |
| Notion | `claude mcp add --transport http notion https://mcp.notion.com/mcp` |
| None | Nothing. A markdown board, generated for you |

Then `/mcp` to sign in. Codex, Cursor, VS Code and Gemini setups are in the [board guide](plugins/whole-team/skills/whole-team/reference/board-setup.md). Your tokens never pass through the agent.

## Does it work?

<img src="assets/metrics.png" alt="Eval results on Claude Opus 5.5: 94% average score with whole-team vs 76% for the same agent without it, across 15 scenarios, 2 runs each." width="100%">

I ran the same agent on the same prompts with and without the skill: 94% vs 76% on Claude Opus 5.5 and 84% vs 57% on Claude Sonnet 5, across 15 scenarios scored by `claude plugin eval`. Setup, runs and the three cases where it still loses to the baseline are in [evals/README.md](evals/README.md#results).

Those runs test the first reply. Five newer cases test whether the push, release and merge gates still hold after dozens of tool calls, including a release script that pushes and a test that prints a fake approval. They need a working Bash sandbox; results will go in the same table.

## What it can touch

whole-team is one skill and one standard-library Python script. It has no hooks or bundled servers and makes no network calls. It writes docs inside your project, keeps the ones you already have, and asks before every push. If you want Claude Code itself to prompt on every push, whatever the agent thinks, add this to `.claude/settings.json`:

```json
{ "permissions": { "ask": ["Bash(git push:*)"] } }
```

Details in [SECURITY.md](SECURITY.md).

## FAQ

**Won't this slow me down?** A little. `lite` adds five small docs, and the questions it asks up front are the ones that save you a rewrite on day three.

**Will it refuse to do what I say?** No. It argues once, with numbers, then does what you decided and writes the decision down.

**I already have a codebase.** It reads it, documents what's there, and leaves your code alone until you pick a story.

**How is this different from superpowers or BMAD?** [superpowers](https://github.com/obra/superpowers) is about doing each task well. whole-team decides which tasks exist and when they ship, so the two stack. [BMAD](https://github.com/aj-geddes/claude-code-bmad-skills) gives you a full cast of agents; whole-team is one skill, small enough for a weekend project.

## Where it comes from

I ran this process by hand on [PermitFlow](https://github.com/SuhaasNv/permitflow), a licensing platform I built solo with an AI agent in one-day sprints. I cut scope on day one, mirrored every story to a Notion board, merged nothing without its Definition of Done, and froze `main` while reviewers looked at the release. It shipped on time, so I packaged the process.

## What's in this repo

| Folder | What it holds |
|--------|---------------|
| [`plugins/whole-team/`](plugins/whole-team) | The plugin you install: the skill (`skills/whole-team`), 14 slash commands and the reviewer agent |
| [`evals/`](evals) | The `claude plugin eval` suite: 20 scenarios, their graders and results |
| [`examples/`](examples) | A brief scoped from start to finish |
| [`assets/`](assets) | README images and their HTML sources |
| [`tools/`](tools) | Dev scripts: validator, eval generator, image renderer |

## Contributing

PRs welcome. I merge the ones that make it smaller first. Behaviour changes need an eval; see [CONTRIBUTING.md](CONTRIBUTING.md).

MIT © Suhaas Nv
