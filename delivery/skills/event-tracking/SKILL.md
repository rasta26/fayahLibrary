---
name: event-tracking
description: Add product analytics and operational telemetry to an application. Use when asked to add event tracking, analytics, instrumentation, monitoring or alerting for onboarding funnels, error and crash logging, feature usage, payment-funnel abandonment, DAU/MAU, API latency and slow queries, retention, background jobs, or uptime.
---

# Event Tracking & Telemetry

Instrument an application against a written event contract. Specs first: the event
schema is agreed and tested before any emitter is written.

## Step 1: Event contract (write this before code)

Create `docs/analytics/events.md` (or the project's equivalent) with one table row per
event. Every event has: `name` (snake_case, `<domain>_<object>_<action>`), `when it fires`,
`required properties`, `optional properties`, `PII class`, `owner`.

Standard envelope on every event:

```json
{ "event": "string", "ts": "ISO-8601", "user_id": "hashed|null", "anonymous_id": "uuid",
  "session_id": "uuid", "app_version": "semver", "platform": "web|ios|android|server",
  "properties": {} }
```

## Step 2: Required event families

| Family | Minimum events | Key properties |
|--------|---------------|----------------|
| **Onboarding funnel** | `onboarding_started`, `onboarding_step_completed`, `onboarding_completed`, `onboarding_abandoned` | `step_name`, `step_index`, `total_steps`, `elapsed_ms` |
| **Error & crash logging** | `error_occurred`, `crash_detected`, `api_error` | `error_type`, `message` (scrubbed), `stack_hash`, `handled`, `route`, `severity` |
| **Feature usage** | `feature_used` | `feature`, `action`, `source` (nav, shortcut, deep link) |
| **Payment funnel abandonment** | `checkout_started`, `checkout_step_completed`, `payment_submitted`, `payment_succeeded`, `payment_failed`, `checkout_abandoned` | `plan`, `amount`, `currency`, `step`, `failure_code` |
| **DAU / MAU** | `session_started`, `session_ended` | derive DAU/MAU from distinct `user_id` per day/30 days; never a separate "dau" event |
| **API latency & slow queries** | `api_request_completed`, `db_query_slow` | `route`, `method`, `status`, `duration_ms`, `query_hash`, `rows`; threshold for slow is configurable, default 500 ms |
| **Retention** | derived from `session_started` cohorts (D1/D7/D30) | document the cohort query, do not add events |
| **Background job monitoring** | `job_started`, `job_succeeded`, `job_failed`, `job_retried` | `job_name`, `queue`, `attempt`, `duration_ms`, `error_type` |
| **Uptime alerts** | `healthcheck_failed`, `healthcheck_recovered` (emitted by the prober, not the app) | `endpoint`, `region`, `latency_ms`, `consecutive_failures` |

## Step 3: Architecture (isolate front end and back end)

- One **`analytics` module per tier** exposing a single `track(event, properties)` function
  behind an interface. Business code never imports the vendor SDK directly.
- **Contract shared, implementations separate.** Put the event names and property types in a
  shared schema (TypeScript types, JSON Schema, protobuf, or a Python `TypedDict` module).
  Front end and back end each validate against it in tests.
- **Server is the source of truth** for payment, job and latency events; the client owns
  onboarding and feature-usage UI events. Do not double-count.
- **Privacy:** hash user ids, strip emails/tokens/URLs with query strings from error messages,
  add a `consent` gate on the client before any network send.
- **Transport:** batch, retry with backoff, drop on persistent failure; telemetry must never
  break the product path. Wrap `track` so it cannot throw.

## Step 4: TDD per event family

For each row of the contract, in order:

1. Write a test asserting the event is emitted with the exact required properties
   (use a fake transport that records calls).
2. Implement the emitter.
3. Add a schema-validation test that rejects an event with a missing required property.
4. Move to the next row. Do not instrument two families in one PR.

## Step 5: Dashboards and alerts

Deliver, as config-as-code where the vendor supports it:
- Funnel charts for onboarding and checkout with abandonment % per step.
- Error rate and crash-free-sessions %, alert on 2x baseline over 10 min.
- p50/p95/p99 latency per route; alert on p95 > SLO for 5 min.
- Job failure rate and queue age; alert on failures > 1 % or age > 10 min.
- DAU/MAU ratio and D1/D7/D30 retention cohorts.
- Uptime probe from at least two regions; page on 3 consecutive failures.

## Output checklist

- [ ] `events.md` contract reviewed and merged first
- [ ] shared schema module with validation test
- [ ] per-tier `analytics` module with fake transport for tests
- [ ] one PR per event family, each with failing-then-passing tests
- [ ] dashboards/alerts committed as code
- [ ] privacy review: hashed ids, scrubbed messages, consent gate
