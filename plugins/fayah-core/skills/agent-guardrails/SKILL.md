---
name: agent-guardrails
description: "Workflow for putting five control patterns around an LLM agent system: adaptive feedback loops, corrective action, human-in-the-loop approval, emergency stop, and input/output guards. Use when building or reviewing an agent, a supervisor/worker setup, or any feature where model output or tool calls reach users, money, or production systems."
---

# Agent Guardrails Workflow

Five patterns, one pipeline. Each pattern is a contract with a testable pass/fail rule, so
it is specified, tested and implemented like any other requirement (see `spec-first-tdd`).

```
User ─▶ [05 Input guard] ─▶ Supervisor ─▶ Workers ─▶ [02 Rule check] ─▶ [03 Risk gate] ─▶ Tools
             │                  ▲  │                     │ correction        │ high risk
             │                  │  └── [01 Score + learn]◀┘                   ▼
             │                  │                                        Human approve/edit
             ▼                  └──────────── [04 Watchdog: circuit breaker / kill switch]
      Safe refusal + audit ◀── [05 Output guard] ◀── draft response ─────────────▶ Response
```

| # | Pattern | Tag | Guarantee |
|---|---------|-----|-----------|
| 01 | Adaptive feedback loop | LEARN | Every output is scored; the next instruction uses the score |
| 02 | Corrective action | FIX | A broken rule reroutes the task mid-run, before it lands |
| 03 | Human in the loop | APPROVE | Risky actions never run unreviewed |
| 04 | Emergency stop | HALT | A hard limit crossed cuts the agent off and pages a human |
| 05 | Input & output guards | SCREEN | Nothing risky goes in, nothing unsafe comes out |

## Phase 1: Spec

Write `docs/specs/agent-guardrails.md` with these requirements, adjusting numbers to the
system. Every requirement must be machine-decidable.

| Rn | Requirement (defaults) |
|----|------------------------|
| R1 | Every worker output receives a score in [0,1] from a scorer that is not the worker itself |
| R2 | The supervisor's next instruction to a worker includes the previous score and its reasons |
| R3 | Scores and instruction versions are persisted, so a regression in mean score is detectable |
| R4 | Every worker result is checked against the guidelines before it is accepted |
| R5 | A rule violation reroutes the task to a corrected path within the same run; the violating result is never forwarded |
| R6 | A worker that violates the same rule 3 times in a run is removed from that run |
| R7 | Every proposed action gets a risk level (low / high) from a declared policy, not from the model's own opinion |
| R8 | High-risk actions (money movement, deletes, external sends, prod writes, above thresholds) are held as drafts until a human approves or edits them |
| R9 | Low-risk actions run directly and are logged |
| R10 | A watchdog enforces hard limits per run: tool calls, spend, wall time, error rate, calls to any one live tool |
| R11 | Crossing a limit opens the circuit breaker: live-tool credentials for that run are revoked before the next call |
| R12 | A kill switch stops all runs of the agent within a stated time and pages on-call |
| R13 | Input guard checks every user input for instruction-override attempts, redacts PII, and enforces topic policy before the model sees it |
| R14 | Input that fails the guard returns a safe refusal and writes an audit entry; the model is never called |
| R15 | Output guard checks format, toxicity + PII, and groundedness against retrieved sources |
| R16 | Failed output is regenerated with the guard's feedback, at most 2 times; then safe refusal + audit entry |

Non-goals to state explicitly: what the guards do not attempt (e.g. no semantic fact-checking
beyond retrieved sources), and which actions are out of scope for automation entirely.

## Phase 2: Contracts

One interface per pattern, no implementation yet. Pre/postconditions in doc-comments.

```ts
// 01 LEARN
interface Scorer { score(task: Task, output: Output): { value: number; reasons: string[] } }
  // post: 0 <= value <= 1; reasons non-empty when value < passThreshold

// 02 FIX
interface RuleChecker { check(result: WorkerResult, guidelines: Rule[]): Violation[] }
interface Router { correct(task: Task, violations: Violation[]): CorrectedTask }
  // post: corrected task names the violated rules; original result is discarded

// 03 APPROVE
interface RiskPolicy { classify(action: Action): "low" | "high" }   // pure, deterministic
interface ApprovalQueue {
  submit(draft: Action): DraftId
  decide(id: DraftId, by: HumanId, decision: "approve" | "edit" | "reject", edited?: Action): void
}
  // invariant: no "high" action reaches a Tool without a decide(approve|edit) record

// 04 HALT
interface Watchdog { observe(event: AgentEvent): void; tripped(runId): Trip | null }
interface CircuitBreaker { open(runId, reason): void }  // post: credentials revoked
interface KillSwitch { stopAll(agentId, reason): void } // post: on-call paged, runs halted

// 05 SCREEN
interface InputGuard  { check(input: string): { pass: boolean; sanitized: string; reasons: string[] } }
interface OutputGuard { check(out: Output, sources: Source[]): { pass: boolean; feedback: string[] } }
interface AuditLog    { write(entry: AuditEntry): void }        // append-only
```

Configuration is part of the contract and lives in one file, e.g. `guardrails.config.yaml`:

```yaml
feedback:   { pass_threshold: 0.7 }
correction: { max_violations_per_worker: 3 }
approval:
  high_risk: [payments.*, *.delete, email.send_external, prod.write]
  amount_threshold: 500          # currency units; above → high
limits:     { tool_calls: 50, spend_usd: 5, wall_seconds: 300, error_rate: 0.3, per_tool_calls: 10 }
guards:     { output_max_retries: 2 }
```

## Phase 3: TDD, one requirement at a time

For each Rn: write a failing test against the contract, implement the minimum, refactor, next.
The tests that prove the guarantees:

| Pattern | Must-have tests |
|---------|-----------------|
| 01 | Scorer bounds; low score produces reasons; next instruction contains prior score; persisted history |
| 02 | Violating result never reaches the caller; corrected task cites the rule; 3rd violation evicts worker |
| 03 | Table-driven `RiskPolicy` cases (each pattern in `high_risk`, threshold ±1); high action blocked with no approval; edited action runs the edited version; reject runs nothing |
| 04 | Each limit trips at exactly N+1; tool call after trip fails for revoked credentials; kill switch halts a running loop and calls the pager stub |
| 05 | Instruction-override, PII and off-topic fixtures refused without calling the model (assert model mock called 0 times); output failing twice then passing is returned; failing 3 times returns safe refusal and 1 audit entry |

Keep a red-team fixture file (`tests/fixtures/guardrails/`) of bad inputs and bad outputs and
grow it with every incident.

## Phase 4: Orchestrate

With `manager-orchestration`, split the work into waves; each pattern is independent once the
contracts exist:

- **Wave 0:** contracts + config schema + audit log (one task).
- **Wave 1 (parallel):** 05 input guard, 05 output guard, 03 risk policy, 04 watchdog, 01 scorer, 02 rule checker. Back end only.
- **Wave 2:** wire into the agent loop; approval UI as a separate front-end task against `ApprovalQueue`.
- **Wave 3:** end-to-end tests walking the full pipeline diagram above.

## Phase 5: Observe

Wire into `event-tracking` so the guardrails are visible:

- `guard.input.refused`, `guard.output.regenerated`, `guard.output.refused` (reason tags only, never raw PII)
- `approval.requested`, `approval.decided` (+ time to decision)
- `watchdog.tripped`, `killswitch.fired` → alerting / on-call
- `score.recorded` → dashboard of mean score per instruction version

## Review checklist (for existing agents)

- [ ] Is any model output shown to a user without an output guard?
- [ ] Can any tool with side effects run without a risk classification?
- [ ] Is the risk policy deterministic code, or is the model deciding its own risk?
- [ ] Are hard limits enforced outside the agent process, so a stuck agent can't skip them?
- [ ] Does regeneration have a cap? Is there a safe refusal at the end of it?
- [ ] Is every refusal, trip and approval in an append-only audit log?
- [ ] Is the scorer independent of the worker it scores?
