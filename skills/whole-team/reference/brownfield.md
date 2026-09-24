# Adopting an existing codebase

Goal: bring an existing repo under the method without breaking it or rewriting it. The code is the source of truth; the docs are written from it.

## 1. Survey (read-only)

- Structure: top-level directories, modules, entry points.
- Stack and versions from build files; how to run it; how to test it (run the tests and record the result: this is the baseline).
- CI and deployment: workflows, hosting, environments.
- Git: branches, recent history, commit style, open pull requests and issues (`gh issue list`, `gh pr list` if on GitHub).
- Existing process files: README, CONTRIBUTING, CLAUDE.md, AGENTS.md, docs, ADRs, TODO comments.

Do not reformat, upgrade, or refactor anything during adoption.

## 2. Write down what exists

- `docs/03-architecture/ARCHITECTURE.md` from the code: stack, modules, API table (with roles as enforced today), data model, configuration. Mark anything uncertain as `Unverified:` rather than guessing.
- `SCOPE.md`: what the product does today (as the baseline), what the owner wants next, what is out of scope.
- `USER_STORIES.md`: existing features as Done stories only if useful for traceability; otherwise start the file with the next planned work. Open issues become candidate stories.
- `DEFINITION_OF_DONE.md`: start from what CI and the codebase already enforce; list the gap to the target as **DoD debt** (for example "no integration tests for the billing module"). Each debt item becomes a story or is accepted with a reason.

## 3. Match conventions

Keep the project's existing branch names, commit style, formatting and folder layout unless the owner asks to change them. Record the choice in `.whole-team.json` (`branches`) and the working agreement.

## 4. Report drift

List every place where docs, comments or config disagree with the code, and every risk found (missing authorization checks, secrets in the repo, failing tests, unpinned dependencies). Present it to the owner as candidate stories with priorities; fix nothing without a yes. Secrets in the repo are raised immediately.

## 5. Continue

Pick a profile with the owner, run `wt.py init` (it skips files that exist), connect the board, and start the story loop with the highest-priority story.
