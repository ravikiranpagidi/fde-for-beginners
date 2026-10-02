# Evaluation plan

## When to use this

Before implementing a change or selecting a launch threshold, for AI and non-AI systems.

## Who contributes

Engineer, domain reviewer, workflow owner, operator, and the person who accepts risk.

## What good looks like

A reproducible comparison with representative failures, explicit denominators, and a decision the evidence can support.

## Behavior under evaluation

- User workflow and system boundary:
- Change or hypothesis:
- Baseline implementation:
- Expected successful behavior:
- Expected rejection, abstention, and degraded behavior:

## Dataset and execution

- Dataset location / version and synthetic or approved provenance:
- Eligible cases, exclusions, and important subgroups:
- Happy paths, edge cases, adversarial inputs, and dependency failures:
- Runtime, configuration, seed or deterministic controls:
- Exact command and report location:

| Metric | Definition / denominator | Baseline | Pass criterion | Limitation |
| --- | --- | --- | --- | --- |
| | | | | |

## Failure analysis and review

- Failure categories, including retrieval versus generation when relevant:
- Human-review sample and disagreement process:
- Safety blockers that cannot be averaged away:
- Regression strategy and held-out cases:
- Threshold change history and rationale:

## Production follow-through

- Signals monitored after launch:
- Alert / pause criteria:
- Dataset refresh triggers:
- Evaluation owner and acceptance owner:
- Next review date:

Do not change expected labels solely to match an implementation. The [RAG lab](../labs/02-rag-and-evaluation/README.md) demonstrates a report with an intentional miss.
