---
description: Add or review the five agent guardrail patterns (feedback loop, corrective action, human approval, emergency stop, input/output guards) for an agent system.
---

Follow the `agent-guardrails` skill for: $ARGUMENTS.

If the target agent already exists, start with the skill's review checklist and report which of
the five patterns are missing or weak. Then write the spec (Phase 1) and contracts (Phase 2),
list open questions, and stop. Implementation runs through `/orchestrate` once the spec has no
open questions.
