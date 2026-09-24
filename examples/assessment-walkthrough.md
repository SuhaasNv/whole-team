# Walkthrough: a take-home assessment, scoped and pushed back

A worked example of what whole-team produces in the first hour of a take-home task. The brief, names and numbers are invented for illustration.

## The brief (excerpt)

> Build a clinic appointment platform in **3 days**.
> 1. Patients book, reschedule and cancel appointments.
> 2. Doctors manage availability and see their day.
> 3. Receptionists handle walk-ins and a waiting-room queue.
> 4. Send SMS reminders 24 hours before.
> 5. Admins see reports on no-shows and utilisation.
> Deliverables: repository, README, deployed URL. We evaluate product judgement, code quality, testing and production readiness.

## 1. Brief analysis (docs/01-discovery/BRIEF_ANALYSIS.md, abridged)

| # | Requirement | Where |
|---|-------------|-------|
| B1 | Patients book, reschedule, cancel | 1 |
| B2 | Doctors manage availability, see their day | 2 |
| B3 | Receptionist walk-ins and queue | 3 |
| B4 | SMS reminders 24 h before | 4 |
| B5 | Admin reports | 5 |

**What is evaluated:** judgement, code quality, testing, production readiness. Feature count is not listed.

**Implied:** four roles need authentication and server-side authorization; bookings need conflict rules (no double booking); times need a time-zone decision; SMS needs a provider and a way to test without sending.

**Ambiguities:**

| Text | Reading 1 (cost) | Reading 2 (cost) |
|------|------------------|------------------|
| "manage availability" | weekly recurring hours (4 h) | recurring hours plus exceptions and leave (10 h) |
| "reports" | two counts on one page (3 h) | filterable charts with export (12 h) |

## 2. Capacity math

| | Hours |
|--|------|
| Time box: 3 days × 7 focused hours | 21 |
| Reserve 30% (setup, tests, docs, deploy, buffer) | 6 |
| Available for MUST items | 15 |

| Candidate | Size (h, with tests and docs) |
|-----------|-------------------------------|
| Walking skeleton, auth, roles, deploy | 4 |
| B1 booking loop with conflict rules | 5 |
| B2 availability (recurring hours only) | 4 |
| B3 walk-in queue | 5 |
| B4 SMS reminders (provider behind an interface, mocked) | 3 |
| B5 reports | 3 |
| **Total** | **24** |

24 hours of work against 15 available. Something has to go.

## 3. The pushback message

```
Recommendation: build patient booking (B1) and doctor availability (B2) as one tested, deployed loop,
plus reminders (B4) behind a provider interface with a mock sender. Defer the walk-in queue (B3)
and reports (B5) with a written design for each.

Why: the MUST candidates size at 24 h against 15 h available (table above). B1 and B2 are two halves
of one loop and hold the hardest graded parts: conflict rules, authorization across roles, time zones.
B4 is cheap once booking exists and shows a real integration seam.

What we give up: receptionists and admins get accounts and a placeholder screen, not features.
The role model already includes them, so adding B3 and B5 later is additive.

Alternative: all five at demo quality: no end-to-end tests, no deployment, thin docs.

Decision needed: A) B1 + B2 + B4 (recommended)  B) all five, reduced quality  C) something else
```

The owner answers A. The decision goes into `SCOPE.md`.

## 4. SCOPE.md (abridged)

**Decision in one line:** build patient booking and doctor availability as one tested, deployed loop with mocked SMS reminders; defer the walk-in queue and reports with written designs.

| # | Feature | Source |
|---|---------|--------|
| M1 | Login for patient, doctor, receptionist, admin; role home screens | Implied |
| M2 | Doctor sets weekly recurring hours | B2 (reading 1) |
| M3 | Patient books, reschedules, cancels within available slots; no double booking | B1 |
| M4 | Doctor's day view | B2 |
| M5 | Reminder job 24 h before, `SmsSender` interface, mock sender logs | B4 |
| M6 | Tests: conflict rules, authorization per role, booking journey end to end | Evaluated |
| M7 | CI, deploy, health check, README | Deliverables |

| Deferred | What production would need |
|----------|----------------------------|
| B3 walk-in queue | Queue entity, receptionist screen, live updates, priority rules |
| B5 reports | Read model for no-shows and utilisation, date filters, export |
| Real SMS | Provider account, delivery receipts, opt-out handling |

**Assumptions:** A1 one clinic, one time zone (clinic local time, stored in UTC). A2 availability exceptions (leave, holidays) are out of scope. A3 appointments are 30 minutes.

**Cut order:** reschedule (keep cancel and book again) → doctor's day view polish → reminders.

## 5. Right-sizing in the architecture step

The first draft proposed a separate notification service and a Redis queue for reminders. The right-sizing checklist asked for a requirement that names the need; there was none at one clinic's volume. Result: one FastAPI app, Postgres, a scheduled job inside the app that runs every five minutes. The `SmsSender` interface stays, because it is a real seam (a provider, and a mock in tests).

## 6. Sprint 1 stories

```markdown
### US-000: As a developer, I want a runnable skeleton with a database, health check, CI and one deploy, so that every feature builds on a working base.
- Acceptance criteria:
  - Given a clean clone, when I follow the README, then the app starts and /health returns 200.
- Priority: MUST · Sprint: 1 · Status: Not started
- Depends on: none · Requirements: NFR-001
- Tests: 

### US-003: As a patient, I want to book an open slot, so that I can see a doctor without calling.
- Acceptance criteria:
  - Given a doctor's open slot, when I book it, then it is mine and no longer offered to others.
  - Given two patients booking the same slot at once, when both submit, then exactly one succeeds and the other sees "slot just taken".
  - Given another patient's appointment ID, when I open it, then I get 404.
- Priority: MUST · Sprint: 1 · Status: Not started
- Depends on: US-001, US-002 · Requirements: FR-003, SEC-001
- Tests: 
```

From here the story loop takes over: branch, tests first for the conflict rule, the smallest implementation, the hats pass, an independent review, a local merge, and a one-line status.
