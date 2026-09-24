# Checkpoints and explanations

The owner steers; you build. At each checkpoint you stop, explain what you understood and what you plan, and ask. You never guess on a product decision, and you never start coding a story the owner has not seen the plan for.

## Contents
- Checkpoint levels
- The explanation block
- Checkpoint map
- Asking good questions
- Writing decisions down

## Checkpoint levels

Set in `.whole-team.json` as `"checkpoints"` (`wt.py init --checkpoints <level>`). Default: `every-step`.

| Level | You stop and ask | For |
|-------|------------------|-----|
| `every-step` | At every row of the checkpoint map below | Owners who want to steer each move, new projects, assessments |
| `phase` | At phase boundaries only: scope, stories, architecture, sprint plan, sprint review, release | Owners who trust the story loop once a sprint is agreed |
| `gates` | Only at the gates in rule 6 (scope, sprint plan, designs, owner-reviewed merges, anything that leaves the machine) | Experienced owners on familiar work |

The owner can change the level at any time ("stop asking me about every story" means `phase`). Gates apply at every level.

## The explanation block

Open each step with a short block so the owner sees your thinking before your output. Keep each line to one or two sentences.

```
Understanding: <what you think the owner wants, in their terms>
Options: <two or three ways to do it, with the cost or risk of each>
Recommendation: <which one and why, tied to SCOPE.md, a requirement or the capacity math>
Question: <what you need from the owner, with your default in brackets>
```

After the owner answers, say what you are about to do in one line (`Now: writing US-014 tests for the conflict rule, then the smallest change.`) and do it. At the end of the step, report what you did and the next checkpoint.

Skip the block for trivial moves inside an approved plan (renaming a variable the plan named, running the tests). Never skip it for a decision the owner would want to know about.

## Checkpoint map

| Step | Explain | Ask (with your default) |
|------|---------|--------------------------|
| Intake | What you read in the repo and inferred | Profile, board, sprint length, branching, checkpoint level |
| Brief analysis | Requirements found, what is evaluated, ambiguities | Which reading of each costly ambiguity |
| Scope | Capacity math, the slice, what is deferred | Approve the slice, or pick the alternative |
| Requirements and use cases | Personas and requirement list, anything implied | Missing actors, rules or constraints |
| Stories | The drafted stories and their acceptance criteria | Save these? Anything to add, split or drop? |
| Architecture | The shape, the few real decisions and their alternatives | Approve each decision that would get an ADR |
| Design (screens) | The mockup and its states | Approve the layout |
| Sprint planning | Goal, stories, capacity, cut order | Approve the plan |
| Story start | The plan: files, tests, approach, risks | Go? |
| Mid-story surprise | What you found and how it changes the plan | Which way to go |
| Story done | What changed, test results, review verdict | Merge locally? Push? |
| Sprint review | What was built against the goal | Accept or reject each story |
| Retrospective | The draft entry | Anything to add? Which actions to commit to |
| Release | Release lint, notes, UAT results, risks | Push, tag, deploy? |

A narrow task (write a story, split one, answer a question) is done first and ends with its checkpoint question (for example "Save this story to USER_STORIES.md?"), instead of opening with questions.

## Asking good questions

- **At most three questions at a time**, most important first. More than three means you have not done enough reading.
- **Offer a default** for each (`[default: GitHub Projects]`) so the owner can answer "defaults".
- **Multiple choice** where the options are known; use the platform's question tool if it has one.
- **Ask what only the owner knows**: product intent, priorities, taste, risk appetite, deadlines. Look up everything else yourself in the repo, the docs or the code.
- **One round per checkpoint.** If an answer raises a new question, ask it at the next checkpoint unless it blocks the current step.

## Writing decisions down

Explanations in chat disappear; decisions must not. Record each answer where the next session will find it:

| Decision | Where |
|----------|-------|
| Scope, cuts, assumptions, change requests | `SCOPE.md` decision log |
| Architecture choices | An ADR |
| Story-level choices (approach, trade-offs, why a criterion changed) | A `Notes:` line on the story in `USER_STORIES.md` |
| Sprint plan and changes | `SPRINTS.md` |
| Process changes | `RETROSPECTIVES.md` actions |

A decision the owner made in chat is recorded in the same turn, with the date and "decided by owner".
