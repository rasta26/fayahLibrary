---
name: code-quality-review
description: Senior-engineer code quality and maintainability audit of a whole codebase. Use when asked to find dead code, duplicate logic, unused UI components, over-complex implementations, legacy code, redundant queries or API calls, abandoned files, or to reduce technical debt and produce a cleanup plan.
---

# Code Quality & Maintainability Review

Act as a senior software engineer reviewing the entire codebase for maintainability.
Produce findings, not opinions: every item must point at concrete files, symbols or routes.

## Procedure

1. **Map the codebase first.** Identify entry points (main, routes, pages, CLI commands,
   scheduled jobs), the build config, and the dependency manifest. Record the module
   graph before judging anything.
2. **Gather evidence with tools, not memory.** Prefer `grep`/`rg`, the language's own
   tooling (`tsc --noEmit`, `knip`, `depcheck`, `vulture`, `deadcode`, `go vet`,
   `cargo udeps`, IDE unused-symbol reports) and git history (`git log --follow`,
   `git blame`) over reading and guessing. Run the project's tests before and after.
3. **Audit each category** below. Skip a category only if the project cannot contain it.
4. **Classify each finding** and write it in the fixed format in "Output".
5. **Write the cleanup plan** ordered by risk, lowest first, in PR-sized steps.

## Categories to audit

| # | Category | Typical evidence |
|---|----------|------------------|
| 1 | Dead code: functions, files, components, routes, APIs, variables, imports, dependencies | zero call sites; export never imported; route never linked or documented; dependency not imported anywhere |
| 2 | Duplicate logic | near-identical functions, copy-pasted validation, parallel utils |
| 3 | Unused UI components | component never rendered; storybook-only; feature-flag removed |
| 4 | Over-complex implementations | deep nesting, hand-rolled versions of stdlib/framework features, abstractions with one implementer |
| 5 | Legacy code no longer needed | migrations already applied, compat shims for dropped versions, old feature flags |
| 6 | Redundant DB queries / API calls | N+1, same query in loop, refetch of data already in scope, duplicate network calls per render |
| 7 | Abandoned or disconnected files | not reachable from any entry point; last touched years ago; `*.old`, `*.bak`, `_v2` |
| 8 | Technical-debt opportunities | missing tests on hot paths, config duplicated across envs, TODO/FIXME older than 6 months |

## Output

For **each** finding use exactly this block so results can be tracked as issues:

```
### [CATEGORY] <short title>
- Location: <path>:<line> (and other sites)
- Why unnecessary: <evidence; include the command or search that proved it>
- Impact of removal: <LOC removed, bundle/latency/complexity change, who benefits>
- Risk before deletion: <dynamic imports, reflection, public API consumers, external callers, DB triggers, feature flags>
- Confidence: high | medium | low
```

Then a **Cleanup plan**:

1. Group findings into PR-sized steps (one category or one module per PR).
2. Order: zero-risk deletions → consolidations → simplifications → architectural debt.
3. For every step list: pre-checks (tests, grep for dynamic use, telemetry showing zero traffic),
   the change, and the rollback.
4. State what *not* to touch yet and why.

## Rules

- Never delete in the same pass as auditing. The audit is a report; cleanup is separate PRs.
- A finding without evidence is a question, not a finding; list it under "Needs confirmation".
- Prefer removing over refactoring; prefer refactoring over commenting.
- Respect public contracts: anything exported from a package boundary or served over HTTP
  is "medium" risk minimum, and needs usage telemetry or consumer search before removal.
