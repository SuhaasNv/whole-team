# Branching and commits

## Contents
- Choose a model
- Branch types
- Naming
- Model A: main + dev (default)
- Model B: trunk-based (lite)
- Merging
- Releases and tags
- Hotfixes
- Protection and pushing
- Commits
- Recovering from mistakes

## Choose a model

| Model | Use when | Branches |
|-------|----------|----------|
| **A: main + dev** (default) | A deployed product, an assessment someone will read, anything with a development and a production environment | `main` (releases only), `dev` (integration), one short branch per story or fix |
| **B: trunk-based** | Lite projects, prototypes, a single environment | `main` plus one short branch per story, merged within a day |

Record the choice in `.whole-team.json` (`branches.integration` is `dev` for A, `main` for B; `wt.py init --trunk` sets B). In a brownfield repo, keep the model the project already uses unless the owner asks to change it.

## Branch types

| Type | From | Merges into | For | Lifetime |
|------|------|-------------|-----|----------|
| `feat/*` | integration | integration | One user story | Hours to two days |
| `fix/*` | integration | integration | A bug found before release | Hours |
| `chore/*` | integration | integration | Tooling, CI, dependencies, config | Hours |
| `docs/*` | integration | integration | Documentation only (sprint close, ADRs) | Hours |
| `refactor/*` | integration | integration | Behaviour-preserving restructuring the owner asked for | Hours |
| `test/*` | integration | integration | Tests only (coverage for existing behaviour) | Hours |
| `spike/*` | integration | never merged | Throwaway experiment to answer one question; findings go into an ADR or story | Under a day |
| `release/*` | `dev` | `main`, then back into `dev` | Optional stabilisation before a release (model A) | Days |
| `hotfix/*` | `main` | `main`, then `dev` | A bug in the released version | Hours |

One branch does one thing. If a story needs a tooling change first, put that change on a `chore/*` branch and merge it before the story branch.

## Naming

```
feat/us-<id>-<slug>      feat/us-012-create-application
fix/us-<id>-<slug>       fix/us-012-upload-size-check     (bug in a story's feature)
fix/<slug>               fix/login-rate-limit
chore/<slug>             chore/ci-postgres-service
docs/<slug>              docs/close-sprint-2
refactor/<slug>          refactor/extract-state-machine
spike/<slug>             spike/pdf-text-extraction
release/<version>        release/v0.3.0
hotfix/<slug>            hotfix/token-expiry
```

Lowercase, hyphens, a slug of two to five words. The story ID in the name links the branch to the board and to `USER_STORIES.md`.

## Model A: main + dev (default)

```
main   ──●─────────────────────●──────────●──   releases only, tagged v0.1.0, v0.2.0 ...
          \                   / \        /
dev        ●──●───●───●──●───●───●──●───●────   integration: always green, deployed to development
             \   / \     /          \  /
feat/us-010   ●─●   \   /            ●●         one story each, merged with --no-ff
feat/us-011          ●─●
hotfix/x                              (from main → main, then → dev)
```

- `main` receives only releases (a pull request from `dev`) and hotfixes. Never commit to it directly, with one exception: the first commit of a new repository (the setup scaffolding), from which `dev` is then created.
- `dev` is always buildable with CI green. It is what the development environment runs and what reviewers read between releases, so it only receives whole stories.
- Story branches start from an up-to-date `dev` and merge back when the story meets its Definition of Done.

```bash
git switch dev && git pull --ff-only          # skip pull without a remote
git switch -c feat/us-012-create-application
# ... commits ...
git switch dev
git merge --no-ff feat/us-012-create-application -m "feat: create application (US-012)"
git branch -d feat/us-012-create-application
```

## Model B: trunk-based (lite)

Same story branches, but they start from and merge into `main`. Keep them under a day. Releases are tags on `main`. Use a feature flag (a config value) only when an unfinished feature must merge; otherwise do not merge unfinished work.

## Merging

- **`--no-ff` into the integration branch** (default): each story is one visible merge commit, and `git log --first-parent dev` reads as a list of stories. Revert a whole story with `git revert -m 1 <merge>`.
- **Squash merge** is acceptable when the project already uses it (common with GitHub pull requests); then the squash commit message carries the story ID.
- **Rebase** a story branch onto the integration branch before merging if it has fallen behind and nobody else uses the branch. Never rebase `main`, `dev` or any branch someone else has pulled.
- Resolve conflicts on the story branch, re-run the full verification, then merge.
- Only whole stories merge. A story that is not Done stays on its branch, however long that takes.

## Releases and tags

- Model A: pull request `dev` → `main`, merged when CI is green, then an annotated tag on the merge commit: `git tag -a v0.3.0 -m "v0.3.0"`.
- Semantic versioning: `MAJOR.MINOR.PATCH`. Before 1.0.0 a minor bump per release is normal.
- A release candidate can be tagged on `dev` as `v0.3.0-rc.1` for the development environment without touching `main`.
- Release steps and their gates: [release.md](release.md).

## Hotfixes

```bash
git switch main && git pull --ff-only
git switch -c hotfix/token-expiry
# failing test first, then the minimal fix, then full verification
# with the owner's yes: merge into main, tag v0.3.1, deploy
git switch dev && git merge --no-ff hotfix/token-expiry   # so the fix is not lost
```

## Protection and pushing

- Suggest branch protection on `main` (pull requests only, required CI checks, no force push, no deletion) and on `dev` (no force push, no deletion). Setting it changes the user's GitHub settings: show the settings or the `gh api` call and let the owner apply it.
- **Every push needs the owner's yes in that turn.** Ask "Push dev to origin?" after the merge; a yes to one push does not cover the next.
- Never `git push --force` to a shared branch. On your own unpushed story branch, `--force-with-lease` after a rebase is fine with the owner's yes.

## Commits

Conventional commits:

```
<type>: <subject, imperative, about 50 characters, no full stop>

<optional body: why, not what, wrapped at 72>
```

| Type | For |
|------|-----|
| `feat` | A user-visible capability |
| `fix` | A bug fix |
| `test` | Tests only |
| `docs` | Documentation only |
| `refactor` | Structure change, no behaviour change |
| `perf` | Measured performance improvement |
| `chore` | Tooling, dependencies, CI, config |

- Reference the story in the merge commit (`(US-012)`) and the issue number if the board is GitHub (`(#34)`).
- Commit in small steps while working; each commit builds.
- Follow the project's rules on attribution trailers; if the owner has none, add none.

## Recovering from mistakes

| Mistake | Fix |
|---------|-----|
| Committed to `dev` or `main` by accident, not pushed | `git branch feat/us-<id>-<slug>` to keep the work, then `git reset --hard origin/<branch>` (or the previous commit) on the wrong branch, after checking `git status` is clean |
| Merged a story that was not Done, not pushed | `git reset --hard HEAD~1` on the integration branch (after confirming the merge is the last commit) |
| Merged a story that was not Done, already pushed | `git revert -m 1 <merge-commit>`, then push with the owner's yes |
| Secret committed | Stop. Tell the owner immediately; rotate the secret first, then clean history only with their yes |

Show every destructive command (`reset --hard`, `branch -D`, `push --force`) to the owner before it runs.
