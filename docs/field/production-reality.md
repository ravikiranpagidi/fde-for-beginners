# Production reality and readiness

The relevant question is not "did the demo work?" It is "what evidence supports this rollout, and who owns the remaining risks?" Northstar's representative may use your view while speaking to a customer. A plausible but stale answer can be worse than an explicit unavailable state.

## Different stages, different claims

| Stage | What it can establish | What it does not establish |
| --- | --- | --- |
| Demo | A selected path can illustrate the idea | Reliability, representative quality, or safe operations |
| Proof of concept | A named technical uncertainty can be reduced | Workflow value or ownership |
| Pilot | A bounded population can test workflow value with safeguards | All-user readiness or rare-event safety |
| Production | A defined service has operational and acceptance evidence | Unlimited load or every new use case |
| Scaled production | Capacity and multi-team operations meet expanded demand | Permission to skip evaluation on changes |

A pilot still needs authorization, support, and rollback. Calling it experimental does not make customer impact disappear.

## Reusable readiness review

Copy the table into your engagement notes. For each row, record evidence location, owner, status (`verified`, `blocked`, or `accepted risk`), and review date. Blank rows are unknowns, not passes. Accepted risks require a named accountable approver and expiry; they cannot override an authorization boundary.

| Area | Evidence to request |
| --- | --- |
| Authentication | Invalid and expired credentials are rejected; credential owner is known |
| Authorization | Cross-region and cross-role reads/writes fail in tests; checks occur before retrieval and tool execution |
| Secrets | Credentials stay out of source, logs, fixtures, and client responses; rotation procedure is rehearsed |
| Data sensitivity | Allowed fields, retention, deletion, and log redaction are reviewed by data owner |
| Input/output validation | Missing, malformed, oversized, and incompatible fields have explicit behavior |
| Timeouts | Every remote call and overall workflow have bounded deadlines |
| Retries/rate limits | Retryable errors are defined; backoff is bounded; retry storms and exhaustion are tested |
| Idempotency | Duplicate or uncertain writes reconcile to one intended action |
| Approval | Unapproved writes fail; approval is bound to the intended action and cannot bypass authorization |
| Retrieval/model quality | Versioned representative cases cover wrong context, stale evidence, unsupported questions, and abstention |
| Monitoring | Success, failure, latency, saturation, and quality regressions have useful signals and owners |
| Logs/tracing | A request ID connects dependency calls and decisions without leaking sensitive data |
| Fallback | Users can return to the prior workflow; partial success is explained |
| Rollback | Operator can disable the new path and verify restored behavior; write side effects are accounted for |
| Deployment | Version, configuration, release approver, and operator are recorded |
| Support | Escalation route, support hours, and incident decision owner are agreed |
| Documentation | Someone other than the author can follow the runbook |
| Launch criteria | Thresholds and blockers were agreed before evaluation; sign-off references evidence |
| Adoption/handoff | Users know limitations; ownership and feedback review continue after launch |

This is a review aid, not a certification or a replacement for customer-specific requirements. The separate field-template set is planned for Phase 2.

## Observability that answers questions

A useful event includes a correlation ID, operation, outcome category, elapsed time, dependency, and retry count. Avoid raw customer messages, credentials, or full model prompts in routine logs. Metrics summarize patterns; logs describe events; traces connect work across services. High-cardinality customer identifiers generally belong in controlled diagnostic records, not metric labels.

For Northstar, distinguish "order missing," "order service unavailable," "access denied," and "policy unsupported." One generic error counter hides different responses. Decide who receives alerts and what action they can take. An alert with no owner or runbook adds noise.

## Safe rollout and rollback

Begin with synthetic replay, then a bounded read-only pilot if access and evidence allow it. Define eligible users and cases, observation duration, stop conditions, and the person authorized to stop rollout. Expand only after reviewing quality, workflow value, failures, and bypass reasons together.

Rehearse rollback before launch: disable the feature, confirm the previous workflow still works, and explain to users which drafts or actions are incomplete. A code rollback does not undo a ticket, refund, or external notification. Such actions require reconciliation or a compensating operation with its own authorization.

## Failure exercise

During a Northstar pilot, the order API begins returning 429 responses and a policy record loses its effective date. Drafts are still being generated from cached context.

Write a short incident note answering: which output should stop, which read-only capability can remain, what sanitized evidence is needed, who decides rollout status, and how users regain a safe workflow? Distinguish containment from permanent repair. Preserve a request timeline, a customer update, and regression cases.

Review guidance: stale policy should not silently remain authoritative. Bound retries and respect rate-limit signals; do not convert failures into empty records. Pause affected recommendations, preserve safe policy browsing only if freshness is known, and restore the manual process. Investigate the contract change and rate-limit behavior before restarting.

## FDE Decision

Launch with a known defect or delay? Classify its consequence, exposure, detectability, reversibility, and workaround. An infrequent cosmetic issue differs from unobservable cross-region data leakage. A narrow launch may be reasonable if the risk is bounded and explicitly accepted; missing authorization or an unsafe write path blocks launch.

## Production Reality

Operations continue after handoff. Review repeat incidents and ask what was customer-specific, what repeated, and what belongs in documentation, a library, a platform, or the product. Give each proposed reusable component a consumer, a contract, and an owner. Otherwise the "shared" code becomes another unsupported dependency.

Use the [progress tracker](../learning-paths/progress-tracker.md) to retain the review and unresolved blockers.
