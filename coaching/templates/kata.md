# Template: Coding practice exercise (kata)

## 1. Purpose
A self-contained exercise that practises one skill, with tests the learner runs locally.
For a mentee (or me when learning a language). Full method: `coding-kata` skill.

## 2. Inputs
- Skill to practise, e.g. error handling, N+1 removal, a language idiom (required)
- Language and runtime; frameworks allowed or not (required)
- Level: junior / mid / senior (if missing, ask)
- Time box: 30 / 60 / 120 minutes (if missing, use 60 and say so)
- Type: standard, language pickup, refactoring or instrumentation (default: standard)
- Optional: the gap from a review's growth notes that this kata targets

## 3. Steps
1. Confirm the inputs. If the problem needs two new ideas, split it into two katas.
2. Write the contract: the interface the learner implements, with pre/post conditions.
3. Write visible tests, easy to hard: 1 trivial, 2–3 core, 1–2 edge cases, 1 that only passes with the skill applied.
4. Write 3–5 hidden tests for the reviewer.
5. Write one idiomatic reference solution.
6. Run the tests: visible tests fail against an empty stub and all tests pass against the solution.
7. Write the rubric and README.

## 4. Output format
```
kata-<slug>/
  README.md        Problem · Constraints · How to run (one command) · Done means · Time box
  CONTRACT.<ext>   interface the learner implements
  tests/           visible tests, easy → hard
  tests/hidden/    3–5 reviewer-only tests
  solution/        reference solution (not shared before review)
  RUBRIC.md        Correctness · Skill applied · Tests/TDD · Readability, each scored 1/3/5
```
README: one page or less, plain language, no trick requirements.

## 5. Finished example
None on file yet. Save the first kata you use with a mentee to `coaching/examples/` and link it here.

## 6. Done check
- [ ] It practises exactly one skill.
- [ ] Visible tests fail against the stub and pass against the solution (actually run).
- [ ] One command, printed in the README, runs the visible tests.
- [ ] There are 3–5 hidden tests and the rubric has all four rows.
- [ ] The reference solution fits inside the time box for the stated level.
