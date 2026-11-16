---
name: coding-kata
description: Create a targeted coding practice exercise (kata) for a developer, with a contract, failing tests, a reference solution and a review rubric. Use when asked to make a coding exercise, practice problem, kata, interview-style drill, or language-learning exercise for a mentee or for yourself.
---

# Coding Kata Generator

Produce a self-contained exercise that practises one skill, in the target language, with
tests the learner runs locally. Tests are the spec.

## Inputs to confirm (ask if missing)

- **Skill under practice:** e.g. error handling, dependency inversion, N+1 removal,
  concurrency, a language idiom, TDD discipline itself.
- **Language / runtime** and whether frameworks are allowed.
- **Level:** junior / mid / senior. Controls hints and the number of hidden tests.
- **Time box:** 30 / 60 / 120 minutes.

## Output layout

```
kata-<slug>/
  README.md          problem, constraints, how to run, what "done" means
  CONTRACT.<ext>     interface/types the learner implements; doc-comments carry pre/post conditions
  tests/             visible tests (fail until implemented), ordered easy → hard
  tests/hidden/      3–5 extra tests the reviewer runs; not shared up front
  solution/          one idiomatic reference solution (never shared before review)
  RUBRIC.md          what a senior reviewer looks for
```

## Design rules

- **One skill per kata.** If the problem needs two new ideas, split it.
- **Contract first.** The learner never designs the public interface; they implement it.
  Design katas are a separate type and say so in the README.
- **Tests escalate:** 1 trivial, 2–3 core, 1–2 edge cases (empty, max, concurrency, bad input),
  1 that only passes with the intended skill applied (e.g. a timing or call-count assertion).
- **Visible tests must be runnable with one command** printed in the README.
- **No trick questions.** Difficulty comes from the skill, not from hidden requirements.
- **Idiomatic to the language**, including its test runner and project layout.

## RUBRIC.md structure

| Dimension | 1 | 3 | 5 |
|-----------|---|---|---|
| Correctness | visible tests fail | visible pass, hidden fail | all pass |
| Skill applied | absent | partial | idiomatic, explained in commit message |
| Tests/TDD | solution only | tests added after | commits show red→green→refactor |
| Readability | needs explanation | mostly clear | reads like the contract |

## Variants

- **Language pickup:** same problem the learner already solved in a known language; rubric
  weights idiom heavily.
- **Refactoring kata:** ship working but tangled code plus green tests; the task is to
  improve structure without breaking tests. Pairs with `code-quality-review`.
- **Instrumentation kata:** add event tracking to a small app against an event contract.
  Pairs with `event-tracking`.
