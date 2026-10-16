---
search:
  exclude: true
---
# Atlas reference: one defensible approach

**Spoiler warning: attempt all five stages first.** Return to the [learner entry](README.md) if you have not saved discovery, scope, design, incident, communication, handoff, and productization artifacts. This is a defensible approach, not a uniquely correct solution. Assess your evidence with the [field rubric](../../docs/learning-paths/field-readiness-rubric.md).

## Discovery and scope

Prioritize questions that can stop or reshape delivery: who closes an exception, which source owns state and ETA, what actions are permitted, which data must remain regional, what makes a case urgent, how conflicts are resolved, and who operates a failure. Then ask about baseline queue quality, investigation time, API budgets, export freshness, code mappings, pilot users, quality reviewers, and rollout decisions. A ranked twelve-question set with decision owners is stronger than exhaustive stack questions.

A reasonable problem statement: US dispatch operators need a trustworthy evidence packet for ordinary shipment exceptions because manual investigation crosses sources with different authority and freshness. Test whether an investigation aid reduces median time on matched eligible cases without increasing incorrect recommendations or hiding missing data. Count actionable cases separately from stale queue entries. The six observed cases cannot establish a reliable baseline.

Scope the first pilot to read-only US investigation, visible evidence age, and operator decisions. Exclude hazardous/high-value decisions, cross-region data, warehouse scraping, and shipment writes. Supervisor cases can be recognized and routed without deciding them. A process-only improvement to queue deduplication may produce enough benefit to defer an AI component entirely.

## Design and alternatives

Normalize approved exports and live reads into typed evidence records with source identity, timestamp, schema version, and known/unknown fields. Keep regional boundaries before any retrieval or model call. Budget all transport requests across workers and consumers. Cache only with visible age and a rule for when evidence becomes unusable. Deterministic routing handles known codes and supervisor classes; optional retrieval explains policy, with citations and abstention when authority conflicts. Model text cannot override routing or authorization.

Tradeoff: live reads improve freshness but consume a shared budget; batch reads reduce load but can miss new exceptions. A hybrid is reasonable if age and unavailable behavior are explicit. A fully manual pilot with a structured evidence worksheet is an alternative when access or baseline quality is insufficient. Revisit live versus batch after measuring actual freshness requirements and shared credential usage. Revisit semantic retrieval only after lexical failure cases demonstrate a need.

MCP is optional for a small application with fixed read adapters. It becomes useful when multiple approved hosts need the same tools, but does not provide business authorization by itself. No current write access means the sponsor's status-update request is deferred, with a possible later design requiring verified identity, supervisor authority, payload-bound approval, upstream idempotency, and reconciliation. A better model does not remove these conditions.

A conditional pilot decision would require contract validation, source-age display, rate budget enforcement, an identified support owner, baseline measurement, and a rehearsed manual fallback. Use proposed thresholds such as zero unauthorized effects, zero cross-region disclosure, all missing-evidence cases visibly unavailable, and weekly operator review of the labeled sample. Investigation-time improvements require measured comparison, not invented percentages.

## Incident: detection

Missing normalized ETA rose from 2/80 to 31/90 and disagreements from 1/20 to 7/20 while process uptime stayed at 100%. These are evidence-quality symptoms, not proof of one root cause. Trace a41 shows a retry one second after a 20-second Retry-After and a 47-minute cache fallback. Trace a42 has a successful HTTP response but a field absent from the normalized object. The current payload supplies `estimated_arrival`; the previous contract used `eta`. Trace a43 also demonstrates a genuinely null ETA that a rename fix cannot fill.

## Incident: containment

Pause automated recommendations for affected evidence paths and show "investigation unavailable; use manual process" with timestamps. Preserve authorized read-only evidence if provenance, region, and age are trustworthy. Fail closed on regional access, supervisor authority, unsupported classification, and consequential decisions; do not equate degraded availability with permission to guess. Throttle or pause nonessential fetches and honor the provider's retry interval. Retain deployment versions, request IDs, affected snapshots, and operator reports. Ask supervisors to identify actions already taken from affected recommendations.

Notify the technical lead, operations sponsor, transport owner, on-call operator, and supervisors. Security/data owners should be consulted if investigation finds a boundary issue; the packet does not establish a data breach. Do not claim all shipments or all operators were affected.

## Incident: diagnosis

The packet supports multiple hypotheses: concurrency and retry behavior exceeded a shared request budget; an adapter failed to map a renamed field; stale fallback obscured missing information; rules/code normalization produced inconsistent classifications. Test them separately. Reproduce a41 with captured Retry-After values and count all attempts. Validate both payload versions against the adapter. Replay EX7 and DLY mappings under r2 and r3 with identical evidence, checking intended semantics with the domain owner. Inspect whether missing ETA defaults to a known state. Compare fallback age with the agreed policy.

The field rename is visible, but its exact rollout extent, operator impact, and the cause of different recommendations still require verification. Contributing factors include incomplete contract fixtures, a shared-budget blind spot, insufficient unknown-state handling, and monitoring limited to process availability. Do not reduce the incident to "the model hallucinated."

## Incident: recovery

Rollback may reduce concurrency or revert problematic rules, but cannot undo the provider contract change or past manual actions. A targeted adapter fix should explicitly support approved contract versions, reject unknown schemas, and preserve null as unknown. Re-enable a small reviewed cohort after replaying both versions, null ETA, rate-limit exhaustion, stale cache, ambiguous codes, and supervisor-only cases. Confirm budget compliance over a full relevant window and compare recommendations with supervisor labels. Reconcile known operator actions before claiming resolution. Keep rollback and manual fallback available.

## Incident: prevention

Add contract-version fixtures, a null/absent distinction, consumer-wide rate budgeting, bounded retries honoring Retry-After, visible freshness, code-mapping tests owned by operations, and an unknown outcome. Monitor missing evidence, stale fallback fraction, rate-budget consumption, disagreement rate, and manual-review volume, with denominators and named alert owners. Make provider bulletins and source changes evaluation triggers. Revisit caching thresholds when measured workflow tolerance changes.

## Example audience updates

**Technical lead, 09:25 UTC:** We have paused recommendations on affected paths. In the 09:00-09:15 window, 31 of 90 investigations lacked normalized ETA and 296 of 1410 transport attempts returned 429. A current payload uses `estimated_arrival`, while the adapter logged absent `eta`; a captured retry also preceded Retry-After. These are separate leads, not a complete diagnosis. Authorized source reads and manual investigation remain available where evidence age is clear. The transport owner is checking schema rollout and shared usage; the application owner is replaying null ETA, code mappings, and cache fallback. Supervisors are identifying decisions made from affected recommendations. Next update at 09:45 UTC with impact scope and recovery evidence; no recovery time is yet confirmed.

**Operations lead, 09:25 UTC:** Some pilot investigations showed missing arrival information and inconsistent recommendations. We paused affected recommendations and directed staff to the existing manual workflow. Shipment updates remain manual; supervisors are checking whether staff acted on affected advice. The pilot may be slower while we establish reliable evidence. At 09:45 UTC we will report the affected scope and decide whether a small reviewed group can resume or whether the pause continues. We have not confirmed a recovery time.

## Handoff and operator proof

Assign application behavior to the support engineering owner, API contracts and shared budgets to the transport owner, code mappings and labels to the regional supervisor, access to the security/data owner, and the go/no-go decision to the operations sponsor. Specify backup contacts and coverage, not just team names. Have an independent operator use the runbook to pause recommendations, locate a request, identify stale or missing evidence, communicate impact, and explain restart criteria. Failed steps become runbook improvements; absent rehearsal remains a readiness blocker.

## Productization review

These are candidate findings, not a prefilled learner answer. Northstar and Atlas both need bounded retries, explicit unknown states, provenance, reviewable evidence, and denial tests. Northstar's local action-ID extension demonstrates how a concrete engagement need can improve a shared approval primitive without replacing its contract.

| Finding | Defensible home now | Evidence needed before broader investment |
| --- | --- | --- |
| Retry-After and attempt bounds | Shared library | Same transport contract; service-specific budgets stay configurable |
| Payload-bound approval and local idempotency | Shared primitive; future platform candidate | Verified identity, durable audit, external effect reconciliation across multiple consumers |
| Audit event vocabulary | Shared logging convention/template | Multiple operators needing correlated traces and retention controls |
| Retrieval case metrics | Shared evaluation helpers | Stable definitions; customer-specific labels and thresholds remain local |
| Atlas shipment codes and supervisor classes | Customer-specific rules | Another engagement with equivalent semantics, not merely similar field names |
| Regional policy boundaries | Customer configuration plus security design | Explicit policy authority and enforcement needs; never generic defaults granting access |
| Incident communication and handoff | Reusable templates | Independent operator feedback and maintenance owner |
| Cross-system evidence workspace | Product discovery candidate | Repeated buyer/user need, adoption, workflow value, support cost, and willingness to fund it |

A platform candidate is not an approved roadmap commitment. An alternative is to keep two small adapters until a third engagement clarifies the boundary. Revisit when duplication causes measurable maintenance or safety cost. Reject a universal logistics/support agent abstraction: similar workflow diagrams do not establish shared domain authority.

Return to your original artifacts, explain where evidence changed your decisions, and update the [rubric](../../docs/learning-paths/field-readiness-rubric.md). Stop at checkpoint 3.
