# Architecture, data model, decisions, threat model

Start from [right-sizing.md](right-sizing.md). Architecture here means the few decisions that are expensive to change, written down so the next person (or session) does not re-decide them.

## Architecture one-pager

`docs/03-architecture/ARCHITECTURE.md` (template provided). Keep it to what exists:
- **Stack in three to five sentences.**
- **Context diagram:** actors, the system, external services. Use Mermaid in the markdown so it renders on GitHub and stays diffable.
- **Modules:** one line each, with what they own.
- **Key flows:** the critical journey as a short sequence (Mermaid `sequenceDiagram` or numbered steps).
- **API table:** method, path, roles allowed, purpose. Every endpoint lists its roles.
- **Data model summary:** entities and relationships (Mermaid `erDiagram`); details in `DOMAIN_MODEL.md` for strict.
- **Error shape:** one format everywhere, for example `{ "error": { "code", "message", "details"? } }`.
- **Configuration:** every environment variable, mirrored in `.env.example`.

When code changes an endpoint, entity, state or flow, update this file in the same commit.

## State machine

If an entity has a status, all transitions go through one module: a table of (from, to, roles allowed, side effects). Test every row, including forbidden ones. Different audiences may need different labels for the same internal state; map them in one place and never leak internal states to roles that must not see them.

## Architecture Decision Records

`docs/03-architecture/decisions/ADR-NNNN-<slug>.md` (template provided). Write one when choosing between real alternatives with a lasting cost: framework, database, auth approach, hosting, sync vs async, a provider interface. Not for choices nobody would question. Status: Proposed, Accepted, Superseded by ADR-NNNN. Never edit an accepted ADR's decision; supersede it.

## Threat model (standard and strict)

`docs/06-security/THREAT_MODEL.md` (template provided). For each trust boundary (browser to API, API to database, API to third parties, file uploads, admin surfaces), walk STRIDE briefly: spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege. Each threat gets a control and the test that proves it. Usual minimum:
- Authentication with sane session or token lifetime; rate limit on login
- Server-side authorization per endpoint, tested with the wrong role and the wrong owner
- Input validation; parameterized queries
- Uploads: extension and MIME allowlist, magic-byte check, size cap, server-generated names, served only through an authorized endpoint
- Secrets in the environment only; secret scanning in CI
- Security headers, CORS allowlist
- Logs carry identifiers, never passwords, tokens or document contents
- If an AI model reads user content: treat its output as untrusted data, validate it against a schema, and never let it change authoritative state

When a control changes, amend the threat model in the same change.

## Testing strategy

`docs/07-testing/TEST_STRATEGY.md`: what each layer covers (unit for domain rules and state transitions, integration for endpoints against a real database, end to end for the critical journey), how to run each, and what CI blocks on. Aim tests at risk, not at a coverage number.
