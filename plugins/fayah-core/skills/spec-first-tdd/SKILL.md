---
name: spec-first-tdd
description: "Specs-first, design-by-contract, test-driven implementation workflow. Use when starting any feature or fix: write the spec and contracts first, isolate front-end and back-end implementations behind the contract, then for each requirement write a failing test, implement, and move to the next."
---

# Spec First, Design by Contract, TDD

Nothing is implemented until there is a written requirement, a contract that encodes it,
and a failing test against that contract.

## Phase 1: Spec

Write `docs/specs/<feature>.md` before touching code:

```
# <Feature>
## Problem            - one paragraph, user-visible
## Requirements       - numbered R1..Rn, each testable, each a single sentence
## Non-goals          - what this does not do
## Contracts          - link to the interface files created in Phase 2
## Acceptance         - for each Rn: Given / When / Then
## Open questions     - must be empty before implementation starts
```

A requirement is testable only if a machine can decide pass/fail. "Fast" is not a
requirement; "p95 < 300 ms for GET /items" is.

## Phase 2: Contracts (design by contract)

For each boundary the feature crosses, write the contract as code, with no implementation:

- **API boundary:** OpenAPI/GraphQL schema, or a typed request/response pair, plus
  preconditions (input validation), postconditions (what the response guarantees) and
  invariants (what never changes, e.g. balances sum to zero).
- **Module boundary:** interface/protocol/abstract class with doc-comments stating pre/post
  conditions. Add runtime assertions for preconditions in debug builds.
- **Data boundary:** schema migration plus constraints (NOT NULL, CHECK, FK) that enforce the
  invariants in the database, not only in code.

Front end and back end are implemented **against the contract, never against each other**.
The front end codes to a generated client or a mock server derived from the contract;
the back end codes to the contract tests. Neither waits for the other.

## Phase 3: TDD loop, one requirement at a time

For R1, then R2, …:

1. **Red:** write one test that encodes Rn's acceptance criterion against the contract.
   Run it. It must fail for the right reason (assertion, not compile error from a typo).
2. **Green:** write the smallest implementation that passes. No speculative generality.
3. **Refactor:** remove duplication introduced in Green. Tests stay green.
4. **Commit:** `feat(<area>): Rn <requirement title>` with the test and implementation together.
5. Next requirement. Never start Rn+1 with Rn red.

Rules:
- A test that passed before you wrote code is not a test; delete or fix it.
- Mock only at contract boundaries. Never mock the unit under test's own internals.
- Contract tests (consumer-driven or schema tests) run in both front-end and back-end suites.

## Phase 4: Integration

- Merge to the shared integration branch at least once per requirement.
- Rebase on the branch head before opening the PR; a conflicting PR is the author's to fix
  before merge, never the reviewer's.
- CI must run: unit, contract, and the acceptance tests from the spec. Red CI blocks merge.

## Definition of done per requirement

- [ ] Rn appears in the spec with Given/When/Then
- [ ] contract updated (if the boundary changed) and its schema test passes
- [ ] failing test written first, now green
- [ ] no implementation detail beyond what Rn needs
- [ ] merged into the shared branch with CI green
