# Right-sizing: do not overengineer

Build for the requirements you have, with room to change, not for the ones you imagine. The goal is the smallest design that is correct, tested and easy to change later.

## Default shape

Unless a requirement says otherwise:
- **One deployable** (a modular monolith): modules by domain, one process, one repo.
- **One database** (Postgres for anything multi-user; SQLite for single-user or prototypes).
- **One frontend** if there is a UI (server-rendered or a single SPA).
- **One deploy target** on a managed platform (Railway, Render, Fly, Vercel, a single VM). No Kubernetes.
- **Background work in-process** (a task runner or scheduled job) until a named need proves otherwise.
- **Boring, well-known libraries** with active maintenance. Fewer is better.

Layering inside the monolith: `api` → `services` → `domain` and `repositories` → `models`. `domain` holds rules and has no I/O, so it is trivial to test.

## The rules

1. **Every new moving part needs a requirement ID.** A service, queue, cache, layer, framework, dependency or config option names the requirement (FR, NFR, SEC) that needs it. No ID, no part.
2. **Rule of two.** No shared helper or abstraction until there are two real uses; no framework or plugin system until three.
3. **Interfaces only at real seams:** external providers (payments, email, AI models), storage, the clock. Where you need a test double or expect a swap. Not around your own code "just in case".
4. **Measure before optimizing.** No caching, denormalizing or async rewrites without a measured problem and a target number.
5. **Configuration only for values that differ between environments.** Everything else is code.
6. **Delete over deprecate** in code you own and nobody else calls.
7. **No speculative generality.** Do not add parameters, flags, tables or endpoints for users who do not exist yet.

## Inside a story: change only what it needs

Scope creep also happens one diff at a time: a bug fix that also restyles the page, rewrites copy, reformats files, bumps dependencies, replaces short comments with essays, or adds an unrequested report. Each is small; together they make a change impossible to review and easy to break. Rules:
- Every file in the diff is explained by the story's acceptance criteria or its tests and docs.
- No unrequested changes to copy, colours, layout, formatting, comments or dependencies.
- No extra artifacts (reports, summaries, new docs) unless the story or the hats table asks for them.
- Improvements you notice, and extras the user mentions in passing, become candidate stories, not part of this one. Say so in the reply.

## Red-flag phrases

When you or the user says one of these, stop and ask for the requirement behind it: "in case we need", "future-proof", "scale to millions", "make it generic", "plugin system", "microservices", "event-driven", "we might switch databases".

## Simple, never sloppy

Right-sizing never cuts these. They are the difference between a small system and a broken one:
- Server-side authorization on every endpoint, tested with the wrong role and the wrong owner
- Input validation at the boundary; one consistent error shape
- Transactions around multi-step writes; audit records written in the same transaction when required
- Explicit state transitions in one place when an entity has a status
- Tests on the critical user journey, end to end
- Secrets from the environment, documented in `.env.example`
- Health check, structured logs with request IDs, and a README that gets a clean clone running

## Review checklist (architecture step and every story)

```
- [ ] New service, container, queue, cache or datastore? Requirement ID: ____ (else remove)
- [ ] New dependency? Needed for this story's acceptance criteria? Maintained? (else remove)
- [ ] New abstraction or layer? Two real uses today? (else inline)
- [ ] New config option? Differs between environments? (else constant)
- [ ] Anything built for a user, load or feature not in SCOPE.md? (else remove)
- [ ] Any file in the diff the story does not need? (else revert it or split it into its own story)
- [ ] Anything from "Simple, never sloppy" missing? (else add)
```

## When the user asks for more

Push back once with cost and a named trigger for revisiting (see the overengineering example in [scoping-and-pushback.md](scoping-and-pushback.md)). If they still want it, it is their call: record it as a decision with its reason and build it well.
