# Rollout and handoff

## When to use this

Before exposing a new workflow to users and before the delivery engineer leaves the engagement.

## Who contributes

Operator, user/team lead, delivery engineer, support owner, and launch approver.

## What good looks like

An operator can stop the rollout, explain incomplete work, recover safely, and support users without relying on the original author.

## Rollout contract

- System and release:
- Audience, eligibility, and exclusions:
- Feature control and who may change it:
- Success signals and guardrails:

| Stage | Audience / duration | Evidence required to enter | Stop condition | Decision owner |
| --- | --- | --- | --- | --- |
| Synthetic replay | | | | |
| Bounded pilot | | | | |
| Expansion | | | | |

## Rollback and recovery

- Disable command or procedure:
- Prior workflow and verification steps:
- In-flight work and committed side effects:
- Reconciliation procedure:
- User notification owner and message:

## Handoff

- Deployment owner and support model:
- Runbook location and exercised recovery case:
- Alerts and escalation contacts:
- Known limitations and unresolved defects:
- Training, user feedback, and bypass reasons:
- Data/configuration ownership and maintenance schedule:

## Acceptance

- Receiving owner:
- Independent runbook exercise and outcome:
- Remaining obligations with owners/dates:
- Handoff accepted on:
- Post-launch review date and evidence:
- Candidate reusable component and proposed maintenance owner:

The [lifecycle guide](../docs/foundations/fde-lifecycle.md) places handoff and productization after operational evidence.
