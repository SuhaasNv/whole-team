# Eval results

Results for each released version. Scores are the mean over all 15 cases of the weighted share of graders passed; "without" is the same agent and prompts with no plugin loaded.

Setup: `claude plugin eval . --runs 2 --scaffold --allow-tools Edit Write --model sonnet --judge-model sonnet`, Claude Code 2.1.281 on macOS. Bash was not granted on the test machine (its Bash sandbox refuses to start there), so the agent could edit files but not run `git` or `wt.py`; graders that check commands still ran.

| Date | Version | With skill | Without | Skill fired | Cost |
|------|---------|-----------:|--------:|------------:|-----:|
<!-- RESULTS_ROW -->
