---
search:
  exclude: true
---
# Stage 5: handoff and productization

Proceed after recording incident containment and a recovery decision. Your task is to make the engagement operable by someone besides its builder.

## Handoff task

Use the [rollout and handoff template](../../templates/rollout-and-handoff.md). Deliver a runbook containing prerequisites, approved workflows, known limitations, source freshness checks, normal operation, failure symptoms, and recovery verification. Include:

- Ownership matrix for application, source contracts, policy review, data access, rate budgets, evaluation, customer communication, and launch decisions. Include a backup and support hours.
- Support path, severity definitions, escalation thresholds, and a method for recording unresolved operator impact.
- Exact disable/rollback steps, configuration and data compatibility checks, retained evidence, and reconciliation of manual actions. State what rollback cannot undo.
- Operational metrics with denominators, alert owners, and response actions. Include evidence quality as well as HTTP health.
- Evaluation ownership and triggers for relabeling/retesting after contract, policy, or rule changes.
- Next review date and explicit criteria for continuing, narrowing, or stopping the pilot.

## Independent operator drill

Give the runbook to a peer without narrating it. Ask them to identify a stale-data investigation, stop recommendations, find affected request IDs, select the manual path, and state what evidence permits recovery. Record elapsed time, questions, incorrect steps, and the resulting runbook changes. If no peer is available, mark independent operation **Not Ready** and schedule the drill. Do not label a builder walkthrough independent evidence.

## Productization task

Complete the single [field-to-product exercise](../../docs/field/productization.md#exercise-atlas-and-northstar) using both engagements. Identify what repeated, what remains Atlas-specific, and what deserves more evidence before abstraction. Preserve an empty classification table in your learner copy before filling it from your own findings. Propose one reusable boundary and explicitly reject one premature abstraction.

## Review gate

Assemble the [FDE Evidence Pack](../../docs/learning-paths/field-readiness-rubric.md#fde-evidence-pack) and apply all thirteen rubric categories. Record strong, partial, and missing evidence, a reviewer, and the next exercise. Do not calculate an aggregate score.

Only after completing the exercises, open [Reference solution: one defensible approach](reference-solution.md). It contains alternatives and revisit triggers, not a single perfect answer. Compare decisions and evidence before changing your artifacts. Stop at checkpoint 3 after review.
