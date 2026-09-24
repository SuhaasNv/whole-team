# Evals

Scenario evaluations for the whole-team skill, in the format suggested by Anthropic's skill authoring guide. Each case has a user query and the behaviours a correct run shows.

## Running them

There is no built-in runner for skill evals. The method used for this repo:

1. Install the skill (see the README) in a fresh session, in a scratch repository.
2. Give the agent the `query` of one case. Answer its questions briefly as a reasonable owner would.
3. Grade each `expected_behavior` line as met or not met. A case passes when every line is met.
4. Record the result in [RESULTS.md](RESULTS.md) with the date, the model and the skill version.

Run every case after changing `SKILL.md` or a reference file, and on each model you support. When a case fails, fix the skill text that should have prevented it, not the case.
