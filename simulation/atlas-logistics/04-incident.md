---
search:
  exclude: true
---
# Stage 4: incident evidence

Open after committing to a design and production plan. The facilitator now places you on call for an inherited read-only pilot. Its implementation may differ from your proposal. Identify which of your controls would have detected or contained these symptoms, but respond to the evidence actually supplied.

At 09:18, dispatch reports intermittent missing ETAs and different recommendations for similar shipments. The pilot has no shipment-write capability. Operators can still make manual downstream changes, so misleading recommendations have consequences even without an automated write tool. All timestamps below are UTC on 2026-10-12.

## Evidence packet

Selected events, not a complete trace:

```json
{"time":"09:12:03","request_id":"a41","shipment":"US-S401","attempt":1,"status":429,"retry_after_seconds":20}
{"time":"09:12:04","request_id":"a41","shipment":"US-S401","attempt":2,"status":429,"retry_after_seconds":19}
{"time":"09:12:04","request_id":"a41","event":"cache_fallback","cache_age_minutes":47}
{"time":"09:12:05","request_id":"a41","event":"recommendation","classification":"monitor","eta_present":false,"rules_version":"r3"}
{"time":"09:13:10","request_id":"a42","shipment":"US-S402","attempt":1,"status":200}
{"time":"09:13:10","request_id":"a42","event":"adapter_warning","field":"eta","reason":"absent"}
{"time":"09:13:11","request_id":"a42","event":"recommendation","classification":"escalate","eta_present":false,"rules_version":"r3"}
```

| Trace | Source | Fetch | Decision evidence available |
| --- | --- | --- | --- |
| a41 | Cache after 429 | Snapshot 08:25 | warehouse `EX7`, carrier note "awaiting clearance", ETA absent in normalized object |
| a42 | Live transport | 09:13 | warehouse `DLY`, carrier note "awaiting clearance", ETA absent in normalized object |
| a43 | Live transport | 09:16 | class hazardous, transport `IN_TRANSIT`, ETA null, supervisor route shown |

Previous captured payload:

```json
{"shipment_id":"US-S401","eta":"2026-10-12T14:00:00Z","status":"IN_TRANSIT","region":"US"}
```

Current payload from trace a42:

```json
{"shipment_id":"US-S402","estimated_arrival":"2026-10-12T16:00:00Z","status":"IN_TRANSIT","region":"US"}
```

Another current payload from trace a43:

```json
{"shipment_id":"US-S403","estimated_arrival":null,"status":"IN_TRANSIT","region":"US","class":"hazardous"}
```

Deployment notes: adapter `0.4` and recommendation rules `r3` deployed at 08:50. Worker concurrency increased from 2 to 8. A provider bulletin says response contract `shipment-v3` begins rollout this morning. The warehouse export was taken at 06:00 local time; the display does not state its timezone. No change to the pilot's write permissions is recorded.

| Metric, 15-minute windows | Before 08:50 | 09:00 to 09:15 |
| --- | --- | --- |
| Transport attempts per minute, shared credential | 28 | 94 |
| HTTP 429 fraction of attempts | 0/420 | 296/1410 |
| Investigations with missing normalized ETA | 2/80 | 31/90 |
| Recommendations reviewed as inconsistent | 1/20 | 7/20 |
| Pilot process uptime | 100% | 100% |

There is no alert on evidence age, missing ETA, per-credential budget, or recommendation disagreement. Samples are too small to infer all affected cases. You have not yet confirmed whether any operator acted on an incorrect recommendation.

## Incident task

Respond in the first 15 minutes using the [postmortem structure](../../templates/postmortem.md), but label hypotheses as hypotheses:

1. What should be checked first, and how does that reduce user harm?
2. What do we know, with evidence identifiers?
3. What do we only suspect, and how would we test each hypothesis?
4. What should be disabled?
5. What can continue operating, under which conditions?
6. Which boundaries fail closed, and which permit a degraded read-only fallback?
7. What customer-visible behavior should change?
8. Who needs to be informed, and who owns each decision?
9. What is the immediate reversible mitigation?
10. What permanent fixes are supported by evidence, versus still hypothetical?
11. Which regression and recovery tests would prevent recurrence?
12. What missing monitoring signal would have detected the problem earlier?

Build a timeline and an impact query. Account for unknown operator actions and records read from cache. Propose restart criteria and compare rollback with a targeted fix; explain why either alone may be insufficient. Do not silently fill null ETA values or suppress validation errors to make the demo work.

## Two audience updates

Write a technical customer-lead update of at most 180 words: facts, impact, current state, mitigation, next investigation, owner, and next update time. Write an operations-leader update of at most 120 words: workflow impact, business risk, containment, manual fallback, and the next decision. Preserve the same facts and uncertainty across both. Do not promise a recovery time you cannot support.

Save the incident analysis and both updates before opening [Stage 5: handoff and productization](05-handoff.md). Attempt the exercise before opening the reference solution.
