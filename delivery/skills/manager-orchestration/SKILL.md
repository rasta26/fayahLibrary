---
name: manager-orchestration
description: Run a feature as a manager agent coordinating small, self-contained sub-agent tasks that integrate continuously into one shared branch. Use when a task is large enough to split, when asked to use sub-agents or parallel agents, or when asked to coordinate front-end and back-end work.
---

# Manager / Sub-agent Orchestration

One manager plans and integrates. Sub-agents each own one small, contract-backed task.
Everything lands on the same shared branch; conflicts are fixed by the sub-agent before merge.

## Manager responsibilities

1. **Read the spec and contracts** (see `spec-first-tdd`). If they don't exist, the first
   sub-agent task is to write them; nothing else starts until the spec has no open questions.
2. **Decompose** into tasks that satisfy all of:
   - one requirement (Rn) or one contract boundary each
   - completable in under ~200 changed lines
   - owns its own files; two tasks never edit the same file in the same wave
   - tagged `backend`, `frontend`, `contract`, `test`, or `infra`; front-end and back-end
     tasks are always separate tasks
3. **Order into waves.** Wave 0: contracts and shared schema. Wave 1+: back-end and front-end
   tasks in parallel against the contract. Last wave: integration tests and docs.
4. **Dispatch** each task with the brief below. Use the `Agent` tool; one agent per task;
   run a wave's tasks in parallel.
5. **Integrate** after each task returns: verify tests pass on the shared branch, verify
   the diff touched only the files it owned, then move on. Never fix a sub-agent's
   conflict yourself; send it back with the conflict description.
6. **Report** at the end: requirements covered, tests added, what was deferred, risks.

## Sub-agent brief (send verbatim, filled in)

```
Task: <id> — <title>
Requirement: Rn — <text from spec>
Contract: <path to interface/schema this must satisfy>
Owns files: <explicit list; create new files only under these paths>
Do not touch: <files other tasks own>
Branch: <shared integration branch>; rebase on its head before you finish.

Procedure (TDD, non-negotiable):
1. Write a failing test for Rn against the contract. Run it; confirm it fails.
2. Implement the minimum to pass.
3. Refactor; keep green.
4. Rebase onto <branch>. If there is a conflict, resolve it, rerun the full test suite.
5. Commit: "feat(<area>): Rn <title>". Return: files changed, tests added, anything deferred.

Stop and report instead of guessing if the contract is ambiguous or the requirement is untestable.
```

## Integration rules (continuous integration)

- The shared branch is always green. A red merge is reverted immediately, not patched.
- Merge order within a wave is arrival order; later arrivals rebase.
- A PR with a conflict is returned to its author (the sub-agent). The manager never resolves
  conflicts in someone else's code: the sub-agent has the context, the manager does not.
- Each merge runs: unit + contract tests of both tiers. Acceptance tests run at wave end.

## Anti-patterns to refuse

- One sub-agent doing "the whole backend".
- Front-end task that imports back-end internals instead of the contract/client.
- Tasks defined by file ("fix utils.ts") instead of by requirement.
- Manager editing code directly to "save a round trip". Manager edits only spec, contracts
  and the task board.

## Task board

Keep the board in the conversation task list (TaskCreate/TaskUpdate) or `docs/specs/<feature>.board.md`:

| id | Rn | tier | owner files | status | wave |
