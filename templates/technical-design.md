# Technical design

## When to use this

When a useful slice is agreed and integration or failure choices need review.

## Who contributes

Delivery engineer, dependency owners, operator, domain reviewer, and security/data owners.

## What good looks like

A reviewer can locate the authoritative system, trust boundary, failure behavior, and operator without a narrated presentation.

## Context and scope

- Problem and acceptance evidence:
- Requirements and constraints:
- Non-goals:
- Smallest useful vertical slice:

## Architecture and data flow

Insert a small Mermaid diagram showing users, boundaries, dependencies, and human decisions. Name each system of record. Distinguish reads, writes, and derived data.

| API / integration | Contract / version owner | Identity and authorization | Deadline / rate limit | Failure behavior |
| --- | --- | --- | --- | --- |
| | | | | |

## Data and security

- Sensitive fields, allowed uses, retention, and redaction:
- Validation at each boundary:
- Authorization before retrieval or tools:
- Approval and idempotency for writes:
- Untrusted input, retrieved content, and output handling:

## Operation and evaluation

| Failure mode | Detection | Containment / fallback | Recovery owner |
| --- | --- | --- | --- |
| | | | |

- Logs, metrics, trace/request IDs, and alert routing:
- Evaluation cases, baseline, thresholds, and regression command:
- Rollout stages and feature control:
- Rollback and reconciliation of side effects:
- Deployment and support owners:
- Open questions, owners, and review dates:

Reference meaningful tradeoffs in an [ADR](architecture-decision-record.md). See the [design guide](../docs/field/solution-design.md) for a worked example.
