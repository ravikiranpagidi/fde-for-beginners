# Production readiness checklist

## When to use this

Before a pilot or production rollout, and after a material change to data, permissions, or dependencies.

## Who contributes

Delivery engineer, operator, security/data owner, domain reviewer, and launch decision owner.

## What good looks like

Every row has evidence and an owner. Unknowns are Not ready. Not applicable requires a reason; it is not a shortcut around a blocker.

## Review record

- System, revision, environment, and date:
- Intended audience / eligible cases:
- Launch owner:
- Reviewers:

Use statuses: **Ready**, **Not ready**, **Not applicable**.

| Area | Check | Status | Evidence / reason | Owner / due date |
| --- | --- | --- | --- | --- |
| Functionality | Ordinary and exception paths meet acceptance criteria | | | |
| Security | Inputs and outputs validated; untrusted content cannot grant authority | | | |
| Authorization | Denial tests cover roles, tenants, and tool actions | | | |
| Secrets | No committed/logged credentials; rotation owned | | | |
| Data | Sensitivity, freshness, retention, access, and deletion reviewed | | | |
| Reliability | Timeouts, bounded retries, fallback, and recovery tested | | | |
| Idempotency | Repeated and uncertain writes cannot duplicate effects | | | |
| Rate limits | Budgets and exhaustion behavior tested | | | |
| Observability | Redacted events, metrics, request IDs, and actionable alerts exist | | | |
| Evaluation | Versioned cases and launch thresholds reviewed | | | |
| Rollback | Disable/restore rehearsed; side effects reconciled | | | |
| Deployment | Configuration, release approval, and version recorded | | | |
| Support | Operator, support hours, escalation, and runbook assigned | | | |
| Documentation | Someone else followed the runbook successfully | | | |
| Launch ownership | Blockers, accepted risks, expiry, and decision recorded | | | |

## Decision

- Launch / narrow scope / defer:
- Blocking evidence:
- Accepted risks, approvers, and expiry:
- Restart or expansion conditions:
- Next review:

The [production guide](../docs/field/production-reality.md) explains why a pilot still needs operational ownership.
