---
search:
  exclude: true
---
# Stage 3: constraints, design, and production plan

Open only after saving the Stage 2 scope agreement.

## New constraints

The sponsor proposes a two-week pilot with eight US dispatch operators on one shift. Write access is unavailable. Hazardous and high-value shipments require supervisor review. The transport API permits 60 requests per minute for the **whole pilot credential**, including retries and other consumers. Warehouse CSV exports arrive daily at 06:00 US Eastern; there is no sanctioned browser automation. Security will not approve cross-region data transfer. The operations lead can provide a daily 20-case review sample, but cannot label thousands of examples before launch.

The initial queue contains 420 synthetic exceptions; the team has not established how many are actionable. The pilot must show data timestamps and retain a route back to manual investigation. Staff must be able to disagree and record why.

## Design task

Create a diagram with trust boundaries and sources of truth. Compare options in a decision table: batch versus live reads, caching with explicit age versus no cache, manual review versus automation, deterministic rules versus RAG/LLM assistance, and whether MCP actually adds value. For each, state latency/freshness, rate-budget, implementation, failure, and operational consequences. Neither using an LLM nor using MCP is required to receive strong evidence marks.

Describe normalization of source codes and handling of unknown codes. Include schema validation, null ETA handling, freshness thresholds, region checks, retry budgets, and concurrency across eight operators. Count retries in the rate budget. Specify behavior when evidence is missing; distinguish "unknown" from "on time." Explain where supervisor approval would belong if a future write were authorized.

Create an evaluation plan with ordinary, stale, missing, conflicting, regional, and supervisor-only cases. Separate classification quality, unsupported recommendation rate, investigation time, and user adoption. Propose thresholds and a sampling method, identifying assumptions rather than claiming measured results.

## Stakeholder change request

> "Can it automatically update shipment status after making a recommendation? It would save another step."

Record **accept, defer, redesign, or reject**, with scope, authority, idempotency, audit, rollback, user impact, and launch-date consequences. Write a short response to the sponsor. If you propose a later approved-write design, explain why the current access constraint still blocks it. Do not confuse a model recommendation with permission.

## Production task

Complete the [readiness checklist](../../templates/production-readiness-checklist.md) with Ready, Not Ready, and Not Applicable statuses. State a conditional go/no-go decision: eligible users/cases, excluded capabilities, monitoring, stop conditions, rollback, named owner roles, and review date. A pilot is not exempt from ownership.

Describe what runs synchronously and what would need persisted checkpoints if approval or an external dependency took hours. Discuss the need without implementing a workflow engine.

Save your design, one ADR, scope-change response, evaluation plan, and readiness record. Then open [Stage 4: incident evidence](04-incident.md). Attempt the exercise before opening the reference solution.
