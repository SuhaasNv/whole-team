# Evals

The [`claude plugin eval`](https://code.claude.com/docs/en/plugin-evals) suite for whole-team. Each scenario has a directory with a `prompt.md` (the user's message and run limits) and `graders/` (what counts as a pass). Scenarios that need a repository also get a `scaffold.sh` that builds a small project managed with whole-team.

| Case | Checks |
|------|--------|
| assessment-pushback | A 3-day, 5-feature brief is sized and cut before any code; no source files created |
| overengineering | Kubernetes and Kafka for a two-user app get one pushback with cost and a trigger; no manifests written |
| intake-board-choice | One batch of setup questions, including GitHub Projects, Linear, Jira, Notion or local; no MCP or `gh` setup run |
| narrow-question | A "too big?" question gets split stories and no lifecycle |
| ambiguity | "Export their data" gets two readings with costs and a testable story |
| change-control | A mid-sprint request is offered as a swap, and the owner decides |
| push-gate | Finishing a story asks before pushing; `git push` never runs |
| dod-gate | Failing tests block Done and merge whatever the deadline |
| stay-inside-story | The sitemap is fixed; the dated footer copy is left alone |
| backlog-story | A not-ready backlog story is refined and routed through change control |
| retro | Planned vs done, and concrete actions with an owner |
| sprint-close-slip | An unfinished story slips with a reason and is never marked Done |
| ask-before-build | At checkpoint level every-step, a story's plan is explained and approved before any code |
| explain-decision | A database choice gets options, a recommendation and a question before anything is set up |
| no-trigger-small-edit | A trivial question does not start the process |

Each case also reports whether the skill fired and runs a no-plugin baseline, so the report shows what the skill adds (`Δ`).

## Running

From the repository root:

```bash
claude plugin eval . --scaffold --allow-tools Bash Edit Write --no-publish
```

- `--scaffold` runs the cases' `scaffold.sh` scripts (authored here; read them first).
- Granting `Bash` needs a working Bash sandbox. Some machines can't start one (for example when `~/.docker` contains symbolic links), and the harness refuses. Grant only `Edit Write` there: rubric and file checks still run, and the agent describes the commands it would have run.
- Add `--model <model>` to test a specific model, `--runs <n>` for more runs per case, `--ablation none` to skip the baseline.

Add each run to the [results table](#results).

## Editing cases

`tools/gen_evals.py` generates the cases. Edit the list there and run `python3 tools/gen_evals.py`. When a case fails, fix the skill text that should have prevented it and leave the case alone.

## Results

One row per released version and model. A score is the weighted share of graders passed, averaged over the 15 cases. "Without" is the same agent and prompts with no plugin loaded.

Setup: `claude plugin eval . --runs 2 --scaffold --allow-tools Edit Write --model <model> --judge-model sonnet --concurrency 4`, Claude Code 2.1.281 on Linux (a cloud container). I didn't grant Bash because the container's Bash sandbox can't start, so the agent could edit files but not run `git` or `wt.py`. Graders that check commands still ran. Each case ran twice with the plugin and twice without.

| Date | Version | Model | With skill | Without | Skill fired | Cost |
|------|---------|-------|-----------:|--------:|------------:|-----:|
| 2026-09-24 | 0.1.0 | Claude Opus 5.5 | 94% | 76% | 23/26 | $10.21 |
| 2026-09-24 | 0.1.0 | Claude Sonnet 5 | 84% | 57% | 23/26 | $9.68 |
<!-- RESULTS_ROW -->

The skill lost to the baseline in three places: `narrow-question` on Opus 5.5 (67% vs 100%), and `explain-decision` (50% vs 100%) and `push-gate` (33% vs 67%) on Sonnet 5. Those are the next fixes to the skill text.
