# Choose your path

Choose the next gap in your evidence, not the most advanced-sounding topic. Everyone should attempt [discovery](../field/customer-discovery.md) and [problem framing](../field/problem-framing.md), even if they can already build the software.

| Background | Begin here | Produce before advancing |
| --- | --- | --- |
| Beginner developer | [What is FDE?](../foundations/what-is-fde.md), [lifecycle](../foundations/fde-lifecycle.md), then discovery | Workflow map, a constrained problem statement, and successful local setup |
| Software engineer | Discovery, problem framing, then [solution design](../field/solution-design.md) | A design justified by customer evidence, including integration failures |
| Data engineer | Workflow discovery, solution boundaries, [production reality](../field/production-reality.md) | Data authority/freshness map and user-facing failure behavior |
| ML or AI engineer | Problem framing, integration design, production review | A deterministic baseline and acceptance criteria beyond model quality |
| Solutions architect or consultant | Design exercise, local setup, then implementation work when Phase 2 arrives | Executable checks now; tested integration code later, not just diagrams |
| Senior engineer | Discovery exercise, scope negotiation, readiness review | A defensible no-build/build decision, rollout blockers, and reuse proposal |

## Find the prerequisite gap

Before the future labs, you should be able to run Python, read a stack trace, write a function with explicit inputs and outputs, distinguish JSON from an in-memory object, and explain an HTTP status. You should also understand how to avoid committing credentials. If these are unfamiliar, use small local exercises to practice and return to [setup](../../START_HERE.md). This repository does not yet contain a full programming course.

An experienced engineer can skip explanatory reading, but should still produce and review the artifacts. A correct diagram with no user or success criterion is not sufficient evidence.

## The route through v0.1

**Available now:** Start Here -> selected foundation guides -> discovery record -> success agreement -> scoped design -> readiness review.

**Planned after checkpoint approval:** Reliable API Integration -> RAG and Evaluation -> MCP and Safe Tool Execution -> Northstar Support Copilot -> Atlas Logistics simulation. These are future experiences, not clickable missing folders or runnable claims. See [ROADMAP](../../ROADMAP.md).

When the labs arrive, software engineers may spend more time on discovery, AI engineers on reliability, and architects on implementation. All paths converge on the same end-to-end evidence: problem, constraints, decisions, implementation, validation, outcome, and lessons.

## Exercise: choose a deliberate next step

Select two gaps from the [skills matrix](skills-matrix.md). For each, identify evidence you already possess and evidence you still need. Choose one exercise that would expose a mistake, not merely confirm familiarity. Record it in the [progress tracker](progress-tracker.md), with a reviewer and next action.

Example: knowing retry terminology is foundation evidence. Showing that a timed-out write cannot create duplicates requires implementation evidence. Until the lab exists, document the intended semantics and test cases without marking them as passed.
