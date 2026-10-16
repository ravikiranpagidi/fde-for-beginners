# Field readiness: evidence and gaps

This is a learning rubric, not certification, hiring equivalence, employer endorsement, or a job-readiness guarantee. Do not add scores or average the levels. Framework count, lines of code, service count, and complexity do not establish field readiness.

Review observable artifacts from [Northstar](../../project/northstar-support-copilot/README.md) and [Atlas](../../simulation/atlas-logistics/README.md). A reviewer should be able to reproduce a claim or follow its evidence without the builder narrating it. Choose the highest level supported by the artifacts, record counterevidence, and identify the next exercise. Field-Ready Evidence describes the submitted exercise evidence, not the person's readiness for every production environment.

## Observable criteria

| Category | Needs Development | Working | Production-Aware | Field-Ready Evidence |
| --- | --- | --- | --- | --- |
| Discovery | Generic requirements questions without priorities | Identifies user and current workflow; separates facts and assumptions | Prioritizes bottleneck, owner, permission, fallback, and baseline questions | Revised scope is traceable to observed answers; a peer can identify what changed and why |
| Problem framing | Restates request for an agent | Names user, problem, in/out scope, and goal | Defines metric denominators, quality guardrails, and launch blockers | Sponsor challenge is answered with evidence; pilot decision and revision trigger are recorded |
| Technical design | Stack diagram without data authority | Maps components, inputs, and outputs | Explains trust boundaries, freshness, failures, and rejected alternatives | ADR connects constraints to decisions and gives testable revisit triggers and operational ownership |
| Implementation | Demo cannot be reproduced | Local workflow runs with typed inputs and visible state | Shared primitives compose without copied engines; unsafe states are explicit | Independent checkout/run evidence and behavioral tests substantiate happy and exception paths |
| Integration | Assumes every successful HTTP response is usable | Validates basic response and missing record | Distinguishes source authority, schema, identity, and retry contracts | Contract drift, ownership mismatch, missing fields, and uncertain effects have tested behavior |
| Evaluation | Shows a good answer without labels | Versioned cases and generated results exist | Separates recall, citation validity, abstention, workflow, and safety denominators | Reproducible report includes misses, failure analysis, and launch thresholds tied to user impact |
| Reliability | Says "added retries" | Demonstrates timeout and bounded recovery | Separates retryable/validation errors and preserves action identity | Real timeout, rate limit, exhaustion, concurrency, and ambiguous-outcome evidence justify recovery limits |
| Security judgment | Treats model output or UI confirmation as authority | Rejects unapproved writes and validates input | Explains data/identity boundaries, token binding, prompt injection, and ACL gaps | Denial tests include forged/reused approval and restricted data; remaining threat boundaries block expansion |
| Production readiness | Marks every item ready | Checklist has owners and open items | Distinguishes local readiness from IAM, data, operations, and support gaps | Conditional pilot decision has eligible scope, stop criteria, monitoring, rollback, and review expiry |
| Incident response | Jumps to one cause or blames AI | Records symptoms, timeline, and a mitigation | Separates detection, containment, hypotheses, recovery, and prevention | Evidence-linked investigation tests alternatives, scopes user impact, and defines restart/regression criteria |
| Communication | Same vague update for every audience | States facts, impact, and next step | Technical and executive updates preserve uncertainty while changing emphasis | Both updates identify decision/owner/time; no unsupported recovery promise or contradictory impact claim |
| Handoff | Builder remains the only operator | Runbook and owner list exist | Support, rollback, metrics, escalation, evaluation ownership, and review date are explicit | Independent operator drill records mistakes and resulting revisions; builder assistance is disclosed |
| Productization | Claims reuse because files were shared | Identifies repeated needs and customer rules | Proposes a small contract with alternatives, owner, compatibility, and maintenance cost | Two engagement examples support the boundary; a counterexample rejects overgeneralization and adoption evidence guides next investment |

## Evidence review record

Use one row per category; do not compute a total. Strong evidence supports the selected level, partial evidence has an explicit limit, and missing evidence gets a concrete next exercise.

| Category | Selected level | Strong evidence link | Partial / missing evidence and counterevidence | Next exercise, owner, review date |
| --- | --- | --- | --- | --- |
| Discovery | | | | |
| Problem framing | | | | |
| Technical design | | | | |
| Implementation | | | | |
| Integration | | | | |
| Evaluation | | | | |
| Reliability | | | | |
| Security judgment | | | | |
| Production readiness | | | | |
| Incident response | | | | |
| Communication | | | | |
| Handoff | | | | |
| Productization | | | | |

For example, a passing timeout test supports reliability evidence but does not prove a distributed ticket adapter is idempotent. A local approval prompt supports the lab threat model but does not establish verified enterprise identity. Keep those gaps visible.

## FDE Evidence Pack

Keep one personal directory with an index naming the repository commit, environment, dates, reviewers, synthetic-data declaration, and reproduction commands. Use ordinary files; no new portfolio framework is required.

| Artifact | What it should let a reviewer verify |
| --- | --- |
| Problem statement | User, workflow bottleneck, scope, success denominator, and non-goals |
| Discovery notes | Prioritized questions, answers, stakeholders, facts/assumptions/unknowns, and changed decisions |
| Architecture diagram | Source authority, data flow, permission boundaries, and fallback |
| ADR | Decision, rejected alternative, evidence, tradeoff, and revisit trigger |
| Working code reference | Exact commit and local commands, with customer versus shared code boundaries |
| Test output | Meaningful success/denial/failure checks and environment; no claim beyond what ran |
| Evaluation output | Generated Northstar JSON plus a readable analysis of failures and denominators |
| Production readiness review | Filled checklist, named owner roles, blockers, and conditional pilot decision |
| Incident analysis | Atlas timeline, evidence, hypotheses, containment, recovery, and regression plan |
| Stakeholder updates | Separate technical and executive messages preserving the same facts |
| Runbook | Support path, operational metrics, rollback, escalation, and independent rehearsal record |
| Productization proposal | Classification table, one small boundary, rejected abstraction, owner, and next evidence |

Use the eight [field templates](../../README.md#v01-learning-environment) where appropriate; do not duplicate them into a new template set. Remove tokens, credentials, private customer/employer information, and raw personal data before sharing. Synthetic exercise results are not real customer outcomes.

Ask a peer to choose one claim and reproduce it, then select one unresolved gap. Record the review and next exercise in the [progress tracker](progress-tracker.md). Stop after checkpoint 3; future infrastructure work is in the [roadmap](../../ROADMAP.md).
