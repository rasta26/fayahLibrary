---
description: Add event tracking against a written event contract, spec-first and TDD, one event family per PR.
---

Use the `event-tracking` skill. Families to cover: $ARGUMENTS (all nine if empty: onboarding funnel,
error & crash logging, feature usage, payment funnel abandonment, DAU/MAU, API latency & slow queries,
retention, background job monitoring, uptime alerts). Start by writing the event contract and stop for
review before implementing.
