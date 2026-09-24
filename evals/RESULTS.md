# Eval results

Results for each released version. Scores are the mean over all 15 cases of the weighted share of graders passed; "without" is the same agent and prompts with no plugin loaded.

Setup: `claude plugin eval . --runs 2 --scaffold --allow-tools Edit Write --model <model> --judge-model sonnet --concurrency 4`, Claude Code 2.1.281 on Linux (a cloud container). Bash was not granted: the container's Bash sandbox cannot start, so the agent could edit files but not run `git` or `wt.py`; graders that check commands still ran. Each case runs twice with the plugin and twice without.

| Date | Version | Model | With skill | Without | Skill fired | Cost |
|------|---------|-------|-----------:|--------:|------------:|-----:|
| 2026-09-24 | 0.1.0 | Claude Opus 5.5 | 94% | 76% | 23/26 | $10.21 |
| 2026-09-24 | 0.1.0 | Claude Sonnet 5 | 84% | 57% | 23/26 | $9.68 |
<!-- RESULTS_ROW -->

Where the skill scored lower than the baseline: `narrow-question` on Opus 5.5 (67% vs 100%); `explain-decision` (50% vs 100%) and `push-gate` (33% vs 67%) on Sonnet 5. Those are the next cases to fix in the skill text.
