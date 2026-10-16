---
search:
  exclude: true
---
# Stage 2: discovery reveal and scope

Open only after saving the Stage 1 discovery record. Compare these answers with your questions: what would you have missed?

## Customer answers

The sponsor owns backlog reduction. Regional supervisors own exception resolution. Dispatch operators investigate cases. The transport platform team owns shipment API contracts. A warehouse administrator owns a legacy portal. Security owns regional access approval; the support team owns incidents after handoff.

Observation of six synthetic cases shows operators copying a shipment identifier between a transport system, warehouse portal, carrier messages, and policy notes. Investigation takes 9 to 24 minutes in this tiny sample, but it is not a representative baseline. Some queue entries are stale or already resolved. "Delayed" means different things in the warehouse and carrier systems.

| Source | Access discovered | Authority and limitation |
| --- | --- | --- |
| Transport management system | Read-only shipment API | Current transport state; owner must approve contract use |
| Warehouse portal | No supported API; approved daily CSV export | Warehouse events; export has an as-of timestamp and can lag |
| Carrier messages | Manually attached notes | Helpful evidence, not authoritative shipment state |
| Regional policy folder | Regional access only | Supervisor rules differ by region and shipment class |
| Exception queue | Read-only CSV for pilot discovery | May contain duplicates and already closed cases |

US and EU records must remain separate. Codes such as `EX7` and `DLY` are not normalized across sources. Staff use a manual override workflow when documents disagree; supervisors record the reason. No one has authorized the proposed software to change shipment state. The manual process remains available.

The sponsor still asks: "Can we just automate all exception handling?" Explain your response using observed workflow constraints, not your preference for a particular architecture.

## Scope task

Revise the workflow and stakeholders. Preserve wrong assumptions and explain why they changed. Write:

1. A one-paragraph problem statement naming the user, bottleneck, and evidence gap.
2. In-scope and out-of-scope workflows, systems, regions, and shipment classes.
3. A pilot goal with measurable workflow value and a manual baseline plan.
4. Success criteria with denominators, reviewer ownership, and a safety stop condition.
5. Launch blockers, accepted uncertainties, and owners for resolving them.

Choose between broad automation, a narrower investigation aid, or a no-build process change. Defend the smallest slice that can test value. Describe how you would detect a stale CSV, conflicting code mapping, missing record, or region mismatch. Name the source of truth for each field. A fluent recommendation cannot resolve conflicting authority.

## Exit gate

Ask the sponsor role to challenge one exclusion. Record your answer and what evidence would justify expanding scope. Do not begin coding. Open [Stage 3: constraints and design](03-constraints-and-design.md) after saving your scope agreement.

Attempt the exercise before opening the reference solution.
